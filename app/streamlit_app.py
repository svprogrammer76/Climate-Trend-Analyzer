"""Optional lightweight dashboard: streamlit run app/streamlit_app.py"""

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import pandas as pd
from climate_trend_analyzer.pipeline import run_pipeline

st.set_page_config(page_title="Climate Trend Analyzer", layout="wide")
st.title("Climate Trend Analyzer")
st.caption("Educational demonstration using simulated data only — not an observed climate record.")
if st.button("Generate and analyze the sample series"):
    with st.spinner("Generating simulated series and charts..."):
        result = run_pipeline(ROOT)
    annual = pd.read_csv(ROOT / "outputs" / "annual_summary.csv")
    trend = result["trend"]
    left, right = st.columns(2)
    left.metric("Simulated temperature trend", f"{trend['slope_c_per_decade']:.3f} °C / decade")
    right.metric("Flagged days", f"{result['anomaly_days']:,}")
    st.line_chart(annual.set_index("year")["temperature_mean_c"])
    st.image(str(ROOT / "outputs" / "figures" / "seasonal_patterns.png"))
    st.dataframe(pd.read_csv(ROOT / "outputs" / "anomalies.csv").head(100))
    st.info("The slope and anomaly count are properties of a fictional simulation, not climate evidence.")

