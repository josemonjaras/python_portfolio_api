# API REST — Indicadores de Salud

API construida con FastAPI para consultar y analizar datos médicos provenientes de un dataset hospitalario. Ideal para análisis clínico, costos y métricas administrativas.

## Endpoints principales

- `/`: Bienvenida
- `/patients/`: Lista de pacientes (parámetro opcional `limit`)
- `/conditions/{condition}`: Filtra por condición médica (ej: `/conditions/diabetes`)
- `/medications/`: Conteo de medicamentos usados
- `/admissions/stats`: Promedios de estadía y facturación
- `/billing/by_insurance`: Facturación promedio por aseguradora

## 🛠️ Uso local

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
