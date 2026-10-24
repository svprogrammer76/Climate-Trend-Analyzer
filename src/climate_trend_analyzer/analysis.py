"""Trend summaries and transparent rolling-z-score anomaly flags."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def annual_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily values into annual means and precipitation totals."""
    return (data.set_index("date").resample("YE")
            .agg(temperature_mean_c=("temperature_c", "mean"),
                 rainfall_total_mm=("rainfall_mm", "sum"),
                 humidity_mean_pct=("humidity_pct", "mean"),
                 days_observed=("temperature_c", "count"))
            .rename_axis("year_end").reset_index()
            .assign(year=lambda frame: frame["year_end"].dt.year))


def linear_trend(annual: pd.DataFrame) -> dict[str, float]:
    """Fit a descriptive OLS line to annual mean temperature."""
    valid = annual.dropna(subset=["year", "temperature_mean_c"])
    if len(valid) < 2:
        raise ValueError("At least two years are required to estimate a trend.")
    model = LinearRegression().fit(valid[["year"]], valid["temperature_mean_c"])
    return {"slope_c_per_year": float(model.coef_[0]),
            "slope_c_per_decade": float(model.coef_[0] * 10),
            "intercept": float(model.intercept_),
            "r_squared": float(model.score(valid[["year"]], valid["temperature_mean_c"])),
            "years": int(len(valid))}


def flag_anomalies(data: pd.DataFrame, window: int = 31, threshold: float = 3.0) -> pd.DataFrame:
    """Flag values whose centered rolling z-score exceeds the threshold.

    This is an exploratory rule, not a climate attribution method. A rolling
    baseline helps account for the normal annual seasonal cycle.
    """
    if window < 3 or threshold <= 0:
        raise ValueError("window must be >= 3 and threshold must be positive.")
    result = data.copy()
    for column in ("temperature_c", "rainfall_mm"):
        baseline = result[column].rolling(window, center=True, min_periods=max(3, window // 2))
        mean = baseline.mean()
        std = baseline.std().replace(0, np.nan)
        result[f"{column}_rolling_z"] = (result[column] - mean) / std
        result[f"{column}_anomaly"] = result[f"{column}_rolling_z"].abs() >= threshold
    result["any_anomaly"] = result["temperature_c_anomaly"] | result["rainfall_mm_anomaly"]
    return result


def seasonal_summary(data: pd.DataFrame) -> pd.DataFrame:
    return (data.groupby("season", sort=False)
            .agg(temperature_mean_c=("temperature_c", "mean"),
                 rainfall_mean_mm=("rainfall_mm", "mean"),
                 humidity_mean_pct=("humidity_pct", "mean"),
                 observations=("date", "count")).reset_index())

