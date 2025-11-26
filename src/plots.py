import plotly.express as px
import pandas as pd

def rating_category_plot(df, category, region_selection):
    # World map plot of the category selected by the user
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        color=category,
        hover_name="city",
        size=category,
        size_max=15, 
        color_continuous_scale="RdYlGn",
        range_color=[1, 5],
        projection="natural earth",
    )

    fig.update_layout(
        geo_scope=region_selection,
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(showland=True, landcolor="rgb(243, 243, 243)")
    )

    return fig

def ratings_city_plot(df, rating_columns, city_choice):
    # Bar chart of the ratings for the city selected by the user
    city_row = df[df["city"] == city_choice].iloc[0]
    
    ratings = city_row[rating_columns].astype(float) 

    rating_df = pd.DataFrame({
        "Category": rating_columns,
        "Rating": ratings.values
    })
    
    fig = px.bar(
        rating_df,
        x="Category",
        y="Rating",
        color="Rating",
        color_continuous_scale="RdYlGn",
        range_color=[1, 5],
        text="Rating",
    )
    
    fig.update_layout(
        yaxis=dict(range=[0, 5]),
        coloraxis_showscale=False, 
        height=400
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    
    return fig

    
def results_plot(df_results):
    # Map plot of the top recommended cities
    plot_df = df_results.copy()

    if plot_df["similarity"].dtype == object:
        plot_df["similarity_score"] = plot_df["similarity"].str.rstrip('%').astype(float)
    else:
        plot_df["similarity_score"] = plot_df["similarity"]

    fig = px.scatter_geo(
        plot_df,
        lat="latitude",
        lon="longitude",
        hover_name="city",
        text="city", 
        size="similarity_score", 
        color="similarity_score", 
        color_continuous_scale="RdYlGn",
        projection="natural earth",
    )

    fig.update_layout(
        geo_scope="world",
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(showland=True, landcolor="rgb(243, 243, 243)")
    )
    
    return fig
