import plotly.express as px
import pycountry

def rating_category_plot(df, category, region_selection):
    
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

import plotly.express as px

def rating_category_plot_test(df, category, region_selection):
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color=category,
        hover_name="city",
        size=category,
        size_max=20,
        color_continuous_scale="RdYlGn",
        range_color=[1, 5],
        zoom=1,
        height=600    
    
    )

    fig.update_layout(
        mapbox_style="open-street-map",  # free, no API key needed
        margin={"r":0,"t":0,"l":0,"b":0},
         
    )

    return fig








'''def get_iso(country):
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None

country_df = df.groupby("country", as_index=False)[category].mean()
country_df["iso_alpha"] = country_df["country"].apply(get_iso)

fig2 = px.choropleth(
    country_df,
    locations="iso_alpha",
    color=category,
    hover_name="country",
    color_continuous_scale="RdYlGn",
    title=f"Average {category.title()} Rating by Country"
)
st.plotly_chart(fig2, use_container_width=True)

st.sidebar.markdown("-------")



city_choice = st.selectbox("Choose a city you liked", df["city"].unique())

if city_choice:
    st.subheader(f"If you liked **{city_choice}**, you might also like:")

    # Compute similarity: find cities with similar ratings
    features = ["culture","adventure","nature","beaches","nightlife","cuisine","wellness","urban","seclusion"]
    city_vector = df[df["city"] == city_choice][features].iloc[0]
    df["similarity"] = df[features].apply(lambda row: -abs(row - city_vector).sum(), axis=1)
    recs = df[df["city"] != city_choice].nlargest(5, "similarity")[["city", "country", category]]
    st.dataframe(recs)
    
    
'''