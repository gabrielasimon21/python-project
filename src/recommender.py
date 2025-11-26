import plotly.express as px
from src.data_utils import df
from src.variables import RATING_COLUMNS
import numpy as np


#TODO: change distance calculation for euclidean distance
# reason: euclidean distance punishes larger deviations


def recommend_similar_cities(df, city_choice):
    # Compute similarity: find cities with similar ratings
    data = df.copy()
    rating_columns_lower = [col.lower() for col in RATING_COLUMNS]
    
    target_vector = data.loc[data["city"] == city_choice, rating_columns_lower].values[0].astype(float)
   
    features = data[rating_columns_lower].astype(float).values

    distances = np.sqrt(np.sum((features - target_vector) ** 2, axis=1))
    data["distance"] = distances

    max_dist = np.sqrt(len(rating_columns_lower) * (4 ** 2))

    data["similarity"] = (1 - (data["distance"] / max_dist)) * 100

    recs = (
        data.loc[data["city"] != city_choice, ["city", "country", "similarity"]]
        .sort_values(by="similarity", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )
    
    recs["similarity"] = recs["similarity"].clip(0, 100).apply(lambda x: f"{x:.1f}%")
    
    return recs
    
    
