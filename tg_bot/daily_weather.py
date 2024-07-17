
import requests
from datetime import datetime, timedelta, timezone, date, time

api_key = '804d8ac00e928e9c82b60a1e89929379'  # Replace with your actual OpenWeatherMap API key


def get_daily_weather_data(lat, lon, lang='ru'):
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'lang': lang,
        'units': 'metric'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        forecasts = data['list']

        # Get the timezone from OpenWeatherMap response
        city_timezone_offset = data['city']['timezone']
        city_timezone = timezone(timedelta(seconds=city_timezone_offset))

        now = datetime.now(tz=city_timezone)
        max_time = datetime.combine(now.date(), time.max).replace(tzinfo=city_timezone)
        max_time = max_time + timedelta(minutes=30)

        print(f"Current time: {now}")  # Для отладки
        print(f"End of the day: {max_time}")  # Для отладки

        max_temp = float('-inf')
        min_temp = float('inf')
        max_rain = 0  # Initialize to 0 for rain if there's no rain data
        max_rain_time = None
        max_wind = 0  # Initialize to 0
        max_wind_time = None

        for forecast in forecasts:
            forecast_time = datetime.fromtimestamp(forecast['dt'], tz=city_timezone)

            if now <= forecast_time <= max_time:
                temp = forecast['main']['temp']
                if temp > max_temp:
                    max_temp = temp
                if temp < min_temp:
                    min_temp = temp

                if 'rain' in forecast and '3h' in forecast['rain'] and forecast['rain']['3h'] > max_rain:
                    max_rain = forecast['rain']['3h']
                    max_rain_time = forecast_time

                if 'wind' in forecast and 'speed' in forecast['wind'] and forecast['wind']['speed'] > max_wind:
                    max_wind = forecast['wind']['speed']
                    max_wind_time = forecast_time

        if max_rain_time is None:
            rain_str = "По прогнозу дождя не будет."
        else:
            rain_str = f"{max_rain} мм в {max_rain_time.strftime('%H:%M')}"
        print("дэйли ведер работает!!!")

        weather_info = [(
            f"Максимальная температура: {max_temp if max_temp != float('-inf') else 'нет данных'}°C\n"
            f"Минимальная температура: {min_temp if min_temp != float('inf') else 'нет данных'}°C\n"
            f"Максимальный дождь: {rain_str}\n"
            f"Максимальный ветер: {max_wind if max_wind != 0 else 'нет данных'} м/с в {max_wind_time.strftime('%H:%M') if max_wind_time else 'нет данных'}"
        ), max_temp, min_temp, rain_str, max_wind]
        return weather_info
    else:
        return f"Не удалось получить данные о погоде. Код ошибки: {response.status_code}"


print(get_daily_weather_data(55.7558, 37.6173))  # Начальной точкой данных является Москва