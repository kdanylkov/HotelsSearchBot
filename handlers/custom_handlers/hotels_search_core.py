from loader import bot, storage
from telebot.types import Message
from states import UserStates
from keyboards.inline import cities_keyboard
import json
from utils.misc import get_location_options_list, get_locale_code_and_currency
from rapid_api import fetch_locations_options


@bot.message_handler(state=UserStates.destination_id)
def get_city_name(message: Message):

    with open('dump_london.json', 'r', encoding='utf-8') as rf:
        locations_dump = json.load(rf)
    locations_options = get_location_options_list(locations_dump)

    with open('static/waiting.tgs', 'rb') as sticker:
        bot.send_sticker(message.chat.id, sticker)

    if message.text is not None:
        locale, currency = get_locale_code_and_currency(message.text) 
        storage.set_data(message.chat.id, message.chat.id, 'locale', locale)
        storage.set_data(message.chat.id, message.chat.id, 'currency', currency)
        
        #locations_options = fetch_locations_options(message.text, locale)
        if locations_options:
            markup = cities_keyboard(locations_options)
            bot.send_message(message.chat.id, 
                'Выберите искомый город из списка:', 
                reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 
            f'Не удалось найти город с таким названием: {message.text}')
            bot.delete_state(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Вы должны ввести название города!')






