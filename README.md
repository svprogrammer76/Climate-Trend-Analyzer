# Climate Trend Analyzer

> **Educational portfolio project.** The default workflow uses simulated data. Its results are not real-world climate findings and must not be used for policy, safety, or scientific conclusions.

A small, reproducible Python pipeline that generates climate-like daily data, validates and enriches it, summarizes annual and seasonal behavior, estimates a descriptive temperature trend, flags rolling-window outliers, and writes charts and machine-readable outputs.

## Why this project

Climate analysis turns long time series into summaries people can investigate: warming or cooling patterns, precipitation variability, seasonal differences, and unusual observations. Governments, research groups, utilities, agriculture, and city planners use observed climate records to inform adaptation and planning. This repository demonstrates the data workflow and communication skills behind that work; the synthetic example does not establish a real climate trend.

## What it does

1. Creates a reproducible daily time series with seasonal temperature, rainfall, humidity, gradual simulated warming, random variation, and injected extreme events.
2. Parses dates, checks required fields, drops duplicate dates, handles invalid values, and adds year/month/season fields.
3. Aggregates annual and seasonal summaries and fits a simple linear regression to annual mean temperature.
4. Uses a centered rolling z-score to flag unusually high or low temperature/rainfall relative to local variation.
5. Saves CSV summaries, anomaly rows, a JSON report, and PNG charts.

## Technology

Python 3.10+, pandas, NumPy, scikit-learn, Matplotlib, and optionally Streamlit. No GPU is required. The selected approach is deliberately beginner-friendly: a transparent linear trend and a transparent statistical anomaly rule before more complex forecasting.

## Architecture

```text
Synthetic generator -> cleaning/features -> annual + seasonal summaries
                                      -> rolling anomaly flags
                                      -> trend fit
                       summaries + flags + trend -> CSV / JSON / PNG
```

## Repository structure

```text
├── app/streamlit_app.py          # Optional interactive dashboard
├── data/raw/                     # Generated input CSV and data notes
├── data/processed/               # Cleaned data (generated; ignored by Git)
├── docs/                         # Project guide and detailed proof plan
├── images/                       # Screenshots and demo assets you capture
├── notebooks/                    # Optional exploratory notebooks
├── outputs/                      # Tables, JSON report, generated figures
├── src/climate_trend_analyzer/   # Reusable simulation and analysis modules
├── main.py                       # Pipeline command-line entry point
├── pyproject.toml
└── requirements.txt
```

## Setup

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal, then activate again. This applies only to the current process.

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Check setup with `python --version` and `python -c "import pandas, numpy, sklearn, matplotlib; print('Environment ready')"`.

## Run

```bash
python main.py
```

The first run creates `data/raw/synthetic_climate.csv`, `data/processed/climate_clean.csv`, `outputs/annual_summary.csv`, `outputs/seasonal_summary.csv`, `outputs/anomalies.csv`, `outputs/summary.json`, and charts in `outputs/figures/`. Reruns use the same default random seed and should reproduce the data.

Optional dashboard (after dependencies install):

```bash
streamlit run app/streamlit_app.py
```

## Data and interpretation

Default series spans 2000–2024 for a fictional temperate region. Fields are date, region label, daily temperature in °C, rainfall in mm, and relative humidity in percent. The generator's slow drift is an intentional teaching parameter, not an estimate. No CO₂ or sea-level data are included in this version. The simple trend is descriptive OLS on annual means; it does not account for autocorrelation, uncertainty, confounders, or attribution. The rolling z-score is an exploratory flag, not a validated extreme-event detector. Review `docs/PROJECT_GUIDE.md` before interpreting outputs.

For a real-data extension, choose a public dataset and document its exact source, license, location/station, units, time coverage, quality flags, and retrieval date. Keep observed and simulated runs separate and cite the source.

## Limitations and next steps

- Synthetic single-region data only; no observational source or validation.
- Annual OLS is an introductory summary, not a climate attribution model.
- Rolling z-scores can miss persistent shifts and behave poorly with strongly skewed rainfall.
- Forecasting, uncertainty intervals, spatial comparison, CO₂, and sea level are not implemented.

Possible extensions: load a documented public station dataset; add missingness and quality-control diagnostics; compare multiple regions; model precipitation occurrence and amounts separately; evaluate forecasts with time-based holdouts and a naive baseline; quantify uncertainty; add geospatial context; or explore environmental covariates. Keep conclusions proportional to evidence.

## Learning outcomes

Data validation, time-series feature engineering, group/resample operations, regression, anomaly rules, reproducible pipelines, plotting, CLI execution, and responsible communication of simulated versus observed data.

## Author

Shraddha Verma, B.Tech in Computer Science.


