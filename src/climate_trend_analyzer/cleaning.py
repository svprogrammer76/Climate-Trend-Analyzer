"""Input validation and reproducible preprocessing."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {"date", "temperature_c", "rainfall_mm", "humidity_pct"}


def clean_climate_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate columns/types, remove duplicate dates, and handle invalid values."""
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    result = data.copy()
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    for column in ("temperature_c", "rainfall_mm", "humidity_pct"):
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result = result.dropna(subset=["date"]).sort_values("date")
    result = result.drop_duplicates(subset=["date"], keep="first")
    result.loc[result["rainfall_mm"] < 0, "rainfall_mm"] = pd.NA
    result.loc[~result["humidity_pct"].between(0, 100), "humidity_pct"] = pd.NA
    for column in ("temperature_c", "rainfall_mm", "humidity_pct"):
        result[column] = result[column].interpolate(limit_direction="both")
    result = result.dropna(subset=["temperature_c", "rainfall_mm", "humidity_pct"])
    result["year"] = result["date"].dt.year
    result["month"] = result["date"].dt.month
    result["month_name"] = result["date"].dt.month_name()
    result["season"] = result["month"].map({12: "Winter", 1: "Winter", 2: "Winter",
                                             3: "Spring", 4: "Spring", 5: "Spring",
                                             6: "Summer", 7: "Summer", 8: "Summer",
                                             9: "Autumn", 10: "Autumn", 11: "Autumn"})
    return result.reset_index(drop=True)

