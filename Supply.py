import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# --------------------------
# Mock Data Setup
# --------------------------
st.title("Global Manufacturing Optimization under Trade Scenarios")

st.sidebar.header("Scenario Selection")
scenario = st.sidebar.selectbox("Choose a Trade Scenario", [
    "All out trade war (1930s style)",
    "All against the USA",
    "NAFTA vs the world",
    "US-China decouple (Cold War style)",
    "Trade war ends with a whimper",
    "Negotiations take most tariffs to zero"
])

st.sidebar.header("Adjustable Parameters")
custom_tariff = st.sidebar.slider("Tariff Multiplier (0 = Free Trade, 3 = High Tariff)", 0.0, 3.0, 1.0, 0.1)

st.subheader("Upload Manufacturing Data")
uploaded_file = st.file_uploader("Upload CSV with columns: Location, Production_Cost, Freight_Cost_to_Market, Tariff (Base) ")

# --------------------------
# Helper Function
# --------------------------
def optimize_location(data):
    # Total cost = production + freight + adjusted tariff
    data["Adjusted_Tariff"] = data["Tariff (Base)"] * custom_tariff
    data["Total_Cost"] = data["Production_Cost"] + data["Freight_Cost_to_Market"] + data["Adjusted_Tariff"]
    best_row = data.loc[data['Total_Cost'].idxmin()]
    return best_row, data

# --------------------------
# Run Optimization
# --------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if all(col in df.columns for col in ["Location", "Production_Cost", "Freight_Cost_to_Market", "Tariff (Base)"]):
        st.write("### Input Data", df)
        best_option, evaluated_data = optimize_location(df)

        st.write("### Cost Evaluation Table")
        st.dataframe(evaluated_data)

        st.success(f"Best Manufacturing Location under '{scenario}' Scenario: {best_option['Location']}")
        st.metric("Total Cost", f"${best_option['Total_Cost']:.2f}")
    else:
        st.error("CSV is missing required columns.")
else:
    st.info("Please upload the manufacturing dataset to continue.")

st.markdown("---")
st.markdown("Developed by AI & geopolitics nerds. Inspired by Richard Baldwin's global trade scenarios.")
