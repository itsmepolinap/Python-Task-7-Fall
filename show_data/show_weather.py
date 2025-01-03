import json

import pytz


def print_weather_data(record: dict):
    """
    Выводит данные о погоде из записи базы данных в читаемом формате.

    Args:
        record (dict): Запись из базы данных с полями created_at, query_data и response_data.

    Returns:
        None
    """
    created_at = record.get("created_at").astimezone(pytz.timezone('Europe/Moscow'))
    query_data = record.get("query_data")
    response_data = json.loads(record.get("response_data", "{}"))

    weather = response_data.get("weather", "Неизвестно")
    temp = response_data.get("temp", "Неизвестно")
    feels_like = response_data.get("feels_like", "Неизвестно")
    wind_speed = response_data.get("wind_speed", "Неизвестно")

    print(f"Текущее время: {created_at}")
    print(f"Название города: {query_data}")
    print(f"Погодные условия: {weather}")
    print(f"Текущая температура: {temp} С°")
    print(f"Ощущается как: {feels_like} С°")
    print(f"Скорость ветра: {wind_speed} м/c")