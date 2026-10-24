"""Save a compact set of publication-ready exploratory charts."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def create_figures(data: pd.DataFrame, annual: pd.DataFrame, anomalies: pd.DataFrame,
                   output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(annual["year"], annual["temperature_mean_c"], marker="o", ms=3, lw=1, color="#d95f02")
    ax.set(title="Annual mean temperature (synthetic series)", xlabel="Year", ylabel="°C")
    ax.grid(alpha=.25); fig.tight_layout()
    path = output_dir / "annual_temperature_trend.png"; fig.savefig(path, dpi=160); plt.close(fig); saved.append(path)

    monthly = data.groupby("month").agg(temperature_c=("temperature_c", "mean"), rainfall_mm=("rainfall_mm", "mean"))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(monthly.index, monthly.temperature_c, marker="o", color="#d95f02")
    axes[0].set(title="Average temperature by month", xlabel="Month", ylabel="°C", xticks=range(1, 13))
    axes[1].bar(monthly.index, monthly.rainfall_mm, color="#1b9e77")
    axes[1].set(title="Average daily rainfall by month", xlabel="Month", ylabel="mm/day", xticks=range(1, 13))
    fig.tight_layout(); path = output_dir / "seasonal_patterns.png"; fig.savefig(path, dpi=160); plt.close(fig); saved.append(path)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(data.date, data.rainfall_mm, lw=.45, color="#377eb8", label="Daily rainfall")
    points = anomalies[anomalies.rainfall_mm_anomaly]
    ax.scatter(points.date, points.rainfall_mm, s=17, color="#e41a1c", label="Rolling anomaly")
    ax.set(title="Rainfall and rolling anomaly flags (synthetic)", xlabel="Date", ylabel="mm/day")
    ax.legend(); ax.grid(alpha=.2); fig.tight_layout()
    path = output_dir / "rainfall_anomalies.png"; fig.savefig(path, dpi=160); plt.close(fig); saved.append(path)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(data.date, data.temperature_c, lw=.5, color="#999999", label="Daily temperature")
    points = anomalies[anomalies.temperature_c_anomaly]
    ax.scatter(points.date, points.temperature_c, s=18, color="#e41a1c", label="Rolling anomaly")
    ax.set(title="Temperature and rolling anomaly flags (synthetic)", xlabel="Date", ylabel="°C")
    ax.legend(); ax.grid(alpha=.2); fig.tight_layout()
    path = output_dir / "temperature_anomalies.png"; fig.savefig(path, dpi=160); plt.close(fig); saved.append(path)
    return saved

