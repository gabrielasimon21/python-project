import streamlit as st
from streamlit_option_menu import option_menu
from src.plots import rating_category_plot, ratings_city_plot, results_plot
from src.data_utils import load_data
from src.recommender import recommend_similar_cities
from src.variables import VARIABLE_DESCRIPTIONS, RATING_COLUMNS, REGIONS, MONTHS, QUESTIONS
from src.quiz import compute_result
from src.images import city_images
from src.theme import local_css, quiz_city_card_html, likes_city_card_html

# -- DATA LOADING --
# Load the dataset once; caching is handled inside load_data()
csv = "data/worldwide-travel-cities.csv"
df = load_data(csv)

# -- APP CONFIGURATION --
st.set_page_config(page_title="Where to Next?", layout="centered", initial_sidebar_state="expanded")

# Apply custom CSS for fonts, colors, and card styling
local_css()

# Initialize Session State for "Liked Cities"
# This ensures the list persists while the user navigates between pages.
if "liked_cities" not in st.session_state:
    st.session_state.liked_cities = []
    
# -- SIDEBAR NAVIGATION --
with st.sidebar:
    # Option Menu library used for a cleaner, app-like navigation bar
    selected = option_menu(
        menu_title="Menu",  
        options=["Home", "Explore Ratings", "City Recommender", "Find Destination", "Liked Cities", "City Gallery"],
        icons=["house", "bar-chart", "compass", "map", "heart", "images"],  
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

# Page Routing: Map sidebar selection to session state variable
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
elif selected == "City Gallery":
    st.session_state.page = "Gallery"
    
# Sidebar Footer
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
    |  Made with ❤️ by <b>Gabriela Simon de Cenco</b>  
</div>
""", unsafe_allow_html=True)

# ---- PAGE: HOME ----
if st.session_state.page == "Home":
    st.title("🌎 Where to Next?")
    
    # Intro Card using Custom HTML
    st.markdown("""
    <div class="content-card">
        <h3 style="margin-top:0;">Welcome Traveler! ✈️</h3>
        <p>This project aims to help you discover your next ideal travel destination based on your preferences and interests.</p>
        <p>Whether you're looking for <b>vibrant city life</b>, <b>serene nature spots</b>, or <b>cultural experiences</b>, we've got you covered!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("https://cdn.pixabay.com/photo/2017/06/05/11/01/airport-2373727_1280.jpg", use_container_width=True)
    
    st.markdown("---")
    
    # Navigation Instructions
    st.markdown("""
    <div class="content-card">
        <h3>How to use this app:</h3>
        <p>Navigate through the app using the sidebar to explore different features:</p>
        <ul style="line-height: 1.8;">
            <li><b>🌟 Explore Cities by Ratings:</b> Visualize and filter cities based on various travel-related ratings.</li>
            <li><b>📍 City Recommender:</b> Select a city to get recommendations for similar cities.</li>
            <li><b>🗺️ Find your ideal destination:</b> Take the quiz to discover your perfect travel spot.</li>
            <li><b>❤️ Liked Cities:</b> Keep track of the cities you liked during your exploration.</li>
            <li><b>🌄 City Gallery:</b> Browse through all the possible destinations to see marvelous sights.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

 # ---- PAGE: CITY RECOMMENDER ----   
elif st.session_state.page == "Recommender":
    st.title("📍 City Recommender")
    st.write("Choose a city you liked, and we'll suggest similar cities you might enjoy!")
    city_options = {
    f"{row['city']}, {row['country']}": row['city']
    for _, row in df.iterrows()
    }
    selected_label = st.selectbox("Choose a city you liked", sorted(city_options.keys()))
    city_choice = city_options[selected_label]
    
    # Retrieve metadata for the selected city
    city_choice_country = df[df["city"] == city_choice]["country"].values[0]
    city_choice_description = df[df["city"] == city_choice]["short_description"].values[0]
    city_choice_id = df[df["city"] == city_choice]["id"].values[0]
    
    if city_choice:
        st.write(f"### If you liked _{city_choice}, {city_choice_country}_ you might also like:")
        
        # Algorithm: Calculate Euclidean distance to find nearest neighbors
        recs = recommend_similar_cities(df, city_choice)
        st.dataframe(recs)
        
        # Visuals: Bar chart of ratings
        st.write(f"### City Ratings Overview for _{city_choice}, {city_choice_country}_")
        rating_columns_lower = [col.lower() for col in RATING_COLUMNS]
        fig = ratings_city_plot(df, rating_columns_lower, city_choice)
        st.plotly_chart(fig, use_container_width=True)
        
        # Like Button Logic
        if st.button("❤️ Like city", key=f"like_{city_choice}"):
            new_fav_city = {
                "id": city_choice_id,
                "city": city_choice,
                "country": city_choice_country,
                "description": city_choice_description
            }
            
            # Check for duplicates in session state
            existing_ids = [item['id'] for item in st.session_state.liked_cities]
            
            
            if city_choice_id not in existing_ids:
                st.session_state.liked_cities.append(new_fav_city)
                st.success(f"You liked {city_choice}!")
            else:
                st.warning(f"{city_choice} is already in your favorites.")
                
# ---- PAGE: DESTINATION QUIZ ----
elif st.session_state.page == "Destination":
    st.title("🗺️ Find your ideal destination!")
    st.write("Take this quick quiz and discover where should you should go for your next vacation!")
    st.markdown("----")
    st.write("Reply to the questions with your preferences.")
    
    # Dynamically render questions
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
        
    # Container for results (persists across reruns)
    if "results_df" not in st.session_state:
        st.session_state.results_df = None
        
    click = st.button("Get Recommendations")
    
    # Logic: Show results if clicked OR if valid results already exist
    if click or st.session_state.results_df is not None:
        if click:
            if any(answer is None for answer in answers.values()):
                st.error("⚠️ Please answer all questions before continuing.")
                st.stop() 
            else:
                # Compute Weighted Euclidean Distance
                st.session_state.results_df = compute_result(answers, df)
                
        computed_results = st.session_state.results_df
        
        if computed_results is not None:
            st.write("### Based on your answers, we recommend you the following cities:")
            
            if computed_results.empty:
                st.write("😔 Unfortunately, no cities match your preferences.")
            else:
                for i, row in computed_results.head(5).iterrows():
                    # Handle month display
                    if answers["month"] is not None:
                        month = answers['month'] - 1
                        month = MONTHS[month]
                        
                    # Render styled HTML card
                    card_html = quiz_city_card_html(row, month)
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    image_url = city_images.get(row["id"])
                    if image_url:
                        st.image(image_url, use_container_width=True)
                    else:
                        st.info("No image available for this city.")
                
                    # Like button for recommended cities
                    if st.button("❤️ Like city", key=f"like_{row['city']}"):
                        new_fav_city = {
                            "id": row["id"],
                            "city": row["city"],
                            "country": row["country"],
                            "description": row["short_description"]
                        }
                        
                        existing_ids = [item['id'] for item in st.session_state.liked_cities]
                        
                        
                        if row["id"] not in existing_ids:
                            st.session_state.liked_cities.append(new_fav_city)
                            st.success(f"You liked {row['city']}!")
                        else:
                            st.warning(f"{row['city']} is already in your favorites.")
                            
                    st.markdown("---")

                # Map Visualization
                st.write("### Top Recommended Cities on the Map")
                fig = results_plot(computed_results.head(5))
                st.plotly_chart(fig, use_container_width=True)
                

# ---- PAGE: EXPLORE CITIES BY RATINGS ----
elif st.session_state.page == "Plots":
    st.title("🌟 Explore Cities by Ratings")
    st.markdown("Explore cities around the world and find your next travel destination!")

    values = [1, 2, 3, 4, 5]

    # Filters
    category = st.selectbox("Select a category", RATING_COLUMNS)
    st.write(f"**{category}:** {VARIABLE_DESCRIPTIONS[category.lower()]}")
    category = category.lower()
    region_selection = st.selectbox("Select a region", REGIONS)
    region_selection = region_selection.lower()
    
    # Star Rating Filters
    st.write("#### **Filter by rating:**")
    cols = st.columns(5)  

    selected_ranks = []
    for i, rating in enumerate(range(1, 6)):
        with cols[i]:
            if st.checkbox(f"{rating} ⭐", value=True, key=f"rating_{rating}"):
                selected_ranks.append(rating)
    st.subheader(f"Cities rankings for {category.title()}")
    
    # Apply filters and plot
    filtered_df = df[df[category].isin(selected_ranks)]
    fig = rating_category_plot(filtered_df, category, region_selection)
    st.plotly_chart(fig, use_container_width=True)


# ---- PAGE: LIKED CITIES ----
elif st.session_state.page == "Liked":
    st.title("❤️ Liked Cities")
    if st.session_state.liked_cities:
        st.write("Here are your liked cities:")
        
        # Iterate over session state list
        for city in st.session_state.liked_cities:
            html_card = likes_city_card_html(city)
            st.markdown(html_card, unsafe_allow_html=True)
            
            image_url = city_images.get(city['id'])
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.info("No image available for this city.")
            
            # Remove Button Layout
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1]) 
            
            with col4: 
                if st.button("💔 Remove Like", key=f"remove_{city['id']}"):
                    st.session_state.liked_cities = [
                        c for c in st.session_state.liked_cities 
                        if c['id'] != city['id']
                    ]
                    # Rerun to update the UI immediately
                    st.rerun()
            st.write("---")
            
    else:
        st.write("You haven't liked any cities yet.")
 
 
# ---- PAGE: CITY GALLERY ----        
elif st.session_state.page == "Gallery":
    st.title("🌄 City Gallery")
    st.write("Browse our collection of stunning destinations!")
    
    # Adjust region list for gallery display
    unique_regions = REGIONS[1:]
    unique_regions.append("Middle East")
    
    for region in unique_regions:
        with st.expander(f"📍 {region}", expanded=False):
            # Normalize region string
            region_cd = region.lower().replace(" ", "_")
            region_df = df[df['region'] == region_cd]
            unique_countries = sorted(region_df['country'].unique())
            for country in unique_countries:
                st.markdown(f"#### {country}")
                country_cities = region_df[region_df['country'] == country]
                
                # Grid Layout (3 columns)
                cols = st.columns(3)
                for index, (_, row) in enumerate(country_cities.iterrows()):
                    
                    col_index = index % 3
                    with cols[col_index]:
                        
                        img_url = city_images.get(row['id'])
                        with st.container():
                            if img_url:
                                st.image(img_url, use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/300x200?text=No+Image", use_container_width=True)
                            st.markdown(f"**{row['city']}**")
                st.markdown("---") 