"""Create reproducible, explicitly synthetic daily climate-like observations."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_synthetic_climate(
    start: str = "2000-01-01",
    end: str = "2024-12-31",
    seed: int = 42,
) -> pd.DataFrame:
    """Generate a fictional temperate-region series; values are not observations.

    Temperature includes a seasonal cycle, a small linear drift, and noise.
    Rainfall is a nonnegative seasonal process. A few extreme events are added
    so the anomaly workflow can be demonstrated.
    """
    dates = pd.date_range(start=start, end=end, freq="D")
    if dates.empty:
        raise ValueError("The date range is empty; check start and end.")

    rng = np.random.default_rng(seed)
    day = dates.dayofyear.to_numpy()
    year_offset = (dates.year.to_numpy() - dates.year.min()).astype(float)
    seasonal = np.sin(2 * np.pi * (day - 100) / 365.25)
    temperature = 15 + 10 * seasonal + 0.035 * year_offset + rng.normal(0, 2.1, len(dates))
    wet_season = 1 + 0.45 * np.cos(2 * np.pi * (day - 210) / 365.25)
    rain_probability = np.clip(0.34 * wet_season, 0.08, 0.75)
    rainfall = np.where(rng.random(len(dates)) < rain_probability,
                        rng.gamma(shape=1.8, scale=5.0, size=len(dates)), 0.0)
    humidity = np.clip(62 + 16 * np.cos(2 * np.pi * (day - 215) / 365.25)
                       + rng.normal(0, 7, len(dates)), 15, 100)

    # Deterministic synthetic extremes, separated by several days.
    if len(dates) > 100:
        event_indices = np.linspace(70, len(dates) - 20, min(12, len(dates) // 400), dtype=int)
        for index in event_indices:
            temperature[index] += 12
            rainfall[index + 3] += 85

    return pd.DataFrame({
        "date": dates,
        "region": "Example Temperate Region (synthetic)",
        "temperature_c": np.round(temperature, 2),
        "rainfall_mm": np.round(rainfall, 2),
        "humidity_pct": np.round(humidity, 1),
    })

