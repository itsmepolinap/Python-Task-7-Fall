import sqlite3
from pathlib import Path

from database.database_manager import DatabaseManager


def create_weather_requests_db(file_path: str):
    """
    Создает файл SQLite базы данных и таблицу `weather_requests`.

    Args:
        file_path (str): Путь к файлу базы данных (например, 'database/weather_requests.db').

    Returns:
        None
    """
    db_path = Path(file_path)

    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        return

    try:
        with DatabaseManager(file_path) as db_manager:
            db_manager.create_weather_requests_table()

    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")

# Пример использования
if __name__ == "__main__":
    create_weather_requests_db("dataweather_requests.db")

    # Пример добавления записи
    with DatabaseManager("weather_requests.db") as db_manager:
        db_manager.insert_weather_request({
            "query_type": "CITY",
            "query_data": "London",
            "response_data": "{\"temp\": 15, \"humidity\": 80}"
        })

        # Пример выборки записей
        records = db_manager.select_weather_requests()
        for record in records:
            print(record)