import pycountry
import plotly.express as px
from src.data_utils import load_data
from src.descriptions import rating_columns
import numpy as np

csv = "data/worldwide-travel-cities.csv"

df = load_data(csv)

def get_iso(country):
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None

def recommend_similar_cities(df, city_choice):
    # Compute similarity: find cities with similar ratings
    data = df.copy()
    rating_columns_lower = [col.lower() for col in rating_columns]
    city_vector = data[data["city"] == city_choice][rating_columns_lower].iloc[0]
    # Compute Manhattan distance (sum of absolute differences)
    data["distance"] = data[rating_columns_lower].apply(lambda row: np.abs(row - city_vector).sum(), axis=1)
    
    # Convert distance to similarity percentage
    max_distance = len(rating_columns_lower) * 4  # max possible distance if ratings are from 1 to 5
    data["similarity"] = (1 - data["distance"] / max_distance) * 100  # scale to 0–100%

    recs = (
        data.loc[data["city"] != city_choice, ["city", "country", "similarity"]]
        .sort_values(by="similarity", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )
    recs["similarity"] = recs["similarity"].round(2).map("{:.1f}%".format)
    return recs
    
    
