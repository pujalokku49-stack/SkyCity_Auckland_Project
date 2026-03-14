import streamlit as st
import pandas as pd
import plotly.express as px
st.title(" ⚠ Aggregator Dependency Risk Dashboard")
df = st.session_state.get("filtered_data")
if df is None:
   st.warning("Please open the main dashboard first.")
   st.stop()

# -----------------------
# Diversification Score
# ----------------------
st.subheader("Channel Diversification Distribution")
fig = px.histogram(
   df,
   x="DiversificationScore",
   nbins=20,
   title="Channel Diversification Score"
)
st.plotly_chart(fig, use_container_width=True)

#---------------------
# Risk Classification
# ---------------------
df["RiskCategory"] = df["AggregatorDependence"].apply(
    lambda x: "High Risk" if x >= 0.70
    else "Moderate Risk" if x >= 0.50
    else "Balanced"
)
risk_counts = df["RiskCategory"].value_counts().reset_index()
risk_counts.columns = ["Risk Level", "Restaurants"]

fig2 = px.bar(
     risk_counts,
     x="Risk Level",
     y="Restaurants",
     title="Restaurant Dependency Risk Levels"
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------
# High Risk Restaurants
# ---------------------------------------------
st.subheader("Restaurants with High Aggregator Dependency")
high_risk = df[df["AggregatorDependence"] >= 0.70]

st.dataframe(
    high_risk[[
        "RestaurantName",
        "Subregion",
        "CuisineType",
        "AggregatorDependence"
    ]].sort_values(by="AggregatorDependence", ascending=False)
)
