from loader import bot, storage
from telebot.types import Message
from states import UserStates
from keyboards.inline import cities_keyboard
import json
from utils.misc import get_location_options_list, get_locale_code
from rapid_api import fetch_locations_options


@bot.message_handler(state=UserStates.destination_id)
def get_city_name(message: Message):
    with open('dump_london.json', 'r', encoding='utf-8') as rf:
        locations_dump = json.load(rf)
    locations_options = get_location_options_list(locations_dump)
    if not message.text is None:
        locale_code = get_locale_code(message.text) 
        storage.set_data(message.chat.id, message.chat.id, 'locale', locale_code)
        
        #locations_options = fetch_locations_options(message.text, locale_code)
        bot.send_message(message.chat.id, 
            'Выберите искомый город из списка:', 
            reply_markup=cities_keyboard(locations_options))
    else:
        bot.send_message(message.chat.id, 'Вы должны ввести название города!')
