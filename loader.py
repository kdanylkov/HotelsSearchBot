'''Модуль для создания экземпляров классов TeleBot, Calendar'''

from config_data import config
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData

bot = TeleBot(token=config.BOT_TOKEN)

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData('calendar_1', 'action', 'year', 'month', 'day')


