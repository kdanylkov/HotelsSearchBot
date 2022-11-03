from loader import bot
from telebot.types import Message

@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    '''Обработчик для команды "help". Вызывает справку для пользователя.'''
    bot.send_message(message.chat.id, 'Напиши "привет" или нажми "/helloworld"')
