# Descarga y Preparacion del Dataset CERT r4.2

Este repositorio no incluye datos raw ni procesados para mantener un tamano ligero y facilitar su publicacion en GitHub.

## 1) Fuente del dataset

Dataset: CERT Insider Threat Dataset r4.2 (CMU/SEI).

Debes obtenerlo desde la fuente oficial y respetar sus terminos de uso/licencia.

## 2) Estructura esperada local

Coloca los archivos en estas rutas locales:

- src/data/raw/logon.csv
- src/data/raw/device.csv
- src/data/raw/file.csv
- src/data/raw/http.csv
- src/data/raw/email.csv
- src/data/raw/psychometric.csv
- src/data/raw/ldap.csv
- src/data/raw/LDAP/*.csv

Los artefactos transformados se generan en:

- src/data/processed/

## 3) Nota de reproducibilidad

- Los archivos de src/data/raw y src/data/processed estan excluidos del control de versiones.
- Para reproducir resultados, ejecuta el flujo indicado en README y notebooks.

## 4) Nota etica

Este trabajo tiene fines academicos. Los resultados deben interpretarse como indicadores de riesgo y no como evidencia concluyente individual.
