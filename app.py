import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.validation import validate_order_totals, validate_channel_share
from utils.kpi_calculator import(
   calculate_dependency_index,
   calculate_diversification_score,
   calculate_channel_market_share
)

st.set_page_config(
    page_title="SkyCity Channel Intelligence",
    layout="wide",
    page_icon="📊"
)

st.markdown("""
<style>
.main-title {
    font-size:32px;
    font-weight:700;
    color: #1f2937;
}
.section-header {
    font-size:22px;
    font-weight:600;
    margin-top:20px;
}
.kpi-box {
    background-color:#f3f4f6;
    padding:18px;
    border-radius:10px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Order Channel Performance and Market Share Analytics for SkyCity Auckland Restaurants & Bars</div>', unsafe_allow_html=True)
st.caption("Unified Mentor x SkyCity Auckland | Hospitality Market Intelligence Dashboard")


@st.cache_data
def load_and_prepare():
    df = load_data()
    df = validate_order_totals(df)
    df = validate_channel_share(df)
    df = calculate_dependency_index(df)
    df = calculate_diversification_score(df)
    return df

df = load_and_prepare()

st.sidebar.header(" 🔎 Global Filters")

subregion_filter = st.sidebar.multiselect(
    "Subregion",
    sorted(df["Subregion"].unique()),
    default=sorted(df["Subregion"].unique())
)

cuisine_filter = st.sidebar.multiselect(
    "Cuisine Type",
    sorted(df["CuisineType"].unique()),
    default=sorted(df["CuisineType"].unique())
)
segment_filter = st.sidebar.multiselect(
    "Business Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

df_filtered = df[
    (df["Subregion"].isin(subregion_filter)) &
    (df["CuisineType"].isin(cuisine_filter)) &
    (df["Segment"].isin(segment_filter))
]

st.session_state["filtered_data"] = df_filtered

st.markdown('<div class="section-header">Executive KPIs</div>', unsafe_allow_html=True)
total_orders = df_filtered["MonthlyOrders"].sum()
total_restaurants = df_filtered["RestaurantID"].nunique()
avg_aov = df_filtered["AOV"].mean()

shares = calculate_channel_market_share(df_filtered)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Monthly Orders", f"{total_orders:,}")
col2.metric("Active Restaurants", total_restaurants)
col3.metric("Average Order Value", f"${avg_aov:.2f}")
col4.metric("In-Store Share", f"{shares['InStore']:.2%}")

st.markdown('<div class="section-header">Delivery vs In-Store Dominance</div>', unsafe_allow_html=True)

delivery_orders = (
     df_filtered["UberEatsOrders"].sum() +
     df_filtered["DoorDashOrders"].sum() +
     df_filtered["SelfDeliveryOrders"].sum()
)

instore_orders = df_filtered["InStoreOrders"].sum()

dominance_df = pd.DataFrame({
    "Category": ["In-Store", "Delivery"],
    "Orders": [instore_orders, delivery_orders]
})

fig_dom = px.bar(
   dominance_df,
   x="Category",
   y="Orders",
   title="Order Volume Comparison"
)

st.plotly_chart(fig_dom, use_container_width=True)

st.markdown('<div class="section-header"> Net Profit by Channel</div>', unsafe_allow_html=True)

profit_df = pd.DataFrame({
    "Channel": ["In-Store", "Uber Eats", "DoorDash", "Self Delivery"],
    "Net Profit": [
        df_filtered["InStoreNetProfit"].sum(),
        df_filtered["UberEatsNetProfit"].sum(),
        df_filtered["DoorDashNetProfit"].sum(),
        df_filtered["SelfDeliveryNetProfit"].sum(),
    ]
})

fig_profit = px.bar(
    profit_df,
    x="Channel",
    y="Net Profit",
    title="Channel-Level Net Profit Comparison"
)

st.plotly_chart(fig_profit, use_container_width=True)

st.markdown('<div class="section-header">Channel Diversification Distribution</div', unsafe_allow_html=True)

fig_div = px.histogram(
    df_filtered,
    x="DiversificationScore",
    nbins=20,
    title="Diversification Score Distribution"
)

st.plotly_chart(fig_div, use_container_width=True)

st.markdown('<div class="section-header">Aggregator Dependency Risk</div>', unsafe_allow_html=True)

df_filtered["RiskCategory"] = df_filtered["AggregatorDependence"].apply(
     lambda x: "High Risk" if x >= 0.70
     else "Moderate Risk" if x >= 0.50
     else "Balanced"
)

risk_counts = df_filtered["RiskCategory"].value_counts().reset_index()
risk_counts.columns = ["Risk Level", "Count"]

st.bar_chart(risk_counts.set_index("Risk Level"))

st.markdown('<div class="section-header"> Automated Executive InSights</div>', unsafe_allow_html=True)

top_channel = max(shares, key=shares.get)
avg_dependency = df_filtered["AggregatorDependence"].mean()

if avg_dependency >= 0.65:
    dependency_msg = "High aggregator dependence risk detected."
elif avg_dependency >= 0.50:
    dependency_msg = "Moderate aggregator exposure observed."
else:
    dependency_msg = "Healthy channel diversification observed."

insight_text = f"""
**Key Findings:**
- Dominant ordering channel: **{top_channel}**
- Average aggregator dependence: **{avg_dependency:.2%}**
- Risk Status: **{dependency_msg}**

**Strategic Recommendation:**
Strengthen direct channels (In-Store & Self-Delivery) to improve margin stability and reduce commission.
"""
st.success(insight_text)

st.divider()
st.caption("Unified Mentor | SkyCity Auckland Hospitality Analytics | Production Build")
