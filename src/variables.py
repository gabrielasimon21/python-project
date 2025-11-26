RATING_COLUMNS = ["Culture", "Adventure", "Nature", "Beaches", "Nightlife", "Cuisine", "Wellness", "Urban", "Seclusion"]

REGIONS = ["World", "Europe", "Asia", "Africa", "North America", "South America", "Oceania"]

VARIABLE_DESCRIPTIONS = {
    "culture": "Represents how rich and accessible the cultural experiences are in a city.",
    "adventure": "Measures opportunities for adventure sports and outdoor activities.",
    "nature": "Captures how scenic and close to nature the city is.",
    "beaches": "Indicates the quality and availability of beaches nearby.",
    "nightlife": "Rates the vibrancy of nightlife and entertainment options.",
    "cuisine": "Represents the diversity and quality of local food experiences.",
    "wellness": "Captures how well the city supports relaxation and wellness tourism.",
    "urban": "Rates modernity, infrastructure, and urban experiences.",
    "seclusion": "Reflects how peaceful, remote, and less touristy the city is."
}

MONTHS = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

LIKED_CITIES = []


QUESTIONS = {
    "region": {
        "text": "🌏 To which region of the world would you like to travel?",
        "type": "select",
        "options": ["Africa", "Asia", "Europe",
                    "Middle East", "North America", 
                    "Oceania", "South America", "No specific region"],
        "mapping": {
            "Europe": "europe",
            "Asia": "asia",
            "Africa": "africa",     
            "North America": "north_america",   
            "South America": "south_america",
            "Oceania": "oceania",
            "Middle East": "middle_east",
            "No specific region": 0
        }
    },
    "ideal_durations": {
        "text": "🧳 How long do you plan to travel?",
        "type": "select",
        "options": ["For a Weekend", "For 4-5 days", "For 1 week to 10 days", "More than 2 weeks"],
        "mapping": {
            "For a Weekend": "Weekend",
            "For 4-5 days": "Short trip",
            "For 1 week to 10 days": "One week",
            "More than 2 weeks": "Long trip"
        }
    },
    "budget_level": {
        "text": "💰 What is your approximate budget for the trip?",
        "type": "select",
        "options": ["Low", "Medium", "High"],
        "mapping": {"Low": "Budget", "Medium": "Mid-range", "High": "Luxury"}
    },
    "month": {
        "text": "📅 In which month would you like to travel?",
        "type": "select",
        "options": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        "mapping": {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }
    },
    "avg_temp_monthly": {
        "text": "🌤️ What's your ideal weather?",
        "type": "select",
        "options": ["Very cold", "Cold", "Mild", "Warm", "Hot"],
        "mapping": {"Very cold": 0, "Cold": 1, "Mild": 2, "Warm": 3, "Hot": 4}
    },
    "culture": {
        "text": "🏰 How important is experiencing local culture when you travel?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "adventure": {
        "text": "🧗‍♂️ How important are adventure activities when you travel?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "nature": {
        "text": "🌳 How important is the presence of nature landscapes in your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "beaches": {
        "text": "🏖️ How important is having access to beaches on your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "nightlife": {
        "text": "🍸 How important is experiencing nightlife on your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "cuisine": {
        "text": "🥗 How important is trying local cuisine when you travel?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "wellness": {
        "text": "🧘‍♀️ How important are wellness and relaxation opportunities on your trip?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "urban": {
        "text": "🏙️ How important is it for your destination to be a modern, urban city?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
    "seclusion": {
        "text": "🎋 How important is it for your destination to be a secluded, peaceful area?",
        "type": "select",
        "options": ["Very important", "Important", "Somewhat important", "Slightly important", "Not important"],
        "mapping": {
            "Not important": 1,
            "Slightly important": 2,
            "Somewhat important": 3,
            "Important": 4,
            "Very important": 5 
        }
    },
}
