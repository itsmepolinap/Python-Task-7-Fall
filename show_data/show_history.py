from datetime import datetime
from typing import Dict, List

import pytz


def print_city_requests(data: List[Dict]):
    """
    Выводит нумерованный список городов и времени их запросов.

    Args:
        data (list): Список словарей, где каждый словарь содержит данные запроса.
            Каждый словарь должен содержать следующие ключи:
                - 'id': идентификатор записи
                - 'created_at': время создания запроса (datetime)
                - 'query_type': тип запроса
                - 'query_data': данные запроса
                - 'response_data': ответ на запрос

    """

    if not data:
        print('Нет данных.')

    for index, row in enumerate(data, 1):
        city = row['query_data']
        created_at = row['created_at'].astimezone(pytz.timezone('Europe/Moscow'))
        query_type = row['query_type']

        formatted_time = str(created_at) if isinstance(created_at, datetime) else created_at
        query_str = ' (Текущая локация)' if query_type == 'LOC' else ''
        print(f"{index}. {city}{query_str}, {formatted_time}")