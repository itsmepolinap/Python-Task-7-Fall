from app.weather import WeatherApp
from database.database_init import create_weather_requests_db
from database.database_manager import DatabaseManager

if __name__ == '__main__':
    create_weather_requests_db("database/weather_requests.db")
    app = WeatherApp(DatabaseManager("database/weather_requests.db"))
    app.run()