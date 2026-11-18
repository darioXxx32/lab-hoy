# 👶 Evaluador de Riesgo de Desnutrición Infantil (Ecuador)

Sistema de inteligencia artificial clínica y comunitaria para la predicción temprana de alerta de desnutrición infantil en infantes de Ecuador, basado en encuestas nacionales de salud y nutrición (ENSANUT) y estándares de crecimiento de la OMS.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue?logo=github)](https://darioXxx32.github.io/lab-hoy/)

---

## 🚀 Despliegue en Streamlit Community Cloud

Para desplegar la aplicación en la nube gratuita de Streamlit:

1. Ve a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"New app"** (o "Create app").
3. Configura los parámetros:
   * **Repository:** `darioXxx32/lab-hoy`
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Haz clic en **"Deploy!"**. 
   * Streamlit leerá automáticamente `requirements.txt` e instalará las dependencias necesarias.
   * En 1 minuto tendrás tu enlace público funcionando (ejemplo: `https://lab-hoy-xxxxx.streamlit.app`).

---

## 🌐 Despliegue en GitHub Pages

Para habilitar la versión web estática alojada directamente en GitHub:

1. En tu repositorio de GitHub, dirígete a **Settings** > **Pages** (en el menú lateral izquierdo).
2. En **Build and deployment** > **Source**, selecciona **Deploy from a branch**.
3. En **Branch**, elige `main` y en la carpeta selecciona `/(root)`.
4. Haz clic en **Save**.
5. En unos minutos estará accesible en:
   ```
   https://darioXxx32.github.io/lab-hoy/
   ```

---

## 💻 Ejecución Local

Para probar la aplicación en tu computadora:

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación Streamlit:**
   ```bash
   streamlit run app.py
   ```

---

## 📁 Estructura del Repositorio

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| **`app.py`** | Aplicación web interactiva principal en Streamlit. |
| **`requirements.txt`** | Lista de librerías para el despliegue automático en Streamlit Community Cloud. |
| **`modelo_desnutricion.joblib`** | Modelo predictivo empaquetado (`HistGradientBoostingClassifier` + preprocesador grupal). |
| **`model_metadata.json`** | Metadatos, umbrales y tablas de referencia para inferencia web. |
| **`index.html`** | Aplicación web interactiva autónoma para GitHub Pages (sin necesidad de servidor). |
| **`practica_desnutricion_infantil.ipynb`** | Cuaderno de análisis exploratorio (EDA), entrenamiento y exportación. |
| **`.streamlit/config.toml`** | Configuración de tema visual para Streamlit Cloud. |
| **`.gitignore`** | Exclusión de archivos temporales y caches. |
