import plotly.express as px
import pandas as pd

def rating_category_plot(df, category, region_selection):
    """
    Generates a bubble map showing cities colored and sized by a specific rating category.
    
    Args:
        df (pd.DataFrame): The dataframe containing city data.
        category (str): The specific column name to visualize (e.g., 'Nature', 'Nightlife').
        region_selection (str): The specific region to focus the map on (e.g., 'europe', 'world').

    Returns:
        plotly.graph_objects.Figure: An interactive Plotly map object.
    """
    
    # Create the scatter map 
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        color=category,
        hover_name="city",
        size=category,
        size_max=15, 
        color_continuous_scale="RdYlGn", # Red (low) to Green (high)
        range_color=[1, 5],
        projection="natural earth",
    )

    # Update layout to focus on specific region and remove whitespace
    fig.update_layout(
        geo_scope=region_selection,
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(showland=True, landcolor="rgb(243, 243, 243)")
    )

    return fig

def ratings_city_plot(df, rating_columns, city_choice):
    """
    Creates a bar chart visualizing how the city selectes by the user ranks across all categories.
    
    Args:
        df (pd.DataFrame): The dataframe containing city data.
        rating_columns (list): A list of column names representing the rating categories.
        city_choice (str): The name of the city selected by the user.

    Returns:
        plotly.graph_objects.Figure: An interactive Plotly bar chart object.
    """
    # Extract the specific row for the selected city
    city_row = df[df["city"] == city_choice].iloc[0]
    
    ratings = city_row[rating_columns].astype(float) 

    # Prepare a dataframe for Plotly
    rating_df = pd.DataFrame({
        "Category": rating_columns,
        "Rating": ratings.values
    })
    
    # Build bar chart
    fig = px.bar(
        rating_df,
        x="Category",
        y="Rating",
        color="Rating",
        color_continuous_scale="RdYlGn",
        range_color=[1, 5],
        text="Rating", # Show the number on the bar
    )
    
    # Lock y-axis to 5 so visual comparison is accurate
    fig.update_layout(
        yaxis=dict(range=[0, 5]),
        height=400
    )
    
    # Format labels to 1 decimal place and place them on top of bars
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    
    return fig

    
def results_plot(df_results):
    """
    Map plot of the top recommended cities
    
    Args:
        df_results (pd.DataFrame): A dataframe containing only the top recommended cities and their similarity scores.

    Returns:
        plotly.graph_objects.Figure: An interactive Plotly map object showing the recommended cities.
    """
    plot_df = df_results.copy()

    # Clean the similarity column if it's currently a string with '%'
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
        size_max=15,
        color_continuous_scale="RdYlGn",
        projection="natural earth",
    )

    fig.update_layout(
        geo_scope="world",
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(showland=True, landcolor="rgb(243, 243, 243)")
    )
    
    return fig
