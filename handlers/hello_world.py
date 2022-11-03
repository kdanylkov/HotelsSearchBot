from loader import bot
from keyboards.inline import how_are_you_reply
from telebot.types import Message

def hi_reply(message: Message) -> None:
    with open('static/hi.tgs', 'rb') as sticker:
        bot.send_sticker(message.chat.id, sticker=sticker)

    bot.reply_to(message, \
            f'Привет и тебе, <b>{message.from_user.first_name}</b>!',\
            parse_mode='html')
    bot.send_message(message.chat.id, 'Как у тебя сегодня дела?😃', reply_markup=how_are_you_reply())


@bot.message_handler(commands=['helloworld'])
def hello_world(message: Message) -> None:
    '''Обработчик для обработки команды "helloworld"'''
    hi_reply(message)


@bot.message_handler(content_types=['text'], func=lambda m: 'привет' in m.text.lower())
def hello(message: Message) -> None:
    '''
    Обработчик для обратотки текста, содержащего в себе слово "привет". Функционал совпадает с\
    командой "helloworld"
    '''
    hi_reply(message)



