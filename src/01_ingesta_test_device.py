import pandas as pd
import os
import time

# Definimos rutas relativas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(BASE_DIR, 'data', 'raw', 'device.csv') # Usamos device.csv para probar
PARQUET_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'device.parquet')

def test_parquet_conversion():
    print("*** INICIANDO PRUEBA DE CONVERSIÓN A PARQUET ***")
    
    # 1. Leemos el CSV original y medimos el tiempo
    start_csv = time.time()
    print(f"Leyendo CSV desde: {RAW_FILE}")
    df = pd.read_csv(RAW_FILE)
    end_csv = time.time()
    print(f"[OK] CSV leído en {end_csv - start_csv:.2f} segundos. Filas: {len(df)}")

    # 2. Guardamos como formato '.Parquet'
    print("Convirtiendo a formato Parquet[...]")
    df.to_parquet(PARQUET_FILE, engine='pyarrow', index=False)
    print(f"[OK] Archivo Parquet guardado en: {PARQUET_FILE}")

    # 3. Leemos el Parquet y comparamos tiempos
    start_parquet = time.time()
    print("Leyendo el nuevo archivo Parquet...")
    df_pq = pd.read_parquet(PARQUET_FILE, engine='pyarrow')
    end_parquet = time.time()
    print(f"[OK] Parquet leído en {end_parquet - start_parquet:.2f} segundos. Filas: {len(df_pq)}")
    
    # Comparativa de tamaño
    size_csv = os.path.getsize(RAW_FILE) / (1024 * 1024)
    size_parquet = os.path.getsize(PARQUET_FILE) / (1024 * 1024)
    
    print("\n *** RESUMEN DE RENDIMIENTO ***")
    print(f"Tamaño CSV: {size_csv:.2f} MB")
    print(f"Tamaño Parquet: {size_parquet:.2f} MB")
    print("¡Mesa de operaciones lista para la M3!")

    # assert len(df) == len(df_pq), "ERROR: Pérdida de filas en conversión"
    # assert df.columns.tolist() == df_pq.columns.tolist(), "ERROR: Columnas modificadas"

if __name__ == "__main__":
    # Aseguramos que el directorio de destino existe
    os.makedirs(os.path.dirname(PARQUET_FILE), exist_ok=True)
    test_parquet_conversion()
