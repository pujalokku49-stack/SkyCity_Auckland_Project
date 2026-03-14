import streamlit as st
import pandas as pd
import plotly.express as px
st.title("🍕 Cuisine & Segment Channel Patterns")
df = st.session_state.get("filtered_data")

if df is None:
   st.warning("Please run the dashboard from main page.")
   st.stop()

# --------------------
# Cuisine Channel Usage
# --------------------
st.subheader("Delivery Channels by Cuisine")
cuisine_channel = df.groupby("CuisineType")[[
    "UberEatsOrders",
    "DoorDashOrders",
    "SelfDeliveryOrders"
]].sum().reset_index()

fig = px.bar(
  cuisine_channel,
  x="CuisineType",
  y=[
      "UberEatsOrders",
      "DoorDashOrders",
      "SelfDeliveryOrders"
  ],
  barmode="group",
  title="Delivery Channel Distribution by Cuisine"
)

st.plotly_chart(fig, use_container_width=True)
# -------------------------
# Segment Comparison
# ---------------------
st.subheader("Channel Usage by Business Segment")

segment_channel = df.groupby("Segment")[[
         "InStoreOrders",
         "UberEatsOrders",
         "DoorDashOrders",
         "SelfDeliveryOrders"
]].sum().reset_index()

fig2 = px.bar(
    segment_channel,
    x="Segment",
    y=[
         "InStoreOrders",
         "UberEatsOrders",
         "DoorDashOrders",
         "SelfDeliveryOrders"
    ],
    title ="Channel Mix by Segment"
)

st.plotly_chart(fig2, use_container_width=True)
