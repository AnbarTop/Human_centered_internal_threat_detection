import pandas as pd
import os
import time

# Configuracion de rutas relativas al directorio del script
# __file__ facilita que la ruta sea dinamica independientemente de donde se ejecute el entorno
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTTP_RAW = os.path.join(BASE_DIR, 'data', 'raw', 'http.csv')
HTTP_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed', 'http_daily_activity.parquet')

# Tamaño del bloque: 1M filas optimiza el balance entre velocidad de E/S y consumo de RAM
# http.csv ronda los ~14GB, por lo que el chunking es imperativo para evitar MemoryError
CHUNK_SIZE = 1000000 

def process_http_logs():
    """
    Procesa http.csv por bloques para agregar la actividad diaria por usuario.
    Estrategia: agregación parcial por chunk + consolidación final para manejar
    particiones de usuarios/días cortadas entre bloques.
    """
    print("*** INICIANDO EXTRACCIÓN MASIVA DE LOGS HTTP ***")
    start_total = time.time()
    
    # Lista para almacenar DataFrames resumidos de cada iteracion
    aggregated_chunks = []
    chunk_counter = 1
    
    # Iterador de chunks: lee secuencialmente sin cargar el archivo completo en memoria
    for chunk in pd.read_csv(HTTP_RAW, chunksize=CHUNK_SIZE):
        start_chunk = time.time()
        
        # 1. Parseo temporal y truncado a día
        # pd.to_datetime infiere formato automaticamente; .dt.date extrae solo la fecha
        # El formato en CERT suele ser "MM/DD/YYYY HH:MM:SS"
        chunk['date'] = pd.to_datetime(chunk['date'])
        chunk['day'] = chunk['date'].dt.date
        
        # 2. Agregacion parcial: conteo de eventos HTTP por usuario y dia dentro del chunk
        # Se cuenta la columna 'id' como proxy de numero de conexiones/registros
        daily_activity = chunk.groupby(['user', 'day'])['id'].count().reset_index()
        daily_activity.rename(columns={'id': 'http_activity_count'}, inplace=True)
        
        # 3. Almacenamiento temporal del resumen parcial
        aggregated_chunks.append(daily_activity)
        
        end_chunk = time.time()
        print(f"Bloque {chunk_counter} procesado en {end_chunk - start_chunk:.2f} segundos.")
        chunk_counter += 1

    print("\nConsolidando todos los bloques...")
    # 4. Concatenamos todos los resumenes
    full_aggregated_df = pd.concat(aggregated_chunks, ignore_index=True)
    
    # 5. Agregacion final: suma de conteos para usuarios/días divididos entre chunks
    # Este paso es critico para garantizar exactitud en la metrica diaria acumulada
    final_df = full_aggregated_df.groupby(['user', 'day'])['http_activity_count'].sum().reset_index()
    
    # 6. Persistencia en formato columnar optimizado para analisis posterior
    final_df.to_parquet(HTTP_PROCESSED, engine='pyarrow', index=False)
    
    end_total = time.time()
    
    print("\n*** OPERACIÓN COMPLETADA ***")
    print(f"Tiempo total: {(end_total - start_total) / 60:.2f} minutos.")
    print(f"Archivo final guardado en: {HTTP_PROCESSED}")
    print(f"Hemos reducido 14 GB a una tabla de {len(final_df)} filas con el perfil diario de cada empleado.")

if __name__ == "__main__":
    # Creamos el directorio de salida si no existe para evitar errores de escritura
    os.makedirs(os.path.dirname(HTTP_PROCESSED), exist_ok=True)
    process_http_logs()