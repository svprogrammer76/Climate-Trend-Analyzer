"""Write a concise text summary while retaining the synthetic-data caveat."""

from pathlib import Path
import json
import pandas as pd


def write_report(trend: dict, annual: pd.DataFrame, anomalies: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    anomaly_count = int(anomalies["any_anomaly"].sum())
    report = {
        "data_status": "SIMULATED educational data; not observed climate records",
        "annual_years": trend["years"],
        "temperature_trend_c_per_decade": round(trend["slope_c_per_decade"], 3),
        "temperature_trend_r_squared": round(trend["r_squared"], 3),
        "flagged_days": anomaly_count,
        "first_year_mean_temperature_c": round(float(annual.iloc[0].temperature_mean_c), 2),
        "last_year_mean_temperature_c": round(float(annual.iloc[-1].temperature_mean_c), 2),
        "interpretation": "The fitted trend describes this simulation only. It is not evidence about the real climate.",
    }
    path = output_dir / "summary.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path

