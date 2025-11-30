import json
import pandas as pd
from src.variables import RATING_COLUMNS
import numpy as np

def get_avg_temp_month(row, month):
    """
    Parses the JSON string in the dataset to retrieve the average 
    temperature for a specific month.
    
    Args:
        row (pd.Series): A row from the dataframe containing the 'avg_temp_monthly' JSON string.
        month (int): The month number (1-12) to retrieve the temperature for.

    Returns:
        float: The average temperature in Celsius for that month.
    """
    temp_dict = json.loads(row["avg_temp_monthly"])
    return temp_dict[str(month)]["avg"]

def compute_result(answers, df):
    """
    Calculates city recommendations based on user quiz answers.
    Uses a hybrid approach: Hard filtering for Region, Soft filtering (penalties)
    for constraints, and Weighted Euclidean Distance for preferences.
    
    Args:
        answers (dict): A dictionary mapping question keys (e.g., 'budget_level') to user responses.
        df (pd.DataFrame): The main dataframe containing city data.

    Returns:
        pd.DataFrame: A dataframe of the top 5 recommended cities with their similarity scores.
    """
    # -- 1. Hard Filter: Region --
    # Strictly enforce region selection. If 0 ('Anywhere'), keep all.
    if answers["region"] != 0: 
        results_df = df[df["region"] == answers["region"]].copy()
    else:
        results_df = df.copy()
        
    # Initialize the penalty multiplier at 1.0 (100% score)
    results_df["constraint_penalty"] = 1.0 
    
    # --- 2. Soft Filter: Duration ---
    # Check which cities fit the user's time constraint
    dur_mask = results_df["ideal_durations"].apply(lambda x: answers["ideal_durations"] in x)
    
    if not results_df[dur_mask].empty:
        # If matches exist, filter down to them
        results_df = results_df[dur_mask]
    else:
        # If filtering causes an empty result, ignore the filter but apply a 20% penalty
        results_df["constraint_penalty"] *= 0.8
        
    # -- 3. Soft Filter: Budget --
    # Default to True (select all) to handle edge cases
    budget_mask = pd.Series(True, index=results_df.index)
    
    # 'Luxury' includes Mid-range; 'Mid-range' includes Budget
    if answers["budget_level"] == "Budget":
        budget_mask = results_df["budget_level"] == "Budget"
    elif answers["budget_level"] == "Mid-range":
        budget_mask = results_df["budget_level"].isin(["Budget", "Mid-range"])
    elif answers["budget_level"] == "Luxury":
        budget_mask = results_df["budget_level"].isin(["Mid-range", "Luxury"])
    
    if not results_df[budget_mask].empty:
        results_df = results_df[budget_mask]
    else:
        # Penalize by 30% if budget constraints cannot be met
        results_df["constraint_penalty"] *= 0.7
    
    # -- 4. Soft Filter: Temperature --
    month = answers["month"]
    # Extract numeric temperature for the selected month
    results_df["avg_temp"] = results_df.apply(lambda r: get_avg_temp_month(r, month), axis=1)
    
    # Map qualitative user input (0-4) to approx Celsius targets
    temp_mapping_celsius = {0: -5, 1: 5, 2: 15, 3: 25, 4: 30}
    target_temp = temp_mapping_celsius.get(answers["avg_temp_monthly"], 20)
    
    # Calculate distance from ideal temp
    results_df["temp_diff"] = abs(results_df["avg_temp"] - target_temp)
    
    # Keep cities within a 10-degree window
    temp_mask = results_df["temp_diff"] <= 10 
    
    if not results_df[temp_mask].empty:
        results_df = results_df[temp_mask]
        # Apply micro-penalty: 1% score reduction per degree of difference
        results_df["constraint_penalty"] *= (1 - (results_df["temp_diff"] * 0.01))
    else:
        # Heavy penalty (30%) if no cities match the weather preference
        results_df["constraint_penalty"] *= 0.7

    # -- 5. Content Matching: Weighted Euclidean Distance --
    rating_cols = [col.lower() for col in RATING_COLUMNS]
    user_vector = np.array([answers[col] for col in rating_cols], dtype=float)

    # Weighting Logic: Square the user preference (1-5).
    # This makes "Very Important" (5->25) significantly more impactful than "Not Important" (1->1).
    if user_vector.sum() == 0:
        weights = np.ones(len(user_vector))
    else:
        weights = user_vector ** 2

    # Calculate max possible distance for normalization (0-100 scale)
    max_diffs = np.maximum(abs(user_vector - 1), abs(user_vector - 5))
    max_possible_dist = np.sqrt(np.sum(weights * (max_diffs ** 2)))
    
    def compute_weighted_euclidean_score(row):
        city_vector = row[rating_cols].astype(float).values
        
        # Calculate weighted squared differences
        sq_diff = (city_vector - user_vector) ** 2
        weighted_sq_diff = sq_diff * weights
        actual_dist = np.sqrt(np.sum(weighted_sq_diff))

        # Normalize: 1.0 is perfect match, 0.0 is worst match
        score = 1 - (actual_dist / (max_possible_dist + 1e-6))
        return score

    # -- 6. Final Scoring --
    # Combine content similarity with constraint penalties
    results_df["content_score"] = results_df.apply(compute_weighted_euclidean_score, axis=1)
    results_df["final_score"] = results_df["content_score"] * results_df["constraint_penalty"]
    
    # Format for display
    results_df["similarity"] = (results_df["final_score"] * 100).clip(0, 100)
    results_df["similarity"] = results_df["similarity"].round(1).map("{:.1f}%".format)

    # Return top 5 matches
    top_cities = results_df.sort_values(by="final_score", ascending=False).head(5)

    return top_cities.drop(
        columns=["constraint_penalty", "temp_diff", "content_score", "final_score"], 
        errors='ignore'
    )