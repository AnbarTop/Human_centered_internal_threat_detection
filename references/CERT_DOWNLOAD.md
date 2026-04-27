# 📦 Descarga y Preparación del Dataset CERT r4.2

> **Nota importante:** Este repositorio no incluye datos *raw* ni procesados para mantener un tamaño ligero, cumplir con los términos de licencia del *dataset* y facilitar su publicación en GitHub.

---

## 🔗 1. Fuente oficial y requisitos de acceso

**Dataset (enlace directo de descarga:** [CERT Insider Threat Dataset r4.2 (CMU/SEI)](https://kilthub.cmu.edu/ndownloader/files/24856766)  

### Pasos para obtener el dataset:
1. Accede al enlace oficial de [Carnegie Mellon University](https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247/1)..
2. Descarga el [archivo comprimido](https://kilthub.cmu.edu/ndownloader/files/24856766): `cert_r4.2.zip` (~2.1 GB).
3. **Checksum de verificación (recomendado):**
   ```bash
   # Tras la descarga, verifica la integridad del archivo
   CHECKSUMS:
   - [CHECKSUMS-sha256](https://kilthub.cmu.edu/ndownloader/files/24857831)
   - [CHECKSUMS-sha1](https://kilthub.cmu.edu/ndownloader/files/24857837)
   # Valor esperado ([consultar en la página oficial](https://www.sei.cmu.edu/library/insider-threat-test-dataset/))
   ```

### ⚠️ Términos de uso clave:
- ✅ Uso exclusivo para investigación académica y educativa.
- ❌ Prohibida la redistribución del dataset raw en repositorios públicos.
- 🔐 Los resultados derivados deben anonimizarse antes de su publicación.

---

## 🗂️ 2. Estructura de directorios esperada

Descomprime el dataset y organiza los archivos según la siguiente estructura:

```text
src/data/
├── raw/
│   ├── logon.csv              # Eventos de autenticación
│   ├── device.csv             # Conexión de dispositivos USB
│   ├── file.csv               # Acceso/copias de archivos
│   ├── http.csv               # Navegación web (~14 GB)
│   ├── email.csv              # Correos corporativos (~1.3 GB)
│   ├── psychometric.csv       # Rasgos Big Five (OCEAN)
│   ├── ldap.csv               # Snapshot organizativo (ver paso 3)
│   └── LDAP/                  # Carpeta original con snapshots mensuales
│       ├── 2009-12.csv
│       ├── 2010-01.csv
│       └── ... (hasta 2011-05.csv)
└── processed/                 # Se genera automáticamente al ejecutar el pipeline
    ├── logon_daily_activity.parquet
    ├── http_daily_activity.parquet
    ├── email_daily_sentiment.parquet
    ├── file_daily_activity.parquet
    ├── device.parquet
    ├── psychometric.parquet
    └── master_behavioral_matrix.parquet
```

### 🛠️ Script de preparación rápida (opcional)
```bash
#!/bin/bash
# prepare_cert_data.sh - Organiza el dataset CERT r4.2 para este repositorio

RAW_DIR="src/data/raw"
mkdir -p "$RAW_DIR"

# Copiar archivos principales (ajusta la ruta de origen según tu descarga)
CERT_SOURCE="/ruta/a/cert_r4.2"

cp "$CERT_SOURCE/logon.csv" "$RAW_DIR/"
cp "$CERT_SOURCE/device.csv" "$RAW_DIR/"
cp "$CERT_SOURCE/file.csv" "$RAW_DIR/"
cp "$CERT_SOURCE/http.csv" "$RAW_DIR/"
cp "$CERT_SOURCE/email.csv" "$RAW_DIR/"
cp "$CERT_SOURCE/psychometric.csv" "$RAW_DIR/"

# Preparar LDAP: renombrar snapshot final para contexto vigente
cp "$CERT_SOURCE/LDAP/2011-05.csv" "$RAW_DIR/ldap.csv"

# Mantener carpeta LDAP completa para análisis histórico opcional
cp -r "$CERT_SOURCE/LDAP" "$RAW_DIR/"

echo "✅ Dataset preparado en $RAW_DIR"
echo "🔍 Verificando archivos..."
ls -lh "$RAW_DIR"/*.csv
```

---

## 🔄 3. Flujo de ejecución recomendado

Una vez preparados los datos, ejecuta el pipeline en este orden:

```bash
# 1. Activar entorno virtual
source .venv/bin/activate  # o conda activate tfm

# 2. Ejecutar scripts de ingesta (generan artefactos en processed/)
python src/01_ingesta_test_device.py
python src/02_ingesta_http.py
python src/03_ingesta_logon.py
python src/04_ingesta_email_nlp.py
python src/05_ingesta_file_psycho.py
python src/06_master_join.py

# 3. Ejecutar notebooks interactivos para feature engineering y modelado
jupyter lab notebooks/
# → 03_Ingenieria_Caracteristicas.ipynb
# → 04_Modelo_Deteccion.ipynb
```

> 💡 **Tip:** Los archivos `.parquet` generados en `processed/` están excluidos de Git por `.gitignore`. Para compartir resultados con colaboradores, comprime la carpeta `processed/` y compártela por canal seguro (no público).

---

## 🔐 4. Consideraciones éticas y de privacidad

Este trabajo se adhiere a los principios de **Privacy by Design** y **IA Responsable**:

| Principio | Implementación en este proyecto |
|-----------|--------------------------------|
| **Minimización de datos** | El NLP extrae únicamente un metadato numérico de sentimiento; no se almacena ni procesa contenido textual completo. |
| **No discriminación** | El análisis SHAP confirma que el modelo no discrimina por rasgos estáticos de personalidad (*Big Five*), sino por comportamientos dinámicos observables. |
| **Transparencia algorítmica** | La capa XAI (SHAP) garantiza el derecho a la explicación (RGPD Art. 13, AI Act). |
| **Supervisión humana** | Las alertas son indicadores de riesgo, no evidencia concluyente; requieren validación por analista humano. |
| **Finalidad académica** | *Dataset* sintético (CERT r4.2); cualquier uso aplicado requeriría EIPD/DPIA, consentimiento y supervisión de DPO. |

> 📜 **Marco normativo de referencia**: RGPD (UE) 2016/679, AI Act (UE) 2024/1689, Directiva NIS2.

---

## 📚 5. Recursos adicionales

### Documentación oficial del *dataset* y publicaciones:

- [Digital Library Search Results in Cybersecurity (CMU)](https://www.sei.cmu.edu/library/search/?q=insider+threat+dataset&facet_sei_topic=Cybersecurity)

- [Discover research from Carnegie Mellon University | KiltHub](https://www.sei.cmu.edu/research/cert/datasets/insider-threat/)

### Bibliografía académica clave:

> *Nota: La bibliografía completa del TFM se encuentra en el [README.md](../README.md#-bibliografía) y en el capítulo 8 de la memoria. Aquí solo incluimos enlaces prácticos para la preparación de datos.*

- Glasser, J., & Lindauer, B. (2013). [Bridging the gap: A pragmatic approach to generating insider threat data](https://doi.org/10.1109/SPW.2013.37). IEEE Security and Privacy Workshops.
- Lindauer, B., et al. (2014). [Insider Threat Test Dataset (CERT r4.2)](https://www.sei.cmu.edu/library/insider-threat-test-dataset/). Software Engineering Institute, CMU.

---

## ❓ Solución de problemas frecuentes

| Problema | Solución |
|----------|----------|
| `FileNotFoundError: logon.csv` | Verifica que estás ejecutando desde la raíz del proyecto o ajusta `BASE_DIR` en los scripts. |
| `MemoryError` al procesar `http.csv` | Asegúrate de que `CHUNK_SIZE` está definido en `02_ingesta_http.py` (valor recomendado: 1_000_000). |
| `KeyError: 'user_id'` en LDAP | Renombra `2011-05.csv` a `ldap.csv` y verifica que la columna `user_id` existe. |
| `nltk.download('vader_lexicon')` falla sin internet | Descarga manualmente el léxico y colócalo en `~/nltk_data/sentiment/`. |

---

> 📬 **¿Problemas con la preparación?** Abre un [Issue en GitHub](https://github.com/AnbarTop/Human_centered_internal_threat_detection/issues) con: (1) sistema operativo, (2) versión de Python, (3) mensaje de error completo.