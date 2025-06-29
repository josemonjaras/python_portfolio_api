import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="API Financiera - Simulación", layout="centered")

# --- Cargar datos ---


@st.cache_data
def load_data():
    df = pd.read_excel("data/healthcare_dataset.xlsx", engine="openpyxl")
    df.columns = [c.strip() for c in df.columns]
    df["Date of Admission"] = pd.to_datetime(
        df["Date of Admission"], dayfirst=True, errors="coerce")
    df["Discharge Date"] = pd.to_datetime(
        df["Discharge Date"], dayfirst=True, errors="coerce")
    df["Length of Stay"] = (df["Discharge Date"] -
                            df["Date of Admission"]).dt.days
    return df


df = load_data()

st.title("📊 API de Datos Financieros (Simulación con Streamlit)")
st.markdown(
    "Consulta de indicadores financieros hospitalarios a partir del dataset clínico.")

# --- Filtros simulando parámetros API ---
col1, col2 = st.columns(2)

with col1:
    hospital = st.selectbox(
        "🏥 Hospital", ["Todos"] + sorted(df["Hospital"].dropna().unique().tolist()))
with col2:
    insurance = st.selectbox("🏦 Aseguradora", [
                             "Todos"] + sorted(df["Insurance Provider"].dropna().unique().tolist()))

# --- Lógica "API" ---
filtered_df = df.copy()
if hospital != "Todos":
    filtered_df = filtered_df[filtered_df["Hospital"] == hospital]
if insurance != "Todos":
    filtered_df = filtered_df[filtered_df["Insurance Provider"] == insurance]

total_pacientes = len(filtered_df)
total_facturado = filtered_df["Billing Amount"].sum()
promedio_facturacion = filtered_df["Billing Amount"].mean()
promedio_estancia = filtered_df["Length of Stay"].mean()

# --- Simulación de respuesta API JSON ---
st.subheader("📦 Respuesta simulada del endpoint `/metrics`")

st.json({
    "filtros": {
        "hospital": hospital if hospital != "Todos" else None,
        "aseguradora": insurance if insurance != "Todos" else None
    },
    "resultados": {
        "total_pacientes": total_pacientes,
        "total_facturado": round(total_facturado, 2),
        "promedio_facturacion": round(promedio_facturacion, 2),
        "promedio_estancia_dias": round(promedio_estancia, 1)
    }
})

# --- Mostrar tabla filtrada si el usuario quiere ---
with st.expander("📋 Ver datos filtrados"):
    st.dataframe(filtered_df)
