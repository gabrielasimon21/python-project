import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pycountry
from src.plots import rating_category_plot, rating_category_plot_test
from src.data_utils import load_data

st.set_page_config(page_title="Where to Next?", layout="centered", initial_sidebar_state="expanded")

csv = "data/worldwide-travel-cities.csv"

df = load_data(csv)

if "page" not in st.session_state:
    st.session_state.page = "Home"
    
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Find your ideal destination"):
    st.session_state.page = "Destination"
if st.sidebar.button("Plots"):
    st.session_state.page = "Plots"

if st.session_state.page == "Home":
    st.title("Home Page 🏠")
    st.write("Welcome to the home page!")

elif st.session_state.page == "Destination":
    st.title("🗺️ Find your ideal destination!")
    st.write("Take this quick quiz and discover where should you should go for your next vacation!")
    st.markdown("----")
    st.write("Reply to the questions with your preferences.")   
    budget = st.radio('Question 1', ('Budget', 'Luxury', 'Idk'))
    longness = st.radio('Question 2', ('quick', 'long', 'etc'))
    st.write("This is the budget: ", budget)
    
    
elif st.session_state.page == "Plots":
    st.title("🌍 Where to Next?")
    st.markdown("Explore cities around the world and find your next travel destination!")


    rating_columns = ["Culture", "Adventure", "Nature", "Beaches", "Nightlife", "Cuisine", "Wellness", "Urban", "Seclusion"]
    regions = ["World", "Europe", "Asia", "Africa", "North America", "South America", "Oceania"]
    values = [1, 2, 3, 4, 5]

    category = st.selectbox("Select a category", rating_columns)
    category = category.lower()
    region_selection = st.selectbox("Select a region", regions)
    region_selection = region_selection.lower()
    
    st.write("**Filter by rating:**")
    cols = st.columns(5)  

    selected_ranks = []
    for i, rating in enumerate(range(1, 6)):
        with cols[i]:
            if st.checkbox(f"{rating} ⭐", value=True, key=f"rating_{rating}"):
                selected_ranks.append(rating)
    st.subheader(f"Cities rankings for {category.title()}")
    
    filtered_df = df[df[category].isin(selected_ranks)]

    fig = rating_category_plot(filtered_df, category, region_selection)

    st.plotly_chart(fig, use_container_width=True)

