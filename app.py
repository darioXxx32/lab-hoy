import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Configuración de página
st.set_page_config(
    page_title="Predicción de Desnutrición Infantil - Ecuador",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 1rem;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .alert-box-danger {
        background-color: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 10px;
        padding: 1.2rem;
        color: #991b1b;
        font-weight: 600;
    }
    .alert-box-success {
        background-color: #f0fdf4;
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 1.2rem;
        color: #166534;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_bundle():
    model_path = "modelo_desnutricion.joblib"
    if not os.path.exists(model_path):
        st.error(f"No se encontró el archivo del modelo '{model_path}'. Por favor ejecuta primero el notebook para exportarlo.")
        return None
    return joblib.load(model_path)

bundle = load_model_bundle()

st.markdown('<div class="main-title">👶 Evaluador de Riesgo de Desnutrición Infantil</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Herramienta clínica y comunitaria para la predicción temprana de alerta de desnutrición infantil en Ecuador con Machine Learning</div>', unsafe_allow_html=True)

if bundle is None:
    st.stop()

model = bundle['model']
feature_cols = bundle['feature_cols']
edu_map = bundle['edu_map']
reg_map = bundle['reg_map']
global_stats = bundle['global_stats']
group_lookups = bundle['group_lookups']
default_threshold = bundle.get('threshold', 0.20)

# Sidebar - Parámetros y Configuración
st.sidebar.header("⚙️ Configuración del Modelo")
threshold = st.sidebar.slider(
    "Umbral de Decisión (Sensibilidad)",
    min_value=0.05,
    max_value=0.50,
    value=float(default_threshold),
    step=0.01,
    help="Umbrales más bajos aumentan la detección preventiva (mayor sensibilidad en salud pública)."
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**ℹ️ Sobre el Modelo:**
- **Algoritmo:** HistGradientBoosting Classifier
- **Entrenamiento:** ENSANUT / Encuesta Nacional Ecuador (70,000 registros)
- **Variables evaluadas:** Antropométricas (peso, talla, IMC, Z-scores) y sociodemográficas (región, educación materna).
""")

# Interfaz Principal - Formulario de Datos
col_form, col_results = st.columns([1.1, 1.2], gap="large")

with col_form:
    st.subheader("📋 Datos del Infante")
    
    c1, c2 = st.columns(2)
    with c1:
        edad_meses = st.number_input(
            "Edad (en meses):",
            min_value=-12,
            max_value=36,
            value=12,
            step=1,
            help="Valores negativos representan meses gestacionales previos al parto."
        )
    with c2:
        sexo = st.selectbox("Sexo biológico:", options=["M", "F"], format_func=lambda x: "Masculino (M)" if x == "M" else "Femenino (F)")
    
    c3, c4 = st.columns(2)
    with c3:
        region = st.selectbox(
            "Región del Ecuador:",
            options=["Sierra", "Costa", "Amazonia", "Insular"],
            index=0
        )
    with c4:
        educacion = st.selectbox(
            "Nivel educativo de la madre:",
            options=["Sin escolaridad", "Primaria", "Secundaria", "Superior"],
            index=2
        )
        
    c5, c6 = st.columns(2)
    with c5:
        peso_kg = st.number_input(
            "Peso actual (kg):",
            min_value=1.0,
            max_value=30.0,
            value=9.2,
            step=0.1,
            format="%.2f"
        )
    with c6:
        talla_cm = st.number_input(
            "Talla actual (cm):",
            min_value=35.0,
            max_value=115.0,
            value=74.5,
            step=0.5,
            format="%.1f"
        )

    # Cálculo inmediato de indicadores OMS
    talla_m = talla_cm / 100.0
    imc = peso_kg / (talla_m ** 2)
    ratio_w_h = peso_kg / talla_cm
    
    st.markdown("---")
    st.markdown("#### 📏 Indicadores Antropométricos Calculados")
    m1, m2, m3 = st.columns(3)
    m1.metric("IMC Pediátrico", f"{imc:.1f} kg/m²")
    m2.metric("Ratio Peso / Talla", f"{ratio_w_h:.3f}")
    m3.metric("Relación Talla/Edad", f"{(talla_cm / (max(0, edad_meses) + 1)):.1f} cm/mes")

with col_results:
    st.subheader("📊 Resultado de la Evaluación")
    
    # Preprocesamiento de entrada
    row = pd.DataFrame([{
        'edad_meses': edad_meses,
        'sexo': sexo,
        'region': region,
        'nivel_educacion_madre': educacion,
        'peso_kg': peso_kg,
        'talla_cm': talla_cm
    }])
    
    row['region'] = row['region'].apply(lambda x: 'Amazonia' if 'Amazon' in str(x) else x)
    row['edu_ord'] = row['nivel_educacion_madre'].map(edu_map).fillna(1)
    row['sexo_num'] = (row['sexo'] == 'M').astype(int)
    row['region_num'] = row['region'].map(reg_map).fillna(1)
    row['peso_isna'] = int(pd.isna(peso_kg))
    row['talla_isna'] = int(pd.isna(talla_cm))
    row['edad_is_neg'] = int(edad_meses < 0)
    row['edad_abs'] = abs(edad_meses)
    row['edad_pos'] = max(0, edad_meses)
    row['peso_clean'] = np.clip(peso_kg, 0, 25)
    row['talla_clean'] = np.clip(talla_cm, 35, 110)
    row['height_m'] = row['talla_clean'] / 100.0
    row['bmi'] = row['peso_clean'] / (row['height_m'] ** 2)
    row['w_h_ratio'] = row['peso_clean'] / (row['talla_clean'] + 1e-5)
    row['w_age_ratio'] = row['peso_clean'] / (row['edad_pos'] + 1.0)
    row['h_age_ratio'] = row['talla_clean'] / (row['edad_pos'] + 1.0)

    # Agregaciones grupales
    for grp_name, cfg in group_lookups.items():
        cols = cfg['cols']
        table = cfg['table']
        val_tuple = tuple(row[c].iloc[0] for c in cols)
        key = str(val_tuple[0]) if len(cols) == 1 else "_".join(str(x) for x in val_tuple)
        stats = table.get(key, {})
        for num_col in ['peso_clean', 'talla_clean', 'bmi']:
            mean_val = stats.get(f'{num_col}_mean', global_stats[f'{num_col}_mean'])
            std_val = stats.get(f'{num_col}_std', global_stats[f'{num_col}_std'])
            if np.isnan(std_val) or std_val <= 0:
                std_val = 1.0
            row[f'{num_col}_diff_{grp_name}'] = row[num_col] - mean_val
            row[f'{num_col}_z_{grp_name}'] = (row[num_col] - mean_val) / (std_val + 1e-5)

    # One hot
    for s in ['F', 'M']:
        row[f'sexo_{s}'] = int(sexo == s)
    for r in ['Amazonia', 'Costa', 'Insular', 'Sierra']:
        row[f'region_{r}'] = int(region == r)
    for e in ['Primaria', 'Secundaria', 'Sin escolaridad', 'Superior']:
        row[f'nivel_educacion_madre_{e}'] = int(educacion == e)

    X_input = row.reindex(columns=feature_cols, fill_value=0)
    
    # Predicción
    pred_prob = float(model.predict_proba(X_input)[0, 1])
    is_alert = pred_prob >= threshold

    # Visualización de probabilidad
    prob_percent = pred_prob * 100
    st.write(f"**Probabilidad Estimada de Riesgo:** `{prob_percent:.2f}%` (Umbral de Alerta: `{threshold * 100:.1f}%`)")
    st.progress(min(1.0, max(0.0, pred_prob)))

    if is_alert:
        st.markdown(f"""
        <div class="alert-box-danger">
            🚨 <strong>ALERTA DE DESNUTRICIÓN INFANTIL DETECTADA</strong><br>
            El modelo ha determinado un riesgo superior al umbral establecido ({prob_percent:.1f}% vs {threshold * 100:.1f}%). Se sugiere evaluación médica y seguimiento nutricional prioritario.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-box-success">
            ✅ <strong>SIN ALERTA INMEDIATA DE DESNUTRICIÓN</strong><br>
            El infante se encuentra dentro de los parámetros de desarrollo esperados según los datos sociodemográficos y antropométricos analizados ({prob_percent:.1f}% de riesgo).
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🩺 Recomendaciones Pediátricas y Nutricionales")
    if is_alert:
        st.warning("""
        - **Atención Primaria:** Agendar cita en el Centro de Salud más cercano para valoración pediátrica integral.
        - **Suplementación:** Verificar administración de hierro, vitamina A y micronutrientes según protocolo MSP Ecuador.
        - **Monitoreo:** Curva de crecimiento mensual (peso/edad y talla/edad).
        - **Alimentación:** Evaluar lactancia materna y densidad calórica-proteica de la alimentación complementaria.
        """)
    else:
        st.info("""
        - **Control Regular:** Continuar con los controles rutinarios de Niño Sano en el centro de salud.
        - **Dieta Equilibrada:** Fomentar consumo variado de frutas, verduras, legumbres y proteínas de alto valor biológico.
        - **Higiene:** Asegurar consumo de agua segura hervida o tratada para prevenir infecciones diarreicas.
        """)

st.markdown("---")
st.caption("Desarrollado para la Práctica de Inteligencia Artificial - Universidad / Proyecto Desnutrición Infantil Ecuador.")
