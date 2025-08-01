# ⚡ Forecasting Power Consumption Peaks in Europe

Full-stack ML system for real-time energy demand forecasting across 20+ European countries.

This project combines data engineering, predictive modeling, and backend API development:

    🔁 ETL pipeline with Prefect 2, collecting hourly demand data via the ENTSO-E API.

    🌦️ Enriched with temperature and calendar features (weekends, holidays).

    🤖 LightGBM regression model trained to predict short-term consumption peaks.

    🧠 FastAPI-powered REST API serving real-time predictions.

    🗃️ Data stored in Parquet format, organized by country and month.

    🧪 Fully testable, modular, and production-ready architecture.

    Tech Stack: Python, Prefect, DuckDB, FastAPI, LightGBM, Pandas, Docker.


> **Elevator pitch**: Predict and alert hourly demand peaks across 30+ European countries using open datasets (ENTSO‑E, OPSD, Ember) combined with weather variables and LSTM/GBM models. Includes a full ETL pipeline, interactive dashboard, and REST API.

---

## 🖥 Live Demo

| Component           | URL (prod) | Screenshot |
| -------------------|------------|------------|
| Streamlit dashboard| *pending*  | *pending*  |
| REST API /docs     | *pending*  | *pending*  |
| Notebook tour      | *pending*  | *pending*  |

---

## 🗺 Architecture
```
┌──────────────┐   API keys   ┌──────────────────┐
│  GitHub CI   │────────────▶│  Docker Image     │
└──────────────┘              │   FastAPI + ML   │
      ▲                       └─────────┬────────┘
      │ push                         expose 443
┌─────┴────────┐  trigger    ┌──────────▼────────┐       ┌──────────────┐
│  ETL Pipeline ├───────────▶│ PostgreSQL/DuckDB │◀──────┤ Dash/Stream  │
│  (Prefect)    │            └──────────┬────────┘       └──────────────┘
└──────────────┘ ingest hourly  ▲
                              │ features
                        ┌─────▼─────┐
                        │  ML model │
                        └───────────┘
```

---

## 📦 Repository Structure
```
.
├── data/               # raw and processed files
├── notebooks/          # exploration and prototypes
├── src/
│   ├── etl/            # Prefect / Dask jobs
│   ├── features/       # feature engineering
│   ├── models/         # training and prediction
│   ├── api/            # FastAPI endpoints
│   └── dashboard/      # Dash/Streamlit components
├── tests/              # pytest
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.template
└── .github/
    └── workflows/ci.yml
```

---

## 🚀 Quick start
```bash
# 1. clone the repo
$ git clone https://github.com/<your-user>/eu-power-peaks.git
$ cd eu-power-peaks

# 2. create the environment
$ python -m venv .venv && source .venv/bin/activate

# 3. install dependencies
$ pip install -r requirements.txt

# 4. configure credentials
$ cp .env.template .env  # add your ENTSOE_API_KEY, etc.

# 5. run local pipeline
$ make etl

# 6. launch dashboard and API
$ make up   # docker-compose up -d
```

---

## 📈 ETL & Feature Store
- **Prefect 2** or **Airflow** DAG calling the `entsoe-py` clients, downloading monthly batches by country, stored partitioned in DuckDB.
- Enrichment with weather variables from **Renewables.ninja** and ERA5 via `cdsapi`.
- Persistence in **PostgreSQL** for OLAP and **Parquet** for ML usage.

---

## 🤖 Modeling
- **Baseline**: SARIMAX with exogenous regressors (temperature, calendars).
- **ML**: Gradient Boosting (LightGBM) and multivariate **LSTM** (Keras) using a sliding window.
- **Metrics**: MAPE and RMSE by country-hour.

---

## 📊 Dashboard
- **Streamlit** for quick overview and **Dash** for corporate-level drill-down.
- Switch by country, timeframe, and temperature, with traffic-light style alerts.

---

## 🔔 Alerts
Webhook (Slack / Teams) triggered when forecast > 95th percentile of historical series or > regulatory threshold.

---

## 🛠 CI/CD
- **GitHub Actions**: linting, tests, Docker build, deployment to Render/Heroku.
- **pre-commit**: black, isort, flake8.

---

## 📝 License
ALL RIGHTS RESERVED © <JesusECB-2025>

---

## 🤝 Contact
[LinkedIn](https://www.linkedin.com/in/your-profile) | [email](mailto:your@email)

