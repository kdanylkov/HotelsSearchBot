from loader import bot
from telebot.types import Message
from states import UserStates
from keyboards.inline import destinations_keyboard, if_need_photos_keyboard
from utils import get_locale, ask_for_input_confirmation
from rapid_api import get_api_destinations_options
from database import add_user


@bot.message_handler(state=UserStates.destination_id)
def get_city_name(message: Message):
    
    add_user(message)
    
    #with open('dump_london.json', 'r', encoding='utf-8') as rf:
    #    locations_dump = json.load(rf)
    #destinations_list = get_destination_options_list(locations_dump)

    locale = get_locale(message.text)       #type: ignore 
    with open('static/waiting.tgs', 'rb') as sticker:
        bot.send_sticker(message.chat.id, sticker)

    destinations_list = get_api_destinations_options(message.text, locale)   #type: ignore
    if destinations_list:

        with bot.retrieve_data(message.chat.id) as data:                    #type: ignore
            data['names_and_ids'] = {des['id']: des['name'] for des in destinations_list}
            data['locale'] = locale
            data['user_id'] = message.from_user.id

        markup = destinations_keyboard(destinations_list)
        bot.send_message(message.chat.id, 
            'Выберите искомый город из списка:', 
            reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 
        f'Не удалось найти город с таким названием: {message.text}')
        bot.delete_state(message.chat.id)


@bot.message_handler(state=UserStates.hotels_amount, is_hotels_amt_correct=True)
def hotels_amount_correct(message: Message):
    with bot.retrieve_data(message.chat.id) as data:                     #type: ignore
        data['hotels_amount'] = message.text

    bot.send_message(message.chat.id, 'Загружать фотографии?', reply_markup=if_need_photos_keyboard())
    bot.set_state(message.chat.id, UserStates.ask_for_photos)

            
@bot.message_handler(state=UserStates.hotels_amount, is_hotels_amt_correct=False)
def hotels_amount_incorrect(message: Message):
    bot.send_message(message.chat.id,
            'Количество отелей должно быть введено цифрой от 1 до 25!')


@bot.message_handler(state=UserStates.ask_for_photos, content_types=['text'])
def ask_for_photos_keyboard_input(message):
    bot.send_message(message.chat.id, 'Нажмите одну из кнопок⬆️')


@bot.message_handler(state=UserStates.photos_amount, is_photos_amt_correct=True)
def photos_amount_correct(message: Message):
    with bot.retrieve_data(message.chat.id) as data:                      #type: ignore
        data['photos_amount'] = message.text

    bot.set_state(message.chat.id, UserStates.confirm_data)
    ask_for_input_confirmation(message.chat.id)


@bot.message_handler(state=UserStates.photos_amount, is_photos_amt_correct=False)
def photos_amount_incorrect(message: Message):
    bot.send_message(message.chat.id,
            'Количество фотографий должно быть введено цифрой от 1 до 5!')


@bot.message_handler(state=UserStates.arrival_date, content_types=['text'])
def calendar_arrival_state_keyboard_input(message):
    bot.send_message(message.chat.id, 'Чтобы ввести дату, воспользуйтесь кнопками календаря⬆️')


@bot.message_handler(state=UserStates.departure_date, content_types=['text'])
def calendar_departure_state_keyboard_input(message):
    bot.send_message(message.chat.id, 'Чтобы ввести дату, воспользуйтесь кнопками календаря⬆️')


@bot.message_handler(state=UserStates.confirm_data, content_types=['text'])
def confirmation_keyboard_input(message):
    bot.send_message(message.chat.id, 'Нажмите одну из кнопок⬆️')


@bot.message_handler(state=UserStates.wait_for_results)
def waiting_for_result(message: Message):
    bot.send_message(message.chat.id, 'Результаты поиска загружаются, ожидайте!')


@bot.message_handler(state=UserStates.currency)
def currency_choice_keyboard_input(message: Message):
    bot.send_message(message.chat.id, 'Нажмите одну из кнопок⬆️')

