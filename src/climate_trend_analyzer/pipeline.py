"""Orchestrate simulation, cleaning, analysis, plots, and report outputs."""

from pathlib import Path
import pandas as pd
from .simulation import generate_synthetic_climate
from .cleaning import clean_climate_data
from .analysis import annual_summary, linear_trend, flag_anomalies, seasonal_summary
from .visualization import create_figures
from .report import write_report


def run_pipeline(project_root: Path, start: str = "2000-01-01", end: str = "2024-12-31", seed: int = 42) -> dict:
    data_dir = project_root / "data"
    output_dir = project_root / "outputs"
    (data_dir / "raw").mkdir(parents=True, exist_ok=True)
    (data_dir / "processed").mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = generate_synthetic_climate(start=start, end=end, seed=seed)
    raw_path = data_dir / "raw" / "synthetic_climate.csv"
    raw.to_csv(raw_path, index=False)

    clean = clean_climate_data(raw)
    annual = annual_summary(clean)
    seasonal = seasonal_summary(clean)
    anomalies = flag_anomalies(clean)
    clean.to_csv(data_dir / "processed" / "climate_clean.csv", index=False)
    annual.to_csv(output_dir / "annual_summary.csv", index=False)
    seasonal.to_csv(output_dir / "seasonal_summary.csv", index=False)
    anomalies.loc[anomalies.any_anomaly].to_csv(output_dir / "anomalies.csv", index=False)
    trend = linear_trend(annual)
    figures = create_figures(clean, annual, anomalies, output_dir / "figures")
    report_path = write_report(trend, annual, anomalies, output_dir)
    return {"rows": len(clean), "trend": trend, "anomaly_days": int(anomalies.any_anomaly.sum()),
            "raw_csv": raw_path, "report": report_path, "figures": figures}

