import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get API key (local: from .env, cloud: from secrets)
API_KEY = os.getenv("WEATHERAPI_KEY") or st.secrets.get("WEATHERAPI_KEY")

if not API_KEY:
    st.error("API Key not found. Please set it in .env for local or as a secret for deployment.")
else:
    # App title
    st.title("🌤 Weather Forecast")

    # Get city input from the user
    city = st.text_input("Enter the city name:")

    if city:
        # WeatherAPI endpoint
        BASE_URL = "http://api.weatherapi.com/v1/current.json"

        # Make API request
        params = {"key": API_KEY, "q": city, "aqi": "no"}
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract weather data
            location = data["location"]["name"]
            region = data["location"]["region"]
            country = data["location"]["country"]
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            wind_kph = data["current"]["wind_kph"]
            humidity = data["current"]["humidity"]

            # Display weather information
            st.subheader(f"Weather in {location}, {region}, {country}:")
            st.write(f"*Condition:* {condition}")
            st.write(f"*Temperature:* {temp_c}°C")
            st.write(f"*Wind Speed:* {wind_kph} km/h")
            st.write(f"*Humidity:* {humidity}%")
        else:
            st.error("City not found. Please try again.")