import pandas as pd
import os
import time

# Configuracion de rutas relativas al directorio del script
# __file__ garantiza que la ruta se resuelva dinámicamente sin depender del CWD del entorno
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGON_RAW = os.path.join(BASE_DIR, 'data', 'raw', 'logon.csv')
LOGON_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed', 'logon_daily_activity.parquet')

def process_logon_logs():
    """
    Procesa logon.csv para derivar métricas diarias de actividad y comportamiento fuera de horario.
    Estrategia: carga completa en memoria (dataset <100MB), derivación temporal, 
    filtrado criminológico (after-hours) y agregación usuario-día.
    """
    print("*** INICIANDO EXTRACCIÓN DE LOGS DE ACCESO (LOGON) ***")
    start_time = time.time()
    
    # 1. Carga completa: logon.csv es suficientemente ligero para procesamiento directo en RAM
    # No requiere chunking, lo que simplifica la pipeline vs HTTP/Email
    print("Cargando el archivo en memoria...")
    df = pd.read_csv(LOGON_RAW)
    
    # 2. Ingenieria temporal basica
    # Conversion explicita a datetime64 para habilitar acceso a atributos .dt
    print("Procesando fechas e identificando actividad nocturna...")
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date          # Granularidad de integración (usuario-día)
    df['hour'] = df['date'].dt.hour         # Para filtrado de ventanas temporales sospechosas
    df['weekday'] = df['date'].dt.weekday # 0=Lunes, 6=Domingo (para fines de semana)
    
    # 3. Filtro criminologico: deteccion de actividad fuera de horario laboral estandar
    # Definicion operativa: horas nocturnas (20:00-06:00) o fines de semana (Sabado/Domingo)
    # Esta señal es un predictor clave en modelos CPIR (fase de preparacion activa/explotacion)
    df['is_after_hours'] = ((df['hour'] >= 20) | (df['hour'] <= 6) | (df['weekday'] >= 5)).astype(int)
    
    # 4. Agregacion diaria por usuario
    # Generamos dos metricas por usuario-día: volumen total y volumen en ventanas de riesgo
    print("Agregando métricas por usuario y día...")
    daily_logon = df.groupby(['user', 'day']).agg(
        total_logon_activity=('id', 'count'),
        after_hours_activity=('is_after_hours', 'sum')
    ).reset_index()
    
    # 5. Persistencia en formato columnar optimizado para analisis posterior
    print("Guardando archivo Parquet comprimido...")
    daily_logon.to_parquet(LOGON_PROCESSED, engine='pyarrow', index=False)
    
    end_time = time.time()
    print("\n*** OPERACIÓN COMPLETADA ***")
    print(f"Tiempo total: {end_time - start_time:.2f} segundos.")
    print(f"Filas generadas: {len(daily_logon)}")
    print(f"Archivo guardado en: {LOGON_PROCESSED}")

if __name__ == "__main__":
    # Creacion segura del directorio de salida si no existe
    os.makedirs(os.path.dirname(LOGON_PROCESSED), exist_ok=True)
    process_logon_logs()