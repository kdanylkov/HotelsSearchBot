from telebot import TeleBot
from filters import LocationsCallbackFilter, HotelAmount, PhotosAmount
from telebot.custom_filters import StateFilter



def set_custom_filters(bot: TeleBot) -> None:
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(LocationsCallbackFilter())
    bot.add_custom_filter(HotelAmount())
    bot.add_custom_filter(PhotosAmount())
