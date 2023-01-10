from loader import bot
from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS

@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    '''Обработчик для команды "help". Вызывает справку для пользователя.'''

    help_text = ''
    for command in DEFAULT_COMMANDS:
        help_text = ''.join([help_text, '/', command[0], ' - <b>', command[1], '</b>\n'])
    bot.send_message(message.chat.id, help_text, parse_mode='html')

