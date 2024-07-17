import telebot
from geopy.geocoders import Nominatim
from telebot import types

API_TOKEN = '7231038692:AAEsZL1uRK9W0TtNUQMZUGhARY10lU8ZWWc'
bot = telebot.TeleBot(API_TOKEN)

geolocator = Nominatim(user_agent="geoapiExercises")


def get_location_name(lat, lon):
    location = geolocator.reverse((lat, lon), language='en')
    if location:
        print(location, location.address)
        return location.address
    else:
        return "Location not found"


def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_geo = types.KeyboardButton(text="Send location", request_location=True)
    markup.add(button_geo)
    bot.send_message(message.chat.id, "Welcome! Please share your location.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location is not None:
        lat = message.location.latitude
        lon = message.location.longitude
        print(f"Received location: Latitude: {lat}, Longitude: {lon}")  # Print геопозиции
        location_name = get_location_name(lat, lon)


def get_daily_weather_data(lat, lon):
    # Your implementation for getting daily weather data
    return "Mock weather data"


bot.polling(none_stop=True)
