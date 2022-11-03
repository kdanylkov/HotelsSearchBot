from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    '''Обработчик для запуска бота и команды "start"'''
    with open('static/hi_duck.tgs', 'rb') as sticker:
        bot.send_sticker(chat_id=message.chat.id, sticker=sticker)

    name = f'{message.from_user.first_name}'
    greet_message = f'Добро пожаловать, <b>{name}</b>!\nДля получения справки нажми /help'

    bot.send_message(chat_id=message.chat.id, text=greet_message, parse_mode='html')
    


