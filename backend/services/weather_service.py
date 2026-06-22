import requests
from dotenv import load_dotenv
import os 

load_dotenv()


def get_weather(city):

    

    API_KEY =  os.getenv("WEATHER_API_KEY")

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    data = requests.get(url).json()

    if "list" not in data:
        raise Exception("Weather API failed")

    # take next 24h forecast (important upgrade)
    next_hours = data["list"][:8]   # 3-hour steps × 8 = 24h

    temp = sum([x["main"]["temp"] for x in next_hours]) / len(next_hours)
    humidity = sum([x["main"]["humidity"] for x in next_hours]) / len(next_hours)

    rainfall = sum([
        x.get("rain", {}).get("3h", 0) for x in next_hours
    ])

    return temp, humidity, rainfall