from loader import bot

from telebot.types import Message


@bot.message_handler(state=None)
def undefined(message: Message) -> None:
    '''Обработчик для сообщений пользователя, которые не подпадают ни под один из фильтров'''
    with open('static/dont_know.tgs', 'rb') as sticker:
        bot.send_sticker(message.chat.id, sticker=sticker)
    bot.reply_to(message, 'Я тебя не понимаю😢 Напиши "/help"')
