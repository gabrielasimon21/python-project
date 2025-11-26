import streamlit as st

def local_css():
    st.markdown("""
    <style>
    /* 1. IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@400;700&display=swap');

    html, body, [class*="css"], button, input, select, textarea {
        font-family: 'Lato', serif !important;
    }

    /* 2. BACKGROUND & LAYOUT */
    .stApp {
        background: linear-gradient(to bottom, #fdfeffff, #c1ddffff);
    }
    
    /* Remove top padding bloat */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 5rem;
    }

    /* 3. HEADERS */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700;
        color: #222473ff !important;
    }
    
    /* 4. CUSTOM "CARD" CONTAINER (Use this everywhere!) */
    .content-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
        margin-bottom: 20px;
    }

    /* 5. STYLE STREAMLIT WIDGETS */
    
    /* Selectbox & Text Input focus state */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    .stSelectbox > div > div:focus-within {
        border-color: #222473;
        box-shadow: 0 0 0 1px #222473;
    }
    
    /* Radio Buttons - Make them look like clean lists */
    .stRadio > div {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        border: 1px solid #eee;
    }

    /* 6. BUTTON STYLING (Deep Blue Theme) */
    .stButton > button {
        background-color: #222473; /* Full Blue Background */
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1a1c5e;
        box-shadow: 0 4px 10px rgba(34, 36, 115, 0.3);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

def quiz_city_card_html(row, month=None):
    """
    Your travel ticket style card.
    """
    html_content = f"""
    <div class="content-card" style="border-left: 6px solid #222473; padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; font-size: 20px; color: #222473;">{row['city']}, {row['country']}</h3>
            <span style="background-color: #e8f2ff; color: #222473; padding: 5px 12px; border-radius: 20px; font-weight: 600; font-size: 13px;">
                {row['similarity']} Match
            </span>
        </div>
        <p style="color: #555; font-style: italic; margin-top: 10px; font-size: 14px;">"{row['short_description']}"</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
        <div style="font-size: 14px; color: #444;">
            🌡️ Average temperature in {month}: <b>{row['avg_temp']:.1f}°C</b>
        </div>
    </div>
    """
    return html_content

def likes_city_card_html(row):
    """
    Card HTML for liked cities.
    Removes the "Match %" and "Temperature" since those might change or not be relevant here.
    """
    html_content = f"""
    <div class="content-card" style="border-left: 6px solid #FF4B4B; padding: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
    <h3 style="margin: 0; font-size: 20px; color: #222473;">{row['city']}, {row['country']}</h3>
    <span style="font-size: 20px;">❤️</span>
    </div> 
    <p style="color: #555; font-style: italic; margin-top: 10px; font-size: 14px;">{row['description']}</p>
    </div>
    """
    return html_content