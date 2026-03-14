import pandas as pd
import streamlit as st
@st.cache_data

def load_data():
    df = pd.read_csv("data/SkyCity Auckland Restaurants & Bars.csv")

    return df
