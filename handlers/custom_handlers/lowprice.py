from loader import bot
from telebot.types import Message
from states import UserStates


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    chat_id = message.chat.id
    msg = '''
    Запущен поиск по критерию: "Наименьшая цена".
В каком городе ищем?
    '''
    bot.send_message(chat_id, msg)
    bot.set_state(chat_id, state=UserStates.destination_id)
    with bot.retrieve_data(message.chat.id) as data:
        data['sortOrder'] = 'PRICE'



    


