from src.data_utils import df
import json
import pandas as pd
from src.variables import RATING_COLUMNS
import numpy as np

QUESTIONS = {
    "region": {
        "text": "🌏 To which region of the world would you like to travel?",
        "type": "select",
        "options": ["Africa", "Asia", "Europe",
                    "Middle East", "North America", 
                    "Oceania", "South America", "No specific region"],
        "mapping": {
            "Europe": "europe",
            "Asia": "asia",
            "Africa": "africa",     
            "North America": "north_america",   
            "South America": "south_america",
            "Oceania": "oceania",
            "Middle East": "middle_east",
            "No specific region": 0
        }
    },
    "ideal_durations": {
        "text": "🧳 How long do you plan to travel?",
        "type": "select",
        "options": ["For a Weekend", "For 4-5 days", "For 1 week to 10 days", "More than 2 weeks"],
        "mapping": {
            "For a Weekend": "Weekend",
            "For 4-5 days": "Short trip",
            "For 1 week to 10 days": "One week",
            "More than 2 weeks": "Long trip"
        }
    },
    "budget_level": {
        "text": "💰 What is your approximate budget for the trip?",
        "type": "select",
        "options": ["Low", "Medium", "High"],
        "mapping": {"Low": "Budget", "Medium": "Mid-range", "High": "Luxury"}
    },
    "month": {
        "text": "📅 In which month would you like to travel?",
        "type": "select",
        "options": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        "mapping": {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }
    },
    "avg_temp_monthly": {
        "text": "🌤️ What's your ideal weather?",
        "type": "select",
        "options": ["Very cold", "Cold", "Mild", "Warm", "Hot"],
        "mapping": {"Very cold": 0, "Cold": 1, "Mild": 2, "Warm": 3, "Hot": 4}
    },
    "culture": {
        "text": "🏰 How important is experiencing local culture when you travel?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "adventure": {
        "text": "🧗‍♂️ How important are adventure activities when you travel?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "nature": {
        "text": "🌳 How important is the presence of nature landscapes in your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "beaches": {
        "text": "🏖️ How important is having access to beaches on your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "nightlife": {
        "text": "🍸 How important is experiencing nightlife on your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "cuisine": {
        "text": "🥗 How important is trying local cuisine when you travel?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "wellness": {
        "text": "🧘‍♀️ How important are wellness and relaxation opportunities on your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "urban": {
        "text": "🏙️ How important is it for your destination to be a modern, urban city?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "seclusion": {
        "text": "🎋 How important is it for your destination to be a secluded, peaceful area?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
}

def get_avg_temp_month(row, month):
    temp_dict = json.loads(row["avg_temp_monthly"])
    return temp_dict[str(month)]["avg"]

def compute_result(answers):
    
    if answers["region"] != 0: 
        results_df = df[df["region"] == answers["region"]]
    else:
        results_df = df.copy()

    results_df = results_df[results_df["ideal_durations"].apply(lambda x: answers["ideal_durations"] in x)]

    if answers["budget_level"] == "Budget":
        results_df = results_df[results_df["budget_level"] == "Budget"]
    elif answers["budget_level"] == "Mid-range":
        results_df = results_df[results_df["budget_level"].isin(["Budget", "Mid-range"])]
    elif answers["budget_level"] == "Luxury":
        results_df = results_df[results_df["budget_level"].isin(["Mid-range", "Luxury"])]

    month = answers["month"]  
    results_df["avg_temp"] = results_df.apply(lambda r: get_avg_temp_month(r, month), axis=1)

    results_df["temp_category"] = pd.cut(results_df["avg_temp"], bins=5, labels=[1, 2, 3, 4, 5])
    preferred_weather = answers["avg_temp_monthly"]  # 1–5
    results_df = results_df[results_df["temp_category"] == preferred_weather]


    rating_cols = [col.lower() for col in RATING_COLUMNS]
    user_vector = np.array([answers[col] for col in rating_cols], dtype=float)

    weights = user_vector**2 / (user_vector**2).sum() 
    
    def compute_weighted_similarity(row):
        city_vector = row[rating_cols].astype(float).values
        weighted_city = city_vector * weights
        weighted_user = user_vector * weights
        return np.dot(weighted_city, weighted_user) / (
            np.linalg.norm(weighted_city) * np.linalg.norm(weighted_user))

    results_df["similarity"] = results_df.apply(compute_weighted_similarity, axis=1)
    results_df["similarity"] = results_df["similarity"] * 100  # scale to 0–100%
    results_df["similarity"] = results_df["similarity"].round(2).map("{:.1f}%".format)

    top_cities = results_df.sort_values(by="similarity", ascending=False).head(5)
    
    return top_cities