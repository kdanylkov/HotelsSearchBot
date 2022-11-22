from config_data import config
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData('calendar_1', 'action', 'year', 'month', 'day')


