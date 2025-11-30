from src.variables import RATING_COLUMNS
import numpy as np
import pandas as pd

def recommend_similar_cities(df, city_choice):
    """
    Calculates the 5 most similar cities to the selected city based on 
    Euclidean distance of their feature ratings.
    
    Args:
        df (pd.DataFrame): The dataframe containing city data.
        city_choice (str): The name of the target city to find similarities for.

    Returns:
        pd.DataFrame: A dataframe containing the top 5 similar cities and their similarity percentages.
        Returns an empty DataFrame if the city is not found.
    """
    if city_choice not in df["city"].values:
        return pd.DataFrame()
    # Work on a copy to prevent modifying the main dataframe
    data = df.copy()
    rating_columns_lower = [col.lower() for col in RATING_COLUMNS]
    
    # Extract the rating vector for the specific city the user selected
    # .values[0] gets the flat array for calculation
    target_vector = data.loc[data["city"] == city_choice, rating_columns_lower].values[0].astype(float)
   
    # Get the rating matrix for all cities
    features = data[rating_columns_lower].astype(float).values

    # Calculate Euclidean Distance 
    distances = np.sqrt(np.sum((features - target_vector) ** 2, axis=1))
    data["distance"] = distances

    # Calculate the theoretical maximum distance to normalize the score 0-100%
    # (Max difference per attribute is 4, i.e., rating 5 vs 1)
    max_dist = np.sqrt(len(rating_columns_lower) * (4 ** 2))

    # Invert distance so that 0 distance = 100% similarity
    data["similarity"] = (1 - (data["distance"] / max_dist)) * 100

    # Sort by highest similarity and remove the city itself from results
    recs = (
        data.loc[data["city"] != city_choice, ["city", "country", "similarity"]]
        .sort_values(by="similarity", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )
    
    # Format similarity as a string for display
    recs["similarity"] = recs["similarity"].clip(0, 100).apply(lambda x: f"{x:.1f}%")
    
    return recs
    
    
