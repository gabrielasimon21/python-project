import plotly.express as px
#import pycountry
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

    fig.update_layout(geo_scope=region_selection)
    
    return fig

def ratings_city_plot(df, rating_columns, city_choice):
    # Plot of the ratings for the city selected by the user
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

    