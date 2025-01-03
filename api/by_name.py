import os

import requests

from dotenv import load_dotenv

load_dotenv()


def get_location_by_name(location: str):
    try:
        query = {'q': location, 'limit': 1, 'appid': os.getenv('API')}
        loc = requests.get('http://api.openweathermap.org/geo/1.0/direct', params=query)
        if not loc.status_code == 200:
            raise ConnectionError('Локация не найдена.')

        loc = loc.json()

        if not loc:
            raise ConnectionError('Локация не найдена.')

        return {'lat': loc[0]['lat'], 'lon': loc[0]['lon']}

    except requests.exceptions.RequestException as e:
        raise ConnectionError('Ошибка при получении геоданных: нет соединения с сервером')


def get_weather_data_by_name(location: str):
    coordinates = get_location_by_name(location)

    try:
        query = \
            {
                'lat': coordinates['lat'],
                'lon': coordinates['lon'],
                'appid': os.getenv('API'),
                'units': 'metric',
                'lang': 'ru'
            }

        loc = requests.get('http://api.openweathermap.org/data/2.5/weather', params=query)

        return loc.json()

    except requests.exceptions.RequestException as e:
        raise ConnectionError('Ошибка при получении даных о погоде: нет соединения с сервером')
