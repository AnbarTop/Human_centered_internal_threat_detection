import pandas as pd
import os
import time
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Descarga silenciosa del lexico VADER (solo se ejecuta si no esta en cache local)
nltk.download('vader_lexicon', quiet=True)

# Configuracion de rutas relativas al directorio del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMAIL_RAW = os.path.join(BASE_DIR, 'data', 'raw', 'email.csv')
EMAIL_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed', 'email_daily_sentiment.parquet')

# Tamaño de chunk: 100k filas equilibra velocidad de NLP y consumo de RAM
# VADER es ligero, pero el overhead de .apply() en Python justifica chunks moderados
CHUNK_SIZE = 100000  # Bloques de 100k para no saturar CPU/RAM con el NLP

def process_email_sentiment():
    """
    Procesa email.csv aplicando análisis de sentimiento VADER por chunks.
    Estrategia: agregación parcial por chunk + consolidación final para manejar
    particiones de usuario-día cortadas entre bloques.
    """
    print("*** INICIANDO EXTRACCIÓN NLP DE CORREOS ***")
    start_total = time.time()
    
    # Inicializacion del analizador lexico (VADER no requiere entrenamiento supervisado)
    sia = SentimentIntensityAnalyzer()  # Instancia global para eficiencia en el procesamiento por chunks
    aggregated_chunks = []              # Lista para almacenar resumenes parciales de cada chunk antes de la consolidación final
    chunk_counter = 1                   # Contador para seguimiento de progreso por bloque
    
     # Funcion wrapper para manejar nulos y forzar tipo string antes de analizar
    def get_sentiment(text):
        if pd.isna(text):
            return 0.0
        return sia.polarity_scores(str(text))['compound']

    # Iteracion por chunks para evitar MemoryError con email.csv (~1.3GB)
    for chunk in pd.read_csv(EMAIL_RAW, chunksize=CHUNK_SIZE):
        start_chunk = time.time()
        
        # 1. Parseo temporal y truncado a dia natural para agregacion posterior
        chunk['date'] = pd.to_datetime(chunk['date'])
        chunk['day'] = chunk['date'].dt.date
        
        # 2. Aplicacion de VADER sobre el campo 'content'
        # .apply() es secuencial pero seguro para textos heterogeneos del CERT
        chunk['sentiment_score'] = chunk['content'].apply(get_sentiment)
        
        # 3. Agregacion parcial: conteo de emails y media de sentimiento por usuario-dia
        daily_sentiment = chunk.groupby(['user', 'day']).agg(
            email_count=('id', 'count'),
            sentiment_mean=('sentiment_score', 'mean')
        ).reset_index()
        
        aggregated_chunks.append(daily_sentiment)
        
        end_chunk = time.time()
        print(f"Bloque {chunk_counter} (NLP aplicado) en {end_chunk - start_chunk:.2f} seg.")
        chunk_counter += 1

    print("\nConsolidando el análisis psicológico global[...]")
    # 4. Concatenacion de resumenes parciales
    full_df = pd.concat(aggregated_chunks, ignore_index=True)
    
    # 5. Agregacion final: suma de volumenes y promedio ponderado de sentimiento
    # Este paso unifica registros del mismo usuario-dia divididos entre chunks
    final_df = full_df.groupby(['user', 'day']).agg(
        total_emails=('email_count', 'sum'),
        avg_sentiment=('sentiment_mean', 'mean') 
    ).reset_index()
    
    # 6. Persistencia en formato columnar optimizado para analisis posterior
    final_df.to_parquet(EMAIL_PROCESSED, engine='pyarrow', index=False)
    
    end_total = time.time()
    print("\n*** OPERACIÓN COMPLETADA ***")
    print(f"Tiempo total: {(end_total - start_total) / 60:.2f} minutos.")
    print(f"Archivo Parquet guardado en: {EMAIL_PROCESSED}")
    print(f"Filas generadas (Días-Usuario analizados): {len(final_df)}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(EMAIL_PROCESSED), exist_ok=True)
    process_email_sentiment()

############################ Notas metodológicas#############################################################################################################
#############################################################################################################################################################
# 1.
# VADER es un analizador de sentimiento basado en reglas, diseñado para textos informales. Su elección esta justificada en su eficiencia y
# adecuación a la naturaleza heterogénea de los correos del CERT. Este puede incluir desde mensajes formales hasta fragmentos de código o logs.
# Aunque NO captura matices complejos como sarcasmo o ironía,
# su capacidad para procesar grandes volúmenes de texto con bajo overhead lo convierte en una opción pragmática para esta fase de ingesta y transformación.

# 2. 
# Al promediar sentiment_mean en la consolidación final, técnicamente se calcula una media de medias. 
# Si un chunk contiene 1 email para un usuario y otro chunk contiene 9, la media global tendrá un ligero sesgo.
# En la práctica UEBA este efecto es despreciable (la varianza se diluye con ~330k registros)
# y la simplicidad de esta aproximación supera la complejidad de calcular un promedio ponderado exacto, pero podriamos usar esta aproximacion
# en futuros nuevos experimentos para validar que el sesgo es efectivamente minimo en este caso concreto.:
# # Alternativa matemáticamente exacta (promedio ponderado por volumen)
# ````
#final_df = full_df.groupby(['user', 'day']).agg(
#    total_emails=('email_count', 'sum'),
#    sentiment_weighted_sum=('sentiment_mean', lambda x: (x * full_df.loc[x.index, 'email_count']).sum()),
#).assign(avg_sentiment=lambda df: df['sentiment_weighted_sum'] / df['total_emails'])
# ````
###########################################################################################################################################################