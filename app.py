import streamlit as st
from streamlit_option_menu import option_menu
from src.plots import rating_category_plot, ratings_city_plot, results_plot
from src.data_utils import df
from src.recommender import recommend_similar_cities
from src.variables import VARIABLE_DESCRIPTIONS, RATING_COLUMNS, REGIONS, MONTHS, LIKED_CITIES, QUESTIONS
from src.quiz import compute_result
from src.images import city_images
from src.theme import local_css, quiz_city_card_html, likes_city_card_html

# TODO: maybe add a pdf download option, maybe add option to remove city from likes, maybe make a city gallery, comment code

st.set_page_config(page_title="Where to Next?", layout="centered", initial_sidebar_state="expanded")

local_css()

with st.sidebar:
    selected = option_menu(
        menu_title="Menu",  
        options=["Home", "Explore Ratings", "City Recommender", "Find Destination", "Liked Cities"],
        icons=["house", "bar-chart", "compass", "map", "heart"],  
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#222473", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "#333",
            },
            "nav-link-selected": {
                "background-color": "#222473",
                "color": "white",
                "font-weight": "bold",
            },
        }
    )

if selected == "Home":
    st.session_state.page = "Home"
elif selected == "Explore Ratings":
    st.session_state.page = "Plots"
elif selected == "City Recommender":
    st.session_state.page = "Recommender"
elif selected == "Find Destination":
    st.session_state.page = "Destination"
elif selected == "Liked Cities":
    st.session_state.page = "Liked"
st.sidebar.markdown("""
<style>
footer {
    visibility: hidden;
}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: left;
    font-size: 13px;
    color: #999999;
    padding: 10px 0;
}
</style>

<div class="footer">
    |  Made with ❤️ by <b>Gabriela Simon - 75736A</b>  
</div>
""", unsafe_allow_html=True)

if st.session_state.page == "Home":
    st.title("🌎 Where to Next?")
    st.markdown("""
    <div class="content-card">
        <h3 style="margin-top:0;">Welcome Traveler! ✈️</h3>
        <p>This project aims to help you discover your next ideal travel destination based on your preferences and interests.</p>
        <p>Whether you're looking for <b>vibrant city life</b>, <b>serene nature spots</b>, or <b>cultural experiences</b>, we've got you covered!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("https://cdn.pixabay.com/photo/2017/06/05/11/01/airport-2373727_1280.jpg", use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="content-card">
        <h3>How to use this app:</h3>
        <p>Navigate through the app using the sidebar to explore different features:</p>
        <ul style="line-height: 1.8;">
            <li><b>🌟 Explore Cities by Ratings:</b> Visualize and filter cities based on various travel-related ratings.</li>
            <li><b>📍 City Recommender:</b> Select a city to get recommendations for similar cities.</li>
            <li><b>🗺️ Find your ideal destination:</b> Take the quiz to discover your perfect travel spot.</li>
            <li><b>❤️ Liked Cities:</b> Keep track of the cities you liked during your exploration.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    
elif st.session_state.page == "Recommender":
    st.title("📍 City Recommender")
    st.write("Choose a city you liked, and we'll suggest similar cities you might enjoy!")
    city_options = {
    f"{row['city']}, {row['country']}": row['city']
    for _, row in df.iterrows()
    }
    selected_label = st.selectbox("Choose a city you liked", sorted(city_options.keys()))
    city_choice = city_options[selected_label]
    city_choice_country = df[df["city"] == city_choice]["country"].values[0]
    city_choice_description = df[df["city"] == city_choice]["short_description"].values[0]
    city_choice_id = df[df["city"] == city_choice]["id"].values[0]
    if city_choice:
        st.write(f"### If you liked _{city_choice}, {city_choice_country}_ you might also like:")
        recs = recommend_similar_cities(df, city_choice)
        st.dataframe(recs)
        st.write(f"### City Ratings Overview for _{city_choice}, {city_choice_country}_")
        rating_columns_lower = [col.lower() for col in RATING_COLUMNS]
        fig = ratings_city_plot(df, rating_columns_lower, city_choice)
        st.plotly_chart(fig, use_container_width=True)
        if st.button("❤️ Like city", key=f"like_{city_choice}"):
            new_fav_city = {
                "id": city_choice_id,
                "city": city_choice,
                "country": city_choice_country,
                "description": city_choice_description
            }
            
            existing_ids = [item['id'] for item in LIKED_CITIES]
            
            if city_choice_id not in existing_ids:
                LIKED_CITIES.append(new_fav_city)
                st.success(f"You liked {city_choice}!")
            else:
                st.warning(f"{city_choice} is already in your favorites.")


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
            "### Select an option",
            options,
            index=None,  
            key=key
        )
        answers[key] = question["mapping"].get(answer, None)
        st.markdown("---")
    if "results_df" not in st.session_state:
        st.session_state.results_df = None
    click = st.button("Get Recommendations")
    if click or st.session_state.results_df is not None:
        if click:
            if any(answer is None for answer in answers.values()):
                st.error("⚠️ Please answer all questions before continuing.")
                st.stop() 
            else:
                st.session_state.results_df = compute_result(answers)
                
        computed_results = st.session_state.results_df
        
        if computed_results is not None:
            st.write("### Based on your answers, we recommend you the following cities:")
            
            if computed_results.empty:
                st.write("😔 Unfortunately, no cities match your preferences.")
            else:
                for i, row in computed_results.head(5).iterrows():
                    if answers["month"] is not None:
                        month = answers['month'] - 1
                        month = MONTHS[month]
                    card_html = quiz_city_card_html(row, month)
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    image_url = city_images.get(row["id"])
                    if image_url:
                        st.image(image_url, use_container_width=True)
                    else:
                        st.info("No image available for this city.")
                
                    
                    if st.button("❤️ Like city", key=f"like_{row['city']}"):
                        new_fav_city = {
                            "id": row["id"],
                            "city": row["city"],
                            "country": row["country"],
                            "description": row["short_description"]
                        }
                        
                        existing_ids = [item['id'] for item in LIKED_CITIES]

                        if row["id"] not in existing_ids:
                            LIKED_CITIES.append(new_fav_city)
                            st.success(f"You liked {row['city']}!")
                        else:
                            st.warning(f"{row['city']} is already in your favorites.")
                    st.markdown("---")

                st.write("### Top 5 Recommended Cities on the Map")
                fig = results_plot(computed_results.head(5))
                st.plotly_chart(fig, use_container_width=True)
                

elif st.session_state.page == "Plots":
    st.title("🌟 Explore Cities by Ratings")
    st.markdown("Explore cities around the world and find your next travel destination!")

    values = [1, 2, 3, 4, 5]

    category = st.selectbox("Select a category", RATING_COLUMNS)
    st.write(f"**{category}:** {VARIABLE_DESCRIPTIONS[category.lower()]}")
    category = category.lower()
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

if st.session_state.page == "Liked":
    st.title("❤️ Liked Cities")
    if LIKED_CITIES:
        st.write("Here are your liked cities:")
        for city in LIKED_CITIES:
            card_html = likes_city_card_html(city)
            st.markdown(card_html, unsafe_allow_html=True)
            image_url = city_images.get(city['id'])
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.info("No image available for this city.")
            st.write("---")
            
    else:
        st.write("You haven't liked any cities yet.")