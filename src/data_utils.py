import pandas as pd
import streamlit as st

@st.cache_data
def load_data(csv):
    """
    Loads the CSV data and caches it to prevent reloading on every interaction.
    Cleans column names to ensure consistency.
    """
    df = pd.read_csv(csv)
    # Standardize headers: lowercase and remove leading/trailing spaces
    df.columns = df.columns.str.lower().str.strip()
    return df
