import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🐱‍👓 Subregion Channel Perference")

df = st.session_state.get("filtered_data")

if df is None:
   st.warning("Please run the main dashboard first.")
   st.stop()

subregion_channel = df.groupby("Subregion")[[
    "InStoreOrders",
    "UberEatsOrders",
    "DoorDashOrders",
    "SelfDeliveryOrders"
]].sum().reset_index()

melted = subregion_channel.melt(
      id_vars = "Subregion",
      var_name = "Channel",
      value_name = "Orders"
)

fig = px.density_heatmap(
    melted,
    x="Channel",
    y="Subregion",
    z="Orders",
    color_continuous_scale="Blues",
    title="Channel Dominance Across Subregions"
)

st.plotly_chart(fig, use_container_width=True)
