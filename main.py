from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="🏥 API de Gestión Hospitalaria")

# CORS (permite uso desde otros dominios si se conecta frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar y limpiar datos
df = pd.read_excel("data/healthcare_dataset.xlsx", engine='openpyxl')
df.columns = df.columns.str.strip()
df["Date of Admission"] = pd.to_datetime(
    df["Date of Admission"], dayfirst=True, errors='coerce')
df["Discharge Date"] = pd.to_datetime(
    df["Discharge Date"], dayfirst=True, errors='coerce')

# Endpoints


@app.get("/")
def index():
    return {"message": "API de Indicadores de Salud — Bienvenido"}


@app.get("/patients/")
def all_patients(limit: int = 10):
    return df.head(limit).to_dict(orient="records")


@app.get("/conditions/{condition}")
def get_by_condition(condition: str):
    filtered = df[df["Medical Condition"].str.contains(
        condition, case=False, na=False)]
    return filtered.to_dict(orient="records")


@app.get("/medications/")
def medications_summary():
    return df["Medication"].value_counts().to_dict()


@app.get("/admissions/stats")
def admission_stats():
    avg_stay = (df["Discharge Date"] - df["Date of Admission"]).dt.days.mean()
    return {
        "total_admissions": len(df),
        "avg_stay_days": round(avg_stay, 2),
        "avg_billing_amount": round(df["Billing Amount"].mean(), 2)
    }


@app.get("/billing/by_insurance")
def billing_by_insurance():
    billing = df.groupby("Insurance Provider")[
        "Billing Amount"].mean().sort_values(ascending=False)
    return billing.round(2).to_dict()
