from typing import Dict, List


def validate_city_number(number: str, weather_data: List[Dict]) -> int:
    """
    Валидирует данные о городе, введенные пользователем и возвращает целочисленное значение, соответствующее
    введенной строке.

    Args:
        number (str): Данные, введенные пользователем.
        weather_data (list[dict]): Данные о погоде из БД.

    Raises:
        ValueError

    Returns:

    """

    _DATA_LEN = len(weather_data)

    if not number.isdigit():
        raise ValueError('Значение должно быть целочисленным.')

    number = int(number)

    if number not in range(1, _DATA_LEN):
        raise ValueError(f'Введите значение от 1 до {_DATA_LEN}')

    return number
