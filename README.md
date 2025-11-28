# Where to next? - Travel Recommender App
**Where to Next?** is an interactive Streamlit application designed to help travelers discover their next ideal destination. By combining data visualization with content-based filtering, the app provides personalized city recommendations based on user preferences for weather, budget, and activities.

## Data Source

The data used in this project consists of a dataset of travel information about cities. It contains information related to budget, ideal trip duration, and temperature in each city, as well as rankings from 1 to 5 of the main features a trip destination could have. 
The dataset can be downloaded from Kaggle in the following url: [link to dataset](https://www.kaggle.com/datasets/furkanima/worldwide-travel-cities-ratings-and-climate/data).

## Pages


* **Explore Cities by Ratings:**  This interactive dashboard  allows users to filter cities based on specific travel categories (e.g., Nightlife, Nature). Users can visualize the data using a global map plot where cities are represented as points. The color and size of each point correspond to its ranking in the selected category, ranging from 1 star (Red/Small) to 5 stars (Green/Large).
Users can select to see all rankings or filter the amount of stars desired. 

* **City Recommender:** In this content-based filtering tool users select a city they already enjoy, and the algorithm identifies the 5 most similar cities in the dataset. Similarity is calculated by computing rating vectors for each city and determining the Euclidean distance between them. The top 5 most similar are shown in tabular format, alongside a bar chart that shows how the selected city was ranked in each of the categories.

* **Find Your Ideal Destination Quiz:** This quiz takes users preferences for each aspect of a trip in a series of questions and defines up to 5 cities that are the most ideal for that set of answers

    * **Logic:** The app creates a vector that stores the user preferences, representing the "perfect destination". The app then calculates the Weighted Euclidean Distance between the user vector and every city vector. This ensures that categories marked as "Very Important" have a higher influence on the result.
    
    * **Soft Filtering:** Instead of strictly removing cities that don't match the budget or duration (which often leads to zero results), the algorithm applies mathematical penalties to their scores. In this way, the app always returns valid recommendations, ranking the "closest matches" highest even if they aren't perfect

* **Liked Cities Page:** Throughout the exploration of the app, users can like cities that spark their attention. In this page, users can see all the cities they liked, to save them.

* **City Gallery:** In this page, users can browse the images of all the cities present in the dataset. To ensure ease of navigation, the gallery is organized hierarchically by Region and Country.


## Setup Instructions

Follow these steps to run the application locally. 

### 1. Clone the repository
```bash
git clone https://github.com/gabrielasimon21/python-project.git
cd python-project
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```bash 
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```
The app should open automatically in your browser at `http://localhost:8501`.


## Project Structure
* `project/`
    * `app.py`: The main entry point of the application. Handles page navigation and UI rendering.
    * `requirements.txt`: Lists all Python libraries and versions required.
    * `.streamlit/`
        * `config.toml`: Global visual configurations (theme colors and fonts) for Streamlit.
    * `data/`
        * `worldwide-travel-cities.csv`: The dataset used for analysis. Downloaded from Kaggle and stored locally. The [data](https://www.kaggle.com/datasets/furkanima/worldwide-travel-cities-ratings-and-climate/data) should be downloaded in your machine and stored in the folder `data/`.
    * `src/`
        * `__init__.py`: Makes the `src/` directory a Python package.
        * `data_utils.py`: Functions for loading and cleaning the CSV data using caching.
        * `images.py`: A dictionary mapping City IDs to their respective image URLs.
        * `plots.py`: Functions for generating Plotly maps and bar charts.
        * `quiz.py`: Contains the Weighted Euclidean Distance logic for the quiz to discover the user's ideal destination.
        * `recommender.py`: Contains the logic for finding and recommending similar cities.
        * `theme.py`: Custom CSS injection for styling.
        * `variables.py`: Constant variables.
    