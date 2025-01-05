import datetime
import sqlite3


class DatabaseManager:
    """
    Контекстный менеджер для управления подключением к SQLite базе данных.
    """

    def __init__(self, file_path: str):
        """
        Инициализирует менеджер базы данных с указанным путем к файлу базы данных.

        Args:
            file_path (str): Путь к файлу SQLite базы данных.
        """
        self.file_path = file_path
        self.connection = None

    def __enter__(self):
        """
        Устанавливает соединение с базой данных SQLite.

        Returns:
            sqlite3.Connection: Объект соединения с SQLite.
        """
        self.connection = sqlite3.connect(self.file_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Закрывает соединение с базой данных SQLite.

        Args:
            exc_type: Тип исключения (если есть).
            exc_value: Значение исключения (если есть).
            traceback: Объект трассировки (если есть).
        """
        if self.connection:
            self.connection.close()

    def create_weather_requests_table(self):
        """
        Создает таблицу `weather_requests` в базе данных.

        Returns:
            None
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE weather_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATETIME NOT NULL,
                query_type VARCHAR(4) NOT NULL,
                query_data VARCHAR(256) NOT NULL,
                response_data TEXT NOT NULL
            );
            """
        )

    def insert_weather_request(self, data: dict):
        """
        Вставляет запись в таблицу `weather_requests`.

        Args:
            data (dict): Словарь с данными для вставки. Ключи должны соответствовать названиям полей таблицы
                        (кроме `created_at`, который задается автоматически).

        Returns:
            None
        """
        cursor = self.connection.cursor()

        created_at = datetime.datetime.now(datetime.UTC)

        query = """
        INSERT INTO weather_requests (created_at, query_type, query_data, response_data)
        VALUES (:created_at, :query_type, :query_data, :response_data)
        """

        data["created_at"] = created_at

        try:
            cursor.execute(query, data)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка вставки данных в SQLite: {e}")

    def select_weather_requests(self, amount: int):
        """
        Получает последние 5 записей из таблицы `weather_requests`.

        Returns:
            list: Список словарей с данными из таблицы `weather_requests`.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                
                "SELECT id, created_at, query_type, query_data, response_data "
                "FROM weather_requests "
                "ORDER BY created_at DESC "
                f"LIMIT {amount}"
            )
            rows = cursor.fetchall()

            result = [
                {
                    "id": row[0],
                    "created_at": datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f%z'),
                    "query_type": row[2],
                    "query_data": row[3],
                    "response_data": row[4]
                }
                for row in rows
            ]

            return result

        except sqlite3.Error as e:
            print(f"Ошибка выборки данных из SQLite: {e}")
            return []

    def select_last_weather_request(self):
        """
        Получает последнюю из таблицы `weather_requests`.

        Returns:
            list: Список словарей с данными из таблицы `weather_requests`.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT id, created_at, query_type, query_data, response_data
                FROM weather_requests
                ORDER BY created_at DESC
                LIMIT 1
                """
            )
            row = cursor.fetchone()

            return {
                "id": row[0],
                "created_at": datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f%z'),
                "query_type": row[2],
                "query_data": row[3],
                "response_data": row[4]
            }

        except sqlite3.Error as e:
            print(f"Ошибка выборки данных из SQLite: {e}")
            return []