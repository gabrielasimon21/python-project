import pandas as pd
import streamlit as st

@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    df.columns = df.columns.str.lower().str.strip()
    return df
