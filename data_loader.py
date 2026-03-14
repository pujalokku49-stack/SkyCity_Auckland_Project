import pandas as pd
import streamlit as st
@st.cache_data

def load_data():
    df = pd.read_csv("skycity_data.csv")

    return df
