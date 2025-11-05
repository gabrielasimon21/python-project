import streamlit as st
from src.plots import rating_category_plot, ratings_city_plot
from src.data_utils import df
from src.recommender import recommend_similar_cities
import pandas as pd
import plotly.express as px 

from src.variables import VARIABLE_DESCRIPTIONS, RATING_COLUMNS, REGIONS 
from src.quiz import QUESTIONS, compute_result


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
        st.write(f"### If you liked _{city_choice}, {city_choice_country}_ you might also like:")
        recs = recommend_similar_cities(df, city_choice)
        st.dataframe(recs)
        st.write(f"### City Ratings Overview for _{city_choice}, {city_choice_country}_")
        rating_columns_lower = [col.lower() for col in RATING_COLUMNS]
        fig = ratings_city_plot(df, rating_columns_lower, city_choice)
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "Destination":
    st.title("🗺️ Find your ideal destination!")
    st.write("Take this quick quiz and discover where should you should go for your next vacation!")
    st.markdown("----")
    st.write("Reply to the questions with your preferences.")
    answers = {}
    for key, question in QUESTIONS.items():
        st.markdown(f"### {question['text']}")
        options = question["options"]
        answer = st.radio(
            f"### Select an option",
            options,
            index=None,  
            key=key
        )
        answers[key] = question["mapping"].get(answer, None)
        st.markdown("---")
    if st.button("Get Recommendations"):
        if any(answer is None for answer in answers.values()):
            st.error("⚠️ Please answer all questions before continuing.")
        else:
            st.write(answers)
            st.write("### Based on your answers, we recommend you the following cities:")
            computed_results = compute_result(answers)
            if computed_results.empty:
                st.write("😔 Unfortunately, no cities match your preferences. Please try adjusting your answers.")
            else:
                st.dataframe(computed_results.reset_index(drop=True))

elif st.session_state.page == "Plots":
    st.title("🌟 Explore Cities by Ratings")
    st.markdown("Explore cities around the world and find your next travel destination!")

    values = [1, 2, 3, 4, 5]

    category = st.selectbox("Select a category", RATING_COLUMNS)
    category = category.lower()
    st.write(VARIABLE_DESCRIPTIONS[category])
    region_selection = st.selectbox("Select a region", REGIONS)
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

