# Evaluador de Riesgo de Desnutrición Infantil (Ecuador)

Sistema clínico y comunitario para la predicción temprana de alerta de desnutrición infantil en infantes de Ecuador, basado en encuestas nacionales de salud y nutrición (ENSANUT) y estándares de crecimiento de la Organización Mundial de la Salud (OMS).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue?logo=github)](https://darioXxx32.github.io/lab-hoy/)

---

## Despliegue en Streamlit Community Cloud

Para desplegar la aplicación en Streamlit Community Cloud:

1. Iniciar sesión en [share.streamlit.io](https://share.streamlit.io/) con la cuenta de GitHub.
2. Hacer clic en **"New app"**.
3. Seleccionar los parámetros del repositorio:
   * **Repository:** `darioXxx32/lab-hoy`
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Hacer clic en **"Deploy!"**.
   * Streamlit instalará las dependencias indicadas en `requirements.txt`.
   * El servicio generará la URL pública de la aplicación.

---

## Despliegue en GitHub Pages

Para habilitar la versión estática alojada en GitHub Pages:

1. En el repositorio de GitHub, ingresar a **Settings** > **Pages**.
2. En **Build and deployment** > **Source**, seleccionar **Deploy from a branch**.
3. En **Branch**, seleccionar `main` y en la carpeta elegir `/(root)`.
4. Hacer clic en **Save**.
5. La aplicación quedará disponible en:
   ```
   https://darioXxx32.github.io/lab-hoy/
   ```

---

## Ejecución Local

Para ejecutar la aplicación localmente:

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Iniciar Streamlit:**
   ```bash
   streamlit run app.py
   ```

---

## Estructura del Repositorio

| Archivo / Directorio | Descripción |
| :--- | :--- |
| **`app.py`** | Aplicación web interactiva en Streamlit. |
| **`requirements.txt`** | Dependencias para despliegue en Streamlit Community Cloud. |
| **`modelo_desnutricion.joblib`** | Modelo predictivo empaquetado (`HistGradientBoostingClassifier`). |
| **`model_metadata.json`** | Metadatos y tablas de referencia para inferencia web. |
| **`index.html`** | Aplicación web autónoma para GitHub Pages. |
| **`practica_desnutricion_infantil.ipynb`** | Cuaderno con el proceso de análisis exploratorio, entrenamiento y validación. |
| **`.streamlit/config.toml`** | Configuración de tema visual para el servidor Streamlit. |
| **`.gitignore`** | Exclusión de archivos temporales, binarios y cachés locales. |

---

## Autor

**Darío Pomasqui** - Lab 8 | Inteligencia Artificial

