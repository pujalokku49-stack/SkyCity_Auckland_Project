import streamlit as st
import pandas as pd
import plotly.express as px
st.title("📊 Channel Market Performance")

df = st.session_state.get("filtered_data")

if df is None:
   st.warning("Please load the dashboard from the main page.")
   st.stop()

# -----------------------
# Channel Market share
# -------------------------
st.subheader("Channel Market Share")

channel_orders = {
      "In-Store": df["InStoreOrders"].sum(),
      "Uber Eats": df["UberEatsOrders"].sum(),
      "DoorDash": df["DoorDashOrders"].sum(),
      "Self Delivery": df["SelfDeliveryOrders"].sum()
}

share_df = pd.DataFrame({
      "Channel": list(channel_orders.keys()),
      "Orders": list(channel_orders.values())
})

fig = px.pie(
     share_df,
     names = "Channel",
     values = "Orders",
     title = "Overall Channel Order Share"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------
# Delivery vs In-Store
# --------------------
st.subheader("Delivery vs In-Store Orders")

delivery_orders = (
     df["UberEatsOrders"].sum() +
     df["DoorDashOrders"].sum() +
     df["SelfDeliveryOrders"].sum()
)

instore_orders = df["InStoreOrders"].sum()

dominance_df = pd.DataFrame({
        "Category": ["In-Store", "Delivery"],
        "Orders": [instore_orders, delivery_orders]
})

fig2 = px.bar(
     dominance_df,
     x="Category",
     y="Orders",
     title="Delivery vs In-Store Dominance"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Net Profit Comparison
# --------------------------
st.subheader("Net Profit by Channel")

profit_df = pd.DataFrame({
      "Channel": ["In-Store", "Uber Eats", "DoorDash", "Self Delivery"],
      "Net Profit": [
           df["InStoreNetProfit"].sum(),
           df["UberEatsNetProfit"].sum(),
           df["DoorDashNetProfit"].sum(),
           df["SelfDeliveryNetProfit"].sum(),
      ]
})

fig3 = px.bar(
     profit_df,
     x = "Channel",
     y = "Net Profit",
     title = "Channel Profitability Comparison"
)

st.plotly_chart(fig3, use_container_width=True)
