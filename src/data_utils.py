import pandas as pd
import streamlit as st

@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    df.columns = df.columns.str.lower().str.strip()
    return df

csv = "data/worldwide-travel-cities.csv"
df = load_data(csv)

def create_city_vectors(df, rating_columns):
    city_vectors = {}
    for _, row in df.iterrows():
        city = row["city"]
        vector = row[rating_columns].values.astype(float)
        city_vectors[city] = vector
    return city_vectors