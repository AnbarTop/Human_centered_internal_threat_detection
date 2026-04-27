import pandas as pd
import os
import time

# Configuracio de rutas relativas al directorio del script
# __file__ garantiza que las rutas se resuelvan dinamicamente sin depender del CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw') # LDAP se mantiene en raw como snapshot historico
MASTER_FILE = os.path.join(PROCESSED_DIR, 'master_behavioral_matrix.parquet')

def build_master_matrix():
    """
    Construye la matriz maestra conductual unificando:
    1. Métricas diarias de actividad técnica (logon, http, email, file, device)
    2. Perfil psicométrico estático (Big Five)
    3. Contexto organizativo (LDAP snapshot más reciente)
    
    Estrategia: Outer joins secuenciales para preservar cobertura + imputación controlada
    según política de nulos definida en M3.2 (sección 5.4 del notebook).
    """
    print("*** INICIANDO FUSIÓN: CONSTRUCCIÓN DE LA MATRIZ MAESTRA ***")
    start_time = time.time()

    # =========================================================================
    # 1. CARGA DE PIEZAS DIARIAS PRE-PROCESADAS
    # =========================================================================
    print("Cargando métricas diarias[...]")
    logon = pd.read_parquet(os.path.join(PROCESSED_DIR, 'logon_daily_activity.parquet'))
    http = pd.read_parquet(os.path.join(PROCESSED_DIR, 'http_daily_activity.parquet'))
    email = pd.read_parquet(os.path.join(PROCESSED_DIR, 'email_daily_sentiment.parquet'))
    file_act = pd.read_parquet(os.path.join(PROCESSED_DIR, 'file_daily_activity.parquet'))

    # =========================================================================
    # 2. AGREGANDO METRICAS DE DISPOSITIVOS (USB) A NIVEL DIARIO
    # =========================================================================
    print("Agregando métricas de dispositivos (USB)...")
    device_raw = pd.read_parquet(os.path.join(PROCESSED_DIR, 'device.parquet'))
    device_raw['date'] = pd.to_datetime(device_raw['date'])
    device_raw['day'] = device_raw['date'].dt.date

    # Agregacion: conteo de conexiones/desconexiones por usuario y día
    device = device_raw.groupby(['user', 'day']).agg(
        usb_activity_count=('id', 'count')
        ).reset_index()

    # =========================================================================
    # 3. ENSAMBLAJE TEMPORAL (OUTER JOINS SECUENCIALES)
    # =========================================================================
    print("Ensamblando el puzzle temporal (Outer Joins)[...]")
    # Outer join preserva TODAS las combinaciones usuario-dia existentes en cualquier fuente
    # Evita pérdida temprana de registros antes de la imputación
    master = pd.merge(logon, http, on=['user', 'day'], how='outer')
    master = pd.merge(master, email, on=['user', 'day'], how='outer')
    master = pd.merge(master, file_act, on=['user', 'day'], how='outer')
    master = pd.merge(master, device, on=['user', 'day'], how='outer')

    # =========================================================================
    # 4. LIMPIEZA DE VACIOS (POLITICA DE IMPUTACION M3.2)
    # =========================================================================
    print("Limpiando valores nulos[...]")
    # Variables de conteo: NaN = ausencia de actividad observada → imputamos 0
    fill_zero_cols = ['total_logon_activity', 'after_hours_activity', 'http_activity_count', 
                      'total_emails', 'file_activity_count', 'usb_activity_count']
    
    for col in fill_zero_cols:
        if col in master.columns:
            master[col] = master[col].fillna(0)
     
    # Variable continua de sentimiento: NaN = sin correos ese día → imputamos 0.0 (neutralidad operativa)
    if 'avg_sentiment' in master.columns:
        master['avg_sentiment'] = master['avg_sentiment'].fillna(0.0)

     # =========================================================================
    # 5. CAPA DE PERFIL ESTATICO (PSICOMETRIA BIG FIVE)
    # =========================================================================
    print("Añadiendo perfiles psicológicos [...]")
    psycho = pd.read_parquet(os.path.join(PROCESSED_DIR, 'psychometric.parquet'))
    
    # Homologacion de llaves: unificamos 'user_id' → 'user' para merge seguro
    if 'user_id' in psycho.columns:
        psycho = psycho.rename(columns={'user_id': 'user'})
    
    #  Privacidad por diseño: eliminamos nombre real, mantenemos solo ID anonimo
    #  para evitar riesgos de reidentificacion en la matriz maestra
    if 'employee_name' in psycho.columns:
        psycho = psycho.drop(columns=['employee_name'])
        
    # Left join: preserva todos los registros diarios, añade rasgos donde exista coincidencia
    master = pd.merge(master, psycho, on='user', how='left')

     # =========================================================================
    # 6. CONTEXTO ORGANIZACIONAL (LDAP - SNAPSHOT MÁS RECIENTE)
    # =========================================================================
    print("Añadiendo contexto corporativo (LDAP) [...]")
    ldap_path = os.path.join(RAW_DIR, 'ldap.csv') # Snapshot de mayo-2011
    
    if os.path.exists(ldap_path):
        ldap = pd.read_csv(ldap_path)
        
        # Homologacion de llaves
        if 'user_id' in ldap.columns:
            ldap = ldap.rename(columns={'user_id': 'user'})
            
        # Seleccion de columnas de contexto relevantes para el modelo de riesgo
        columnas_ldap = ['user', 'role', 'department', 'functional_unit']
        columnas_ldap = [c for c in columnas_ldap if c in ldap.columns]
        
        # Deduplicacion: conservamos el ultimo estado conocido por usuario (mas reciente)
        ldap_unico = ldap.drop_duplicates(subset=['user'], keep='last')[columnas_ldap]
        
        # Left join para enriquecer sin alterar la granularidad usuario-día
        master = pd.merge(master, ldap_unico, on='user', how='left')
    else:
        print(f"[AVISO] No se encontró el archivo '{ldap_path}'. Copiar un mes de LDAP a la carpeta 'raw' y llamarlo 'ldap.csv'.")

    # =========================================================================
    # 8. PERSISTENCIA DEL MONOLITO
    # =========================================================================
    print("Ordenando eventos longitudinalmente [user, day]...")
    # Ordenar es critico para ventanas moviles (shift) y cálculo de Z-Scores intrausuario en M3.3
    master = master.sort_values(by=['user', 'day']).reset_index(drop=True)

    # 8. Guardar el monolito
    master.to_parquet(MASTER_FILE, engine='pyarrow', index=False)
    end_time = time.time()

    print("\n*** MATRIZ MAESTRA COMPLETADA ***")
    print(f"Tiempo de fusión: {end_time - start_time:.2f} segundos.")
    print(f"Dimensiones finales: {master.shape[0]} filas x {master.shape[1]} columnas.")
    print(f"Archivo definitivo guardado en: {MASTER_FILE}")

if __name__ == "__main__":
    build_master_matrix()

# NOTA METODOLÓGICA: Adoptamos el snapshot final como "estado organizativo vigente"
# para evitar introducir ruido de reestructuraciones historicas en la deteccion de anomalias.
# La evolucion temporal de cargos queda fuera del alcance operativo de M3.2/M3.4.