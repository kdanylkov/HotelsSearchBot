from telebot.types import BotCommand
from telebot import TeleBot
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    '''Функция для создания меню команд бота.'''
    bot.set_my_commands([BotCommand(com, name) for com, name in DEFAULT_COMMANDS])

