import json


def prepare_data_for_db(query_type: str, query_data: str, query_result):
    weather = \
        {
            'weather': query_result.get('weather')[0].get('description').capitalize(),
            'temp': int(query_result.get('main').get('temp')),
            'wind_speed': query_result.get('wind').get('speed'),
            'feels_like': int(query_result.get('main').get('feels_like'))
        }

    return {'query_type': query_type, 'query_data': query_data,
            'response_data': json.dumps(weather, ensure_ascii=False)}
