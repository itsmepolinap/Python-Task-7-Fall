from api.by_location import get_coordinates, get_weather_data_by_coordinates
from api.by_name import get_weather_data_by_name
from api.reformat_data import prepare_data_for_db
from database.database_manager import DatabaseManager
from show_data.show_history import print_city_requests
from show_data.show_weather import print_weather_data
from validate.validate_history import validate_city_number


class WeatherApp:
    def __init__(
            self,
            db: DatabaseManager
    ):
        """"""
        self._db = db

    def run(self):
        '''
        Запуск обработчика консольных команд.
        '''
        print('Приветствуем! \n')
        self._print_menu()

        self._start()

    def _print_menu(self):
        """
        Отображает меню для выбора действия пользователем.
        """
        print("0. Показать меню")
        print("1. Узнать погоду в городе")
        print("2. Узнать погоду по текущему местоположению")
        print("3. Посмотреть историю запросов")
        print("4. Выйти")

    def _handle_choice(self, choice):
        """
        Обрабатывает выбор пользователя и вызывает соответствующие функции.

        Args:
            choice (str): Введённый пользователем выбор.

        Raises:
            ValueError
        """
        if choice == "0":
            return self._print_menu()
        elif choice == "1":
            return self._get_weather_by_city()
        elif choice == "2":
            return self._get_weather_by_location()
        elif choice == "3":
            return self._view_history()
        elif choice == "4":
            return self._exit_app()

        raise ValueError(f'Вы ввели некорректные данные {choice}.')

    def _get_weather_by_city(self):
        """
        Запрашивает погоду для указанного города.
        """
        city = input("Введите название города: ")

        try:
            response_data = get_weather_data_by_name(city)
        except (TimeoutError, ConnectionError,) as err:
            print(err.args[0])
            return

        response_data = prepare_data_for_db('NAME', city, response_data)

        with self._db as db:
            db.insert_weather_request(response_data)
            weather_data = db.select_last_weather_request()

        print_weather_data(weather_data)


    def _get_weather_by_location(self):
        """
        Запрашивает погоду по текущему местоположению пользователя.
        """
        try:
            coordinates = get_coordinates()
        except (ConnectionError, TimeoutError,) as err:
            print(err.args[0])
            return

        try:
            response_data = get_weather_data_by_coordinates(*coordinates)
        except (ConnectionError, TimeoutError, ) as err:
            print(err.args[0])
            return

        response_data = prepare_data_for_db('LOC', '', response_data)

        with self._db as db:
            db.insert_weather_request(response_data)
            weather_data = db.select_last_weather_request()

        print_weather_data(weather_data)

    def _view_history(self):
        """
        Отображает историю последних запросов.
        """
        with self._db as db:
            weather_list = db.select_weather_requests()

        print_city_requests(weather_list)
        city_number = input('Введите номер города, в котором хотите просмотреть погоду: ')

        try:
            city_number = validate_city_number(city_number, weather_list)
        except ValueError as err:
            print(err.args[0])
            return self._view_history()

        print_weather_data(weather_list[city_number])

    def _exit_app(self):
        """
        Выход из приложения.
        """
        print("Выход из приложения...")
        exit()

    def _start(self):
        while True:
            try:
                choice = input('Введите команду: ')
                try:
                    self._handle_choice(choice)
                except ValueError as err:
                    print(err.args[0])
                    self._start()
            except KeyboardInterrupt:
                self._exit_app()


# Создание экземпляра приложения и запуск
if __name__ == "__main__":
    app = WeatherApp()
    app.run()
