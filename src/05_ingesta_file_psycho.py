import pandas as pd
import os
import time

# Configuracion de rutas relativas al directorio del script
# __file__ garantiza que la ruta se resuelva dinamicamente sin depender del CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_RAW = os.path.join(BASE_DIR, 'data', 'raw', 'file.csv')
PSYCHO_RAW = os.path.join(BASE_DIR, 'data', 'raw', 'psychometric.csv')
FILE_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed', 'file_daily_activity.parquet')
PSYCHO_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed', 'psychometric.parquet')

def process_remaining_data():
    """
    Procesa los dos datasets restantes del pipeline M3.2:
    1. file.csv: actividad de acceso/copias de archivos (agregación diaria)
    2. psychometric.csv: rasgos Big Five (tabla estática dimensional)
    
    Nota ética: Los rasgos de personalidad se persisten como contexto estático,
    pero el análisis SHAP (M3.4) confirmó que su contribución al modelo es marginal.
    Esto refuerza la viabilidad legal del sistema: detecta anomalías por COMPORTAMIENTO
    (variables dinámicas), no por rasgos inherentes del individuo.
    """
    print("*** INICIANDO EXTRACCIÓN DE ARCHIVOS (FILE) Y PSICOMETRÍA ***")
    
   # =========================================================================
    # 1. PROCESAR FILE.CSV (Actividad diaria de acceso a archivos)
    # =========================================================================
    print("\n1. Procesando file.csv...")
    start_file = time.time()
    
    # Carga completa: file.csv (~184MB) es manejable en RAM sin chunking
    df_file = pd.read_csv(FILE_RAW)
    df_file['date'] = pd.to_datetime(df_file['date'])
    df_file['day'] = df_file['date'].dt.date
    
    # Agregacion: conteo de operaciones de archivo por usuario y dia
    # Esta metrica es clave para detectar exfiltracion masiva (fase CPIR: acción maliciosa)
    daily_file = df_file.groupby(['user', 'day']).agg(
        file_activity_count=('id', 'count')
    ).reset_index()
    
    # Persistencia en formato columnar optimizado para futuras fases de modelado
    daily_file.to_parquet(FILE_PROCESSED, engine='pyarrow', index=False)
    end_file = time.time()
    print(f"[OK] Archivo 'file' procesado en {end_file - start_file:.2f} seg. Filas: {len(daily_file)}")

    # =========================================================================
    # 2. PROCESAR PSYCHOMETRIC.CSV (Datos estaticos Big Five)
    # =========================================================================
    print("\n2. Procesando psychometric.csv[...]")
    start_psycho = time.time()
    
    # Este archivo no cambia por dia: es un perfil estatico por usuario (1000 registros)
    # Variables: O (Openness), C (Conscientiousness), E (Extraversion), A (Agreeableness), N (Neuroticism)
    df_psycho = pd.read_csv(PSYCHO_RAW)
    
    # Persistencia directa a Parquet: mantenemos ecosistema optimizado
    # NOTA CRITICA: Aunque se incluye en la matriz maestra, el analisis SHAP (M3.4) revela
    # que estas variables tienen contribucion marginal (~0) en la detección de anomalias.
    # Esto es ETICAMENTE POSITIVO: el sistema no discrimina por personalidad inherente,
    # sino por desviaciones conductuales observables (after-hours, USB, sentimiento).
    df_psycho.to_parquet(PSYCHO_PROCESSED, engine='pyarrow', index=False)
    end_psycho = time.time()
    print(f"[OK] Archivo 'psychometric' convertido en {end_psycho - start_psycho:.2f} seg. Filas: {len(df_psycho)}")
    
    print("\n*** FASE DE INGESTA TOTALMENTE COMPLETADA ***")
    print("¡Todos los datos brutos han sido domados y convertidos a Parquet!")
    print("\n📋 Reflexión metodológica:")
    print("   - file_activity_count: variable dinámica de alto peso predictivo")
    print("   - Big Five (O,C,E,A,N): contexto estático con contribución marginal")
    print("   → El sistema detecta POR CÓMO ACTÚAS, no por QUIÉN ERES.")
    print("   → Esto garantiza viabilidad ética y legal (RGPD Art. 22 + AI Act).")

if __name__ == "__main__":
    # Creacion segura del directorio de salida si no existe
    os.makedirs(os.path.dirname(FILE_PROCESSED), exist_ok=True)
    os.makedirs(os.path.dirname(PSYCHO_PROCESSED), exist_ok=True)
    process_remaining_data()

##################### REFLEXION FINAL: ##################################################
# NOTA LEGAL RGPD + AI ACT:
# --------------------------------------------------------------------------------------#
# El Art. 22 del RGPD prohíbe decisiones automatizadas basadas en datos sensibles
# (incluyendo rasgos de personalidad) sin consentimiento explícito.
# El hecho de que el modelo IGNORE los Big Five en la práctica (SHAP ≈ 0)
# constituye una salvaguarda técnica de Privacy by Design:
# - No perfilamos por quién eres (rasgos estáticos)
# - Detectamos por cómo actúas (desviaciones dinámicas)
# Esto alinea el sistema con el principio de minimización de datos (Art. 5.1.c RGPD).
# Además, el AI Act enfatiza la necesidad de transparencia y explicabilidad.
# Al documentar claramente esta arquitectura de ingesta y su impacto en el modelado,
# garantizamos que el sistema no solo es efectivo, sino también éticamente responsable y
# legalmente viable para su implementación en entornos corporativos.
##########################################################################################