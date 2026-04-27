# 🛡️ TFM: Detección Conductual de Amenaza Interna (CERT r4.2)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19435851.svg)](https://doi.org/10.5281/zenodo.19435851)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/Kamaranis/Internal-Threat-Detection-Ensemble-CPIR)

> **Trabajo Final de Máster en Ciencia de Datos**  
> **Universitat Oberta de Catalunya (UOC)**  
> **Autor:** Antonio Barrera Mora  
> **Director:** Blas Torregrosa García | **Directora PRA:** Esther Ibáñez  
> **Fecha de entrega:** 7 de abril de 2026  
> **Área:** NLP, Ciberseguridad y Visual Analytics (A2. NPL&VA)

---

## 📋 Resumen Ejecutivo

Este proyecto desarrolla un sistema híbrido de detección temprana de **amenaza interna** (*Insider Threat*) que integra:

| Dimensión | Fuentes | Variables Clave |
|-----------|---------|----------------|
| **Técnica** | `logon`, `http`, `usb`, `file` | Volumetría, horarios, actividad fuera de jornada |
| **Conductual** | `email` (NLP) | Deriva afectiva (`sentiment_z_user`), ventanas móviles |
| **Contextual** | `psychometric`, `ldap` | Big Five (OCEAN), rol, departamento (snapshot) |

**Resultados clave** (validación sobre CERT r4.2, 330k registros, 191 insiders confirmados):

| Modelo | AUC | Recall @ Top-0.5% | Insiders detectados |
|--------|-----|-------------------|---------------------|
| Isolation Forest (baseline) | **0.629** | 4.71% | 9 / 191 |
| Autoencoder (Deep Learning) | 0.551 | **11.52%** | 22 / 191 |
| **Ensemble (votación lógica)** | — | **12.57%** | **24 / 191** ✅ |

> 🔍 **Hallazgo principal**: La integración de señales técnicas y conductuales permite anticipar la amenaza interna investigando únicamente el **0.5% de la actividad corporativa diaria**, reduciendo drásticamente la fatiga de alertas operativa.

---

## 🎥 Demostración Interactiva

🔗 **[Internal Threat Detection Ensemble - CPIR (Hugging Face Space)](https://huggingface.co/spaces/Kamaranis/Internal-Threat-Detection-Ensemble-CPIR)**

Prueba el sistema en tiempo real:
- Altera variables conductuales (actividad, sentimiento, horarios)
- Observa el recálculo del Índice de Riesgo (0-100)
- Visualiza la explicación SHAP (Waterfall Plot) para auditoría forense

---

## 🎯 Objetivos del Trabajo

### Objetivo Principal
Desarrollar un modelo analítico de detección de anomalías que integre variables técnicas de TI con indicadores conductuales extraídos mediante NLP, para anticipar cambios de comportamiento de riesgo en entornos corporativos.

### Objetivos Secundarios
1. ✅ Estructurar datos heterogéneos de CERT r4.2 en una matriz de perfiles usuario-día.
2. ✅ Aplicar NLP (VADER) para extraer métricas de sentimiento y deriva afectiva.
3. ✅ Entrenar y comparar algoritmos no supervisados (Isolation Forest, Autoencoder) en contexto de desbalanceo extremo (1:1730).
4. ✅ Implementar capa XAI (SHAP) para traducir decisiones matemáticas en evidencia criminológica trazable.

---

## ❓ Preguntas de Investigación

### Pregunta General (PIG)
> ¿Es posible anticipar incidentes de amenaza interna mediante modelos no supervisados sobre una matriz conductual híbrida (técnica + psicológica)?

**Respuesta empírica**: ✅ **Sí**. El sistema detectó 24 atacantes reales (Recall 12.57%) investigando solo el 0.5% de la actividad.

### Preguntas Específicas (PIE)

| PIE | Pregunta | Respuesta Empírica |
|-----|----------|-------------------|
| **PIE 1** | ¿Mejora la deriva afectiva (`sentiment_z_user`) la capacidad predictiva? | ✅ **Sí, como confirmador**. El sentimiento no es predictor primario, pero contextualiza la anomalía técnica (SHAP ≈ −0.42). |
| **PIE 2** | ¿Qué Recall alcanzan modelos no supervisados sin sobremuestreo? | ✅ **12.57% @ Top-0.5%**. Métrica operativamente relevante frente al AUC global en desbalanceo extremo. |
| **PIE 3** | ¿Contribuye el Ensemble a maximizar la detección? | ✅ **Sí**. Complementariedad táctica: IF detecta anomalías volumétricas; AE captura desviaciones sutiles multidimensionales. |
| **PIE 4** | ¿Valida XAI las premisas del modelo CPIR? | ✅ **Sí**. SHAP mapea variables técnicas con fases CPIR ("preparación activa", "explotación") y confirma que los rasgos Big Five tienen contribución marginal (garantía ética). |

---

## 🗂️ Estructura del Repositorio

```text
.
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias Python
├── notebooks/
│   ├── 01_Exploracion.ipynb          # EDA inicial y validación de fuentes
│   ├── 02_Ingesta_Procesamiento.ipynb# Arquitectura ETL y matriz maestra
│   ├── 03_Ingenieria_Caracteristicas.ipynb # Feature engineering + shortlist
│   └── 04_Modelo_Deteccion.ipynb     # Modelado, evaluación y XAI
├── src/
│   ├── 01_ingesta_test_device.py     # Prueba de concepto CSV→Parquet
│   ├── 02_ingesta_http.py            # Procesamiento HTTP por chunks
│   ├── 03_ingesta_logon.py           # Agregación diaria de logon + after-hours
│   ├── 04_ingesta_email_nlp.py       # NLP VADER + agregación sentimiento
│   ├── 05_ingesta_file_psycho.py     # File + Psychometric processing
│   ├── 06_master_join.py             # Integración final: matriz maestra
│   └── check_setup.py                # Verificación de entorno
├── references/
│   ├── CERT_DOWNLOAD.md              # Instrucciones para obtener el dataset
│   └── dataset_structure.md          # Descripción estructural de CERT r4.2
├── models/                           # Modelos serializados (no versionados en Git)
│   ├── isolation_forest_v1.pkl
│   ├── autoencoder_v1.keras
│   └── scaler_v1.pkl
└── .gitignore                        # Excluye datos raw/processed y modelos
```

⚠️ Nota sobre datos: Los directorios `src/data/raw/` y `src/data/processed/` están excluidos por .gitignore. Debes preparar el dataset localmente siguiendo references/CERT_DOWNLOAD.md.