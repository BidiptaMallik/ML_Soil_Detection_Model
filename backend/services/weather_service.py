import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather(city):
    API_KEY = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    data = requests.get(url).json()

    if "main" not in data:
        raise Exception("Weather API failed")

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temp, humidity, rainfall