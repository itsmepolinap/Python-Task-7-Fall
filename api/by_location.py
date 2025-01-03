import os

import geocoder
import requests
from dotenv import load_dotenv

load_dotenv()


def get_weather_data_by_coordinates(lat: float, lon: float):
    try:
        query = \
            {
                'lat': lat,
                'lon': lon,
                'appid': os.getenv('API'),
                'units': 'metric',
                'lang': 'ru'
            }

        loc = requests.get('http://api.openweathermap.org/data/2.5/weather', params=query)

        return loc.json()

    except requests.exceptions.RequestException as e:
        raise ConnectionError('Ошибка при получении даных о погоде: нет соединения с сервером')


def get_coordinates():
    try:
        geo = geocoder.ipinfo('me')
        return geo.latlng

    except ConnectionError as e:
        raise ConnectionError('Не удалось выполнить подключение к серверу для получения местоположения')