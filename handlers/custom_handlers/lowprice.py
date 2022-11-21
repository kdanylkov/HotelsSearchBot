from loader import bot
from telebot.types import Message
from states import UserStates
import json


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    msg = '''
    Запущен поиск по критерию: "Наименьшая цена".
В каком городе ищем?
    '''
    bot.send_message(message.chat.id, msg)
    bot.set_state(message.chat.id, state=UserStates.destination_id)


    


