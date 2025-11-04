import streamlit as st
from src.plots import rating_category_plot, ratings_city_plot
from src.data_utils import df
from src.recommender import recommend_similar_cities
import pandas as pd
import plotly.express as px 

from src.descriptions import variable_descriptions, rating_columns, regions 


st.set_page_config(page_title="Where to Next?", layout="centered", initial_sidebar_state="expanded")

if "page" not in st.session_state:
    st.session_state.page = "Home"
    
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Find your ideal destination"):
    st.session_state.page = "Destination"
if st.sidebar.button("Explore Cities by Ratings"):
    st.session_state.page = "Plots"
if st.sidebar.button("City Recommender"):
    st.session_state.page = "Recommender"

if st.session_state.page == "Home":
    st.title("Home Page 🏠")
    st.write("Welcome to the home page!")
 
elif st.session_state.page == "Recommender":
    st.title("📍 City Recommender")
    st.write("Choose a city you liked, and we'll suggest similar cities you might enjoy!")
    city_choice = st.selectbox("Choose a city you liked", sorted(df["city"].unique()))
    city_choice_country = df[df["city"] == city_choice]["country"].values[0]
    #category = st.selectbox("Choose a category", rating_columns)
    #category = category.lower()
    if city_choice:
        st.write(f"### If you liked _{city_choice}_, _{city_choice_country}_ you might also like:")
        recs = recommend_similar_cities(df, city_choice)
        st.dataframe(recs)
        st.subheader(f"City Ratings Overview for {city_choice}")
        rating_columns_lower = [col.lower() for col in rating_columns]
        fig = ratings_city_plot(df, rating_columns_lower, city_choice)
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "Destination":
    st.title("🗺️ Find your ideal destination!")
    st.write("Take this quick quiz and discover where should you should go for your next vacation!")
    st.markdown("----")
    st.write("Reply to the questions with your preferences.")   
    budget = st.radio('Question 1', ('Budget', 'Luxury', 'Idk'))
    longness = st.radio('Question 2', ('quick', 'long', 'etc'))
    st.write("This is the budget: ", budget)
    
    
elif st.session_state.page == "Plots":
    st.title("🌟 Explore Cities by Ratings")
    st.markdown("Explore cities around the world and find your next travel destination!")

    values = [1, 2, 3, 4, 5]

    category = st.selectbox("Select a category", rating_columns)
    category = category.lower()
    st.write(variable_descriptions[category])
    region_selection = st.selectbox("Select a region", regions)
    region_selection = region_selection.lower()
    
    st.write("#### **Filter by rating:**")
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

