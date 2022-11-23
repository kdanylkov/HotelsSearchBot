from loader import bot, storage
from telebot.types import Message
from states import UserStates
from keyboards.inline import destinations_keyboard, confirm_query_keyboard
import json
from utils.misc import get_destination_options_list, get_locale_code_and_currency, get_query_confirmation_text, set_id_to_name_data
from rapid_api import get_api_destinations_options


@bot.message_handler(state=UserStates.destination_id)
def get_city_name(message: Message):

    with open('dump_london.json', 'r', encoding='utf-8') as rf:
        locations_dump = json.load(rf)
    destinations_list = get_destination_options_list(locations_dump)

    with open('static/waiting.tgs', 'rb') as sticker:
        bot.send_sticker(message.chat.id, sticker)

    if message.text is not None:
        locale, currency = get_locale_code_and_currency(message.text) 
        storage.set_data(message.chat.id, message.chat.id, 'locale', locale)
        storage.set_data(message.chat.id, message.chat.id, 'currency', currency)
        
        destinations_list = get_api_destinations_options(message.text, locale)
        if destinations_list:
            set_id_to_name_data(storage, message.chat.id, destinations_list)

            markup = destinations_keyboard(destinations_list)
            bot.send_message(message.chat.id, 
                'Выберите искомый город из списка:', 
                reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 
            f'Не удалось найти город с таким названием: {message.text}')
            bot.delete_state(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Вы должны ввести название города!')


@bot.message_handler(state=UserStates.hotels_amount, is_hotels_amt_correct=True)
def hotels_amount_correct(message: Message):
    storage.set_data(message.chat.id, message.chat.id, 'hotels_amount', message.text) 

    txt = get_query_confirmation_text(storage, message.chat.id)
    #bot.send_message(message.chat.id, text, reply_markup=confirm_query())
    print('our_data:', txt)

            


@bot.message_handler(state=UserStates.hotels_amount, is_hotels_amt_correct=False)
def hotels_amount_incorrect(message: Message):
    bot.send_message(message.chat.id,
            'Количество отелей должно быть цифрой от 1 до 25!')


