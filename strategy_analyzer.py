import streamlit as st
import pandas as pd
import numpy as np

# --- Fake Data Generation ---
np.random.seed(42)

manufacturing_locations = ["Factory A (Spain)", "Factory B (USA)", "Factory C (China)"]
market_locations = ["Market X (Europe)", "Market Y (North America)", "Market Z (Asia)"]
products = ["Lipstick", "Foundation", "Eyeshadow"]

# Production Capacity (units per month)
production_capacity = pd.DataFrame({
    "Location": manufacturing_locations,
    "Lipstick": np.random.randint(5000, 15000, size=len(manufacturing_locations)),
    "Foundation": np.random.randint(3000, 10000, size=len(manufacturing_locations)),
    "Eyeshadow": np.random.randint(7000, 18000, size=len(manufacturing_locations)),
}).set_index("Location")

# Cost of Goods Sold (COGS) per unit
cogs = pd.DataFrame({
    "Location": manufacturing_locations,
    "Lipstick": np.random.uniform(2, 5, size=len(manufacturing_locations)),
    "Foundation": np.random.uniform(4, 8, size=len(manufacturing_locations)),
    "Eyeshadow": np.random.uniform(3, 6, size=len(manufacturing_locations)),
}).set_index("Location")

# Demand Forecast (units per month)
demand = pd.DataFrame({
    "Market": market_locations,
    "Lipstick": np.random.randint(4000, 12000, size=len(market_locations)),
    "Foundation": np.random.randint(2500, 9000, size=len(market_locations)),
    "Eyeshadow": np.random.randint(6000, 16000, size=len(market_locations)),
}).set_index("Market")

# Selling Price per unit
selling_price = pd.DataFrame({
    "Market": market_locations,
    "Lipstick": np.random.uniform(8, 15, size=len(market_locations)),
    "Foundation": np.random.uniform(12, 20, size=len(market_locations)),
    "Eyeshadow": np.random.uniform(10, 18, size=len(market_locations)),
}).set_index("Market")

# Initial Tariff Matrix (%)
tariff_data = {}
for man_loc in manufacturing_locations:
    tariff_data[man_loc] = {}
    for market_loc in market_locations:
        tariff_data[man_loc][market_loc] = np.random.randint(0, 15)

tariffs = pd.DataFrame(tariff_data)

# --- Streamlit UI ---
st.title("Cosmetic Company Strategy Analyzer")
st.subheader("Scenario Planning for Profit Maximization")

# Scenario Selection
scenario_name = st.text_input("Enter Scenario Name:", "Base Scenario")

st.sidebar.header("Data Input")

with st.sidebar.expander("Manufacturing Data", expanded=False):
    st.subheader("Manufacturing Capacity")
    st.dataframe(production_capacity)
    st.subheader("Cost of Goods Sold (COGS)")
    st.dataframe(cogs)

with st.sidebar.expander("Market Data", expanded=False):
    st.subheader("Demand Forecast")
    st.dataframe(demand)
    st.subheader("Selling Price")
    st.dataframe(selling_price)

with st.sidebar.expander(f"Trade Tariffs ({scenario_name})", expanded=True):
    st.subheader("Tariff Percentages (%)")
    edited_tariffs = st.data_editor(tariffs)

# --- Calculation Logic ---
def calculate_profit(production_plan, cogs_df, selling_price_df, tariff_df):
    total_profit = 0
    detailed_results = []

    for man_loc in production_plan.index:
        for market_loc in production_plan.columns:
            for product in products:
                units_exported = production_plan.loc[man_loc, market_loc].get(product, 0)
                if units_exported > 0:
                    unit_cogs = cogs_df.loc[man_loc, product]
                    unit_price = selling_price_df.loc[market_loc, product]
                    tariff_rate = tariff_df.loc[man_loc, market_loc] / 100
                    tariff_cost_per_unit = unit_cogs * tariff_rate  # Applying tariff to COGS (can be adjusted)
                    total_cost_per_unit = unit_cogs + tariff_cost_per_unit
                    profit_per_unit = unit_price - total_cost_per_unit
                    product_profit = units_exported * profit_per_unit

                    total_profit += product_profit
                    detailed_results.append({
                        "Manufacturing Location": man_loc,
                        "Market Location": market_loc,
                        "Product": product,
                        "Units Exported": units_exported,
                        "COGS per Unit": unit_cogs,
                        "Selling Price per Unit": unit_price,
                        "Tariff (%)": tariff_rate * 100,
                        "Tariff Cost per Unit": tariff_cost_per_unit,
                        "Total Cost per Unit": total_cost_per_unit,
                        "Profit per Unit": profit_per_unit,
                        "Product Profit": product_profit,
                    })
    return total_profit, pd.DataFrame(detailed_results)

def find_best_strategy(capacity_df, demand_df, cogs_df, selling_price_df, tariff_df):
    # This is a simplified mockup and doesn't implement a full optimization algorithm.
    # In a real application, you would use linear programming or other optimization techniques.

    best_profit = -np.inf
    best_plan = None
    all_plans = []

    # Create a basic production plan DataFrame initialized to 0
    initial_plan = pd.DataFrame(
        index=manufacturing_locations,
        columns=market_locations
    )
    for man_loc in manufacturing_locations:
        for market_loc in market_locations:
            initial_plan.loc[man_loc, market_loc] = {}
            for prod in products:
                initial_plan.loc[man_loc, market_loc][prod] = 0
    all_plans.append(initial_plan.copy())

    # --- Very basic (and not optimal) allocation logic for the mockup ---
    current_plan = initial_plan.copy()
    for product in products:
        remaining_demand = demand_df[product].copy()
        available_capacity = capacity_df[product].copy()

        for man_loc in manufacturing_locations:
            for market_loc in market_locations:
                if remaining_demand[market_loc] > 0 and available_capacity[man_loc] > 0:
                    shipment_size = min(remaining_demand[market_loc], available_capacity[man_loc], 2000) # Limit for mockup
                    if shipment_size > 0:
                        current_plan.loc[man_loc, market_loc][product] = shipment_size
                        remaining_demand[market_loc] -= shipment_size
                        available_capacity[man_loc] -= shipment_size

    profit, details = calculate_profit(current_plan, cogs_df, selling_price_df, tariff_df)
    if profit > best_profit:
        best_profit = profit
        best_plan = current_plan
        best_details = details

    return best_plan, best_profit, best_details

# --- Run Analysis ---
if st.button("Analyze Strategy"):
    with st.spinner("Analyzing..."):
        best_production_plan, max_profit, detailed_results_df = find_best_strategy(
            production_capacity, demand, cogs, selling_price, edited_tariffs
        )

        st.subheader(f"Best Strategy for Scenario: {scenario_name}")
        if best_production_plan is not None:
            st.write("Optimal Production and Export Plan:")
            st.dataframe(best_production_plan)
            st.metric("Maximum Estimated Profit", f"${max_profit:,.2f}")

            if not detailed_results_df.empty:
                st.subheader("Detailed Profit Breakdown")
                st.dataframe(detailed_results_df)
            else:
                st.warning("No profitable export routes found under the current scenario.")
        else:
            st.warning("Could not determine a profitable strategy with the current data.")
