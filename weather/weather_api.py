# weather/weather_api.py
import requests
from config import WEATHER_API_KEY, WEATHER_API_URL

def get_weather(location: str):
    """
    WeatherAPIから天気を取得
    """
    params = {
        'key': WEATHER_API_KEY,
        'q': location,
        'aqi': 'no'
    }
    res = requests.get(WEATHER_API_URL, params=params)
    data = res.json()
    weather = {
        'text': data['current']['condition']['text'],
        'temp': data['current']['temp_c'],
        'wind_kph': data['current']['wind_kph'],
        'humidity': data['current']['humidity']
    }
    return weather
