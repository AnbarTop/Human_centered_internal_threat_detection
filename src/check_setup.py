import os
import sys
import pandas as pd
import nltk
from textblob import TextBlob

# Configuración de rutas (relativas para que funcione en cualquier PC)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')

# Archivos clave del dataset CERT r4.2 que esperamos encontrar
REQUIRED_FILES = ['logon.csv', 'device.csv', 'email.csv', 'http.csv', 'psychometric.csv']

def print_status(message, status="INFO"):
    colors = {
        "INFO": "\033[94m[INFO]\033[0m",    # Azul
        "OK": "\033[92m[OK]\033[0m",        # Verde
        "ERROR": "\033[91m[ERROR]\033[0m",  # Rojo
        "WARN": "\033[93m[AVISO]\033[0m"    # Amarillo
    }
    prefix = colors.get(status, "[?]")
    print(f"{prefix} {message}")

def check_environment():
    print("--- INICIANDO VERIFICACIÓN DEL SISTEMA TFM ---")
    
    # 1. Verificamos la estructura de directorios
    if os.path.exists(DATA_RAW_DIR):
        print_status(f"Directorio de datos encontrado: {DATA_RAW_DIR}", "OK")
    else:
        print_status(f"No se encuentra el directorio: {DATA_RAW_DIR}", "ERROR")
        print_status("Por favor, crea la carpeta 'data/raw' en la raíz del proyecto.", "WARN")
        return

    # 2. Verificamos Archivos del Dataset
    missing_files = []
    found_files = []
    
    print_status("Verificando integridad del Dataset CERT r4.2...", "INFO")
    
    for filename in REQUIRED_FILES:
        filepath = os.path.join(DATA_RAW_DIR, filename)
        if os.path.exists(filepath):
            found_files.append(filepath)
            # Leemos solo las primeras 5 líneas para no saturar la RAM
            try:
                df = pd.read_csv(filepath, nrows=5)
                print_status(f"  -> {filename}: Detectado y legible ({len(df.columns)} columnas)", "OK")
            except Exception as e:
                print_status(f"  -> {filename}: Error al leer ({str(e)})", "ERROR")
        else:
            missing_files.append(filename)

    if missing_files:
        print_status(f"Faltan archivos en data/raw: {missing_files}", "WARN")
    else:
        print_status("Todos los archivos críticos del dataset están listos.", "OK")

    # 3. Preparamos 'Motor Psicológico' (NLP)
    print_status("Inicializando librerías de Psicología Computacional (NLTK)[...]", "INFO")
    try:
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        print_status("Diccionarios de Sentimiento (VADER) descargados correctamente.", "OK")
    except Exception as e:
        print_status(f"Error descargando NLTK data: {e}", "ERROR")

    print("\n--- RESUMEN ---")
    if not missing_files:
        print("\033[92m¡SISTEMA LISTO! Todo preparado para empezar la fase de análisis.\033[0m")
    else:
        print("\033[93mFaltan archivos, pero el entorno Python funciona correctamente.\033[0m")

if __name__ == "__main__":
    check_environment()