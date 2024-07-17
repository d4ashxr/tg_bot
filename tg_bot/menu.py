import telebot
from telebot import types
import requests
from daily_weather import get_daily_weather_data  # Исправлено для правильного импорта функции
from sql import daily_clothes_choise  # Импорт функции clothes_choise
from what_to_wear_now import clothes_choice

bot = telebot.TeleBot('7403947420:AAH75OlgZgK8sF5FcZnb_uJq1e0U2dF3KN4')
api_key = '804d8ac00e928e9c82b60a1e89929379'  # Replace with your actual OpenWeatherMap API key

city_coords = {
    'msk': (55.7558, 37.6173),  # Moscow
    'spb': (59.9343, 30.3351),  # Saint Petersburg
    'ekb': (56.8389, 60.6057),  # Yekaterinburg
    'psk': (57.8194, 28.3319)  # Pskov
}

city_names_cords = {
    'msk': 'moscow?lat=55.755863&lon=37.6177',  # Moscow
    'spb': 'saint-petersburg',  # Saint Petersburg
    'ekb': 'yekaterinburg',  # Yekaterinburg
    'psk': 'pskov'  # Pskov
}

city_names = {
    'msk': 'Москва',
    'spb': 'Питер',
    'ekb': 'Екатеринбург',
    'psk': 'Псков'
}


def get_weather_data(lat, lon, lang='ru'):
    url = f"https://api.openweathermap.org/data/2.5/weather"
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
        weather = data['weather'][0]
        main = data['main']

        temperature = main['temp']
        feels_like = main['feels_like']
        condition = weather['description']
        humidity = main['humidity']
        pressure = main['pressure']

        weather_info = [(
            f"Температура: {temperature}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Состояние: {condition}\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {pressure} мм рт.ст."
        ), temperature, feels_like, condition, humidity, pressure]
        return weather_info
    else:
        return f"Не удалось получить данные о погоде. Код ошибки: {response.status_code}"


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location_button = types.KeyboardButton('Отправить локацию', request_location=True)
    help_button = types.KeyboardButton('Помощь')
    markup.add(location_button)
    markup.add(help_button)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}! Бот запущен, поделитесь вашей локацией для прогноза погоды.',
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        'Этот бот поможет вам быстро узнать погоду. Введите /start и поделитесь вашей локацией для начала.',
        reply_markup=main_menu()
    )


@bot.message_handler(content_types=['location'])
def location_received(message):
    lat = message.location.latitude
    lon = message.location.longitude
    print(f"Received location: Latitude: {lat}, Longitude: {lon}")  # Print геопозиции

    # Additional markup and user feedback
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Погода сейчас'))
    markup.add(types.KeyboardButton('Погода на день'))
    markup.add(types.KeyboardButton('Назад'))

    bot.send_message(
        message.chat.id,
        'Отлично! Локация получена. Выберите действие из меню:',
        reply_markup=markup
    )

    # Store the user's location with the chat ID for future operations
    bot.user_data[message.chat.id] = (lat, lon)


@bot.message_handler(content_types=['text'])
def action_selection(message):
    lat, lon = bot.user_data.get(message.chat.id, (None, None))

    if message.text == 'Погода сейчас':
        if lat is not None and lon is not None:
            weather_info = get_weather_data(lat, lon)
            if isinstance(weather_info, str):  # Check for error message
                bot.send_message(message.chat.id, weather_info)
                return

            recommendation = clothes_choice(weather_info)
            url = f'https://yandex.ru/pogoda/?lat={lat}&lon={lon}'
            markup = types.InlineKeyboardMarkup()
            recommend_button = types.InlineKeyboardButton('Рекомендации по одежде', callback_data='clothes_recommendation_now')
            button = types.InlineKeyboardButton('Посмотреть на сайте', url=url)
            markup.add(recommend_button)
            markup.add(button)
            bot.send_message(
                message.chat.id,
                f'Текущая погода:\n{weather_info[0]}',
                reply_markup=markup
            )
        else:
            bot.send_message(message.chat.id, 'Локация не найдена. Пожалуйста, отправьте свою локацию снова, для этого используйте команду /start..')

    elif message.text == 'Погода на день':
        if lat is not None and lon is not None:
            weather_info = get_daily_weather_data(lat, lon)
            if isinstance(weather_info, str):  # Check for error message
                bot.send_message(message.chat.id, weather_info)
                return

            recommendation = daily_clothes_choise(weather_info)
            url = f'https://yandex.ru/pogoda/?lat={lat}&lon={lon}'
            markup = types.InlineKeyboardMarkup()
            recommend_button = types.InlineKeyboardButton('Рекомендации по одежде', callback_data='clothes_recommendation')
            button = types.InlineKeyboardButton('Посмотреть на сайте', url=url)
            markup.add(recommend_button)
            markup.add(button)
            bot.send_message(
                message.chat.id,
                f'Погода на день:\n{weather_info[0]}',
                reply_markup=markup
            )
        else:
            bot.send_message(message.chat.id, 'Локация не найдена. Пожалуйста, отправьте свою локацию снова, для этого используйте команду /start.')

    elif message.text == 'Помощь':
        help(message)
    elif message.text == 'Назад':
        bot.send_message(
            message.chat.id,
            'Возвращаемся в главное меню',
            reply_markup=main_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, используйте меню',
            reply_markup=main_menu()
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith('clothes_recommendation'))
def send_clothes_recommendation(call):
    lat, lon = bot.user_data.get(call.message.chat.id, (None, None))

    if call.data == 'clothes_recommendation_now':
        weather_info = get_weather_data(lat, lon)
        if weather_info != "Не удалось получить данные о погоде. Код ошибки: 400":
            recommendation = clothes_choice(weather_info)
    else:
        weather_info = get_daily_weather_data(lat, lon)
        if weather_info != "Не удалось получить данные о погоде. Код ошибки: 400":
            recommendation = daily_clothes_choise(weather_info)

    # Construct the recommendation message
    recommendation_message = "Рекомендации по одежде:\n"
    for key, items in recommendation.items():
        recommendation_message += f"{key}\n"
        for item in items:
            recommendation_message += f"- {item}\n"

    # Send the recommendation message
    bot.send_message(call.message.chat.id, recommendation_message)


# Ensure the bot stores user data
bot.user_data = {}

# Ensure the bot runs
bot.polling(none_stop=True)