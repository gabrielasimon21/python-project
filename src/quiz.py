from src.data_utils import df
import json
import pandas as pd
from src.variables import RATING_COLUMNS
import numpy as np

# TODO: comment code 

def get_avg_temp_month(row, month):
    try:
        temp_dict = json.loads(row["avg_temp_monthly"])
        return temp_dict[str(month)]["avg"]
    except:
        return 20 

def compute_result(answers):
    if answers["region"] != 0: 
        results_df = df[df["region"] == answers["region"]].copy()
    else:
        results_df = df.copy()

    results_df["constraint_penalty"] = 1.0 

    dur_mask = results_df["ideal_durations"].apply(lambda x: answers["ideal_durations"] in x)
    
    if not results_df[dur_mask].empty:
        results_df = results_df[dur_mask]
    else:
        results_df["constraint_penalty"] *= 0.8
        
    budget_mask = pd.Series(True, index=results_df.index)

    if answers["budget_level"] == "Budget":
        budget_mask = results_df["budget_level"] == "Budget"
    elif answers["budget_level"] == "Mid-range":
        budget_mask = results_df["budget_level"].isin(["Budget", "Mid-range"])
    elif answers["budget_level"] == "Luxury":
        budget_mask = results_df["budget_level"].isin(["Mid-range", "Luxury"])
    
    if not results_df[budget_mask].empty:
        results_df = results_df[budget_mask]
    else:
        results_df["constraint_penalty"] *= 0.7

    month = answers["month"]
    results_df["avg_temp"] = results_df.apply(lambda r: get_avg_temp_month(r, month), axis=1)
    
    temp_mapping_celsius = {0: -5, 1: 5, 2: 15, 3: 25, 4: 30}
    target_temp = temp_mapping_celsius.get(answers["avg_temp_monthly"], 20)
    
    results_df["temp_diff"] = abs(results_df["avg_temp"] - target_temp)
    
    temp_mask = results_df["temp_diff"] <= 10 
    
    if not results_df[temp_mask].empty:
        results_df = results_df[temp_mask]

        results_df["constraint_penalty"] *= (1 - (results_df["temp_diff"] * 0.01))
    else:
        results_df["constraint_penalty"] *= 0.7

    rating_cols = [col.lower() for col in RATING_COLUMNS]
    user_vector = np.array([answers[col] for col in rating_cols], dtype=float)

    if user_vector.sum() == 0:
        weights = np.ones(len(user_vector))
    else:
        weights = user_vector ** 2

    max_diffs = np.maximum(abs(user_vector - 1), abs(user_vector - 5))
    max_possible_dist = np.sqrt(np.sum(weights * (max_diffs ** 2)))
    
    def compute_weighted_euclidean_score(row):
        city_vector = row[rating_cols].astype(float).values
        sq_diff = (city_vector - user_vector) ** 2
        weighted_sq_diff = sq_diff * weights
        actual_dist = np.sqrt(np.sum(weighted_sq_diff))

        score = 1 - (actual_dist / (max_possible_dist + 1e-6))
        return score

    results_df["content_score"] = results_df.apply(compute_weighted_euclidean_score, axis=1)
    results_df["final_score"] = results_df["content_score"] * results_df["constraint_penalty"]
    
    results_df["similarity"] = (results_df["final_score"] * 100).clip(0, 100)
    results_df["similarity"] = results_df["similarity"].round(1).map("{:.1f}%".format)

    top_cities = results_df.sort_values(by="final_score", ascending=False).head(5)

    return top_cities.drop(
        columns=["constraint_penalty", "temp_diff", "content_score", "final_score"], 
        errors='ignore'
    )