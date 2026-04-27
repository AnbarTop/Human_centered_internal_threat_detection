# TFM Insider Threat Detection (CERT r4.2)

Proyecto de Trabajo Fin de Master (UOC, Ciencia de Datos) orientado a la deteccion temprana de riesgo interno (insider threat) con un enfoque hibrido:

- senales tecnicas de actividad digital,
- senales conductuales y emocionales en texto,
- contexto psicometrico y organizacional.

El objetivo es academico: validar una metodologia reproducible y explicable para anticipar cambios de comportamiento de riesgo en entornos corporativos.

## Video de presentacion (YouTube)

- Enlace del video: PENDIENTE_DE_PUBLICACION

## 1. Objetivos del trabajo

### 1.1 Objetivo principal

Desarrollar un modelo analitico de deteccion de anomalias para identificar amenazas internas corporativas, integrando variables tecnicas de sistemas de informacion con indicadores conductuales extraidos mediante analisis de sentimiento en comunicaciones organizacionales.

### 1.2 Objetivos secundarios

1. Preprocesar y estructurar datos heterogeneos y multivariantes de CERT r4.2 (logon, device, http, email y file) para construir una matriz de perfiles de actividad por usuario.
2. Aplicar tecnicas NLP para generar caracteristicas psicologicas cuantificables a partir del contenido de email.
3. Entrenar y comparar algoritmos no supervisados de deteccion de anomalias en contexto de desbalanceo extremo.
4. Evaluar el rendimiento del sistema mediante metricas y analisis forense de casos de estudio contrastados con la ground truth del dataset.

## 2. Preguntas de investigacion

### 2.1 Pregunta de investigacion general (PIG)

Es posible anticipar y detectar incidentes de amenaza interna en un entorno corporativo mediante modelos de aprendizaje no supervisado sobre una matriz conductual que integre volumetria tecnica y deriva psicologica?

### 2.2 Preguntas de investigacion especificas (PIE)

1. En que medida la cuantificacion de deriva conductual (por ejemplo `sentiment_z_user` y ventanas moviles por usuario) mejora la capacidad predictiva frente a un enfoque puramente volumetrico?
2. Que nivel de eficacia operativa (AUC y recall a nivel usuario) pueden alcanzar modelos no supervisados ante desbalanceo extremo, sin recurrir a sobremuestreo sintetico?
3. Como contribuye la combinacion de paradigmas (Isolation Forest y Autoencoder en estrategia de fuego cruzado) a incrementar la captura de insiders sin aumentar de forma descontrolada la fatiga de alertas?
4. Es posible traducir las decisiones de los modelos a evidencia operativa trazable mediante XAI (SHAP), de forma coherente con el marco CPIR?

## 3. Alineacion con los notebooks del proyecto

1. `01_Exploracion.ipynb`: validacion de cobertura de fuentes, temporalidad y consistencia de datos base.
2. `02_Ingesta_Procesamiento.ipynb`: arquitectura por capas, transformaciones por fuente, reglas de integracion y control de calidad.
3. `03_Ingenieria_Caracteristicas.ipynb`: construccion de variables de sentimiento, z-scores conductuales, variables temporales y shortlist para modelado.
4. `04_Modelo_Deteccion.ipynb`: modelado no supervisado (Isolation Forest y Autoencoder), evaluacion (AUC/Recall), estrategia ensemble y explicabilidad con SHAP.

## 4. Dataset

Se utiliza CERT Insider Threat Dataset r4.2 (CMU/SEI), simulacion de 1000 empleados durante 17 meses.

Politica de datos de este repositorio:

- No se versionan datos raw ni procesados en GitHub.
- Debes descargar y preparar el dataset localmente.
- Instrucciones en references/CERT_DOWNLOAD.md.

## 5. Metodologia resumida

1. Ingesta y limpieza (normalizacion temporal, IDs, calidad de registros).
2. Ingenieria de caracteristicas por usuario y ventana temporal.
3. Extraccion NLP de senales emocionales en email.
4. Fusion de senales tecnicas y psico-conductuales.
5. Deteccion de anomalias con modelos no supervisados y comparativa entre paradigmas.
6. Evaluacion cuantitativa y analisis cualitativo de casos.

## 6. Estructura del repositorio

```text
.
├── README.md
├── requirements.txt
├── notebooks/
│   ├── 01_Exploracion.ipynb
│   ├── 02_Ingesta_Procesamiento.ipynb
│   ├── 03_Ingenieria_Caracteristicas.ipynb
│   └── 04_Modelo_Deteccion.ipynb
├── references/
│   ├── dataset_structure.md
│   └── CERT_DOWNLOAD.md
└── src/
    ├── 01_ingesta_test_device.py
    ├── 02_ingesta_http.py
    ├── 03_ingesta_logon.py
    ├── 04_ingesta_email_nlp.py
    ├── 05_ingesta_file_psycho.py
    ├── 06_master_join.py
    ├── check_setup.py
    └── data/
        ├── raw/
        └── processed/
```

## 7. Requisitos tecnicos

- Python 3.10+
- Entorno recomendado: conda o venv
- Dependencias en requirements.txt

## 8. Quickstart

```bash
git clone <URL_DEL_REPOSITORIO>
cd "TFM_Insider_Threat (trabajando)"

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python src/check_setup.py
```

## 9. Flujo recomendado de ejecucion

1. Preparar datos locales siguiendo references/CERT_DOWNLOAD.md.
2. Ejecutar notebooks/01_Exploracion.ipynb.
3. Revisar notebooks/02_Ingesta_Procesamiento.ipynb como guia metodologica.
4. Ejecutar notebooks/03_Ingenieria_Caracteristicas.ipynb.
5. Ejecutar notebooks/04_Modelo_Deteccion.ipynb.
6. Consolidar logica estable en scripts de src/.

## 10. Reproducibilidad

- Este repositorio versiona codigo, notebooks y documentacion.
- Los directorios src/data/raw y src/data/processed estan excluidos por .gitignore.
- Los resultados dependen de la version del dataset y del estado del entorno Python.

## 11. Estado actual

- Pipeline base de ingesta y fusion disponible en src/.
- Cuatro notebooks de trabajo preparados para el flujo completo.
- Artefactos generados para modelado: `master_behavioral_matrix.parquet`, `feature_matrix_v1.parquet` y `feature_shortlist_m34.csv` (en entorno local, no versionados).
- Documentacion de referencia en references/.

## 12. Consideraciones eticas y de uso

Este trabajo tiene finalidad academica y de investigacion.

- Los resultados son indicadores de riesgo, no evidencia concluyente individual.
- Cualquier uso aplicado requiere supervision humana y gobernanza.
- Para datos reales, se requiere base legal, minimizacion de datos y controles de auditoria.

## 13. Referencias del proyecto

- `references/CERT_DOWNLOAD.md`: preparacion local de dataset y estructura esperada.
- `references/dataset_structure.md`: descripcion estructural de las fuentes CERT.
- `src/01_ingesta_test_device.py` a `src/06_master_join.py`: pipeline de ingesta, transformacion e integracion.
- `src/check_setup.py`: verificacion de entorno.

## 14. Bibliografia

1. CERT Division, Carnegie Mellon University. Insider Threat Test Dataset r4.2.
2. Liu, F. T., Ting, K. M., Zhou, Z.-H. Isolation Forest. ICDM, 2008.
3. Le, D. C., Zincir-Heywood, A. N. Anomaly Detection for Insider Threats Using Unsupervised Ensembles. IEEE TNSM, 2021.
4. Lundberg, S. M., Lee, S.-I. A Unified Approach to Interpreting Model Predictions (SHAP). NeurIPS, 2017.
5. Chandola, V., Banerjee, A., Kumar, V. Anomaly Detection: A Survey. ACM Computing Surveys, 2009.

## 15. Siguientes pasos

1. Publicar el video en YouTube y actualizar el enlace en este README.
2. Estandarizar limpieza de outputs de notebooks antes de cada commit.
3. Definir metrica final de comparacion baseline (solo logs) vs enfoque hibrido.
