"""Command-line entry point. Run with: python main.py"""

from pathlib import Path
from climate_trend_analyzer.pipeline import run_pipeline


def main() -> None:
    root = Path(__file__).resolve().parent
    result = run_pipeline(root)
    trend = result["trend"]
    print("Climate Trend Analyzer finished (SIMULATED DATA)")
    print(f"Rows processed: {result['rows']:,}")
    print(f"Descriptive temperature slope: {trend['slope_c_per_decade']:.3f} °C/decade")
    print(f"Trend R²: {trend['r_squared']:.3f}")
    print(f"Flagged days: {result['anomaly_days']:,}")
    print(f"Report: {result['report']}")
    print("Figures:")
    for figure in result["figures"]:
        print(f"  {figure}")
    print("Reminder: results describe the simulation only; do not present them as observed climate findings.")


if __name__ == "__main__":
    main()

