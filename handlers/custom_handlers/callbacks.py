from loader import bot, calendar_1_callback
from telebot.types import CallbackQuery
from filters import destinations_factory
from datetime import datetime, timedelta
from states import UserStates
from keyboards.inline import create_calendar_keyboard, calendar_keyboard
from utils import ask_for_input_confirmation
from database import add_query
from rapid_api import get_api_hotels_and_send_to_user


@bot.callback_query_handler(func=None, locations_config=destinations_factory.filter())
def callback_location_choice_handler(call: CallbackQuery):

    ID = call.message.chat.id
    bot.delete_message(call.message.chat.id, call.message.message_id)

    callback_data: dict = destinations_factory.parse(callback_data=call.data)

    destination_id = callback_data['destination_id']

    with bot.retrieve_data(call.message.chat.id) as data:                   #type: ignore
        destination_name = data['names_and_ids'][destination_id]
        data['destination_name'] = destination_name
        data['destination_id'] = int(destination_id)
        data.pop('names_and_ids')

    print(data)

    bot.set_state(ID, UserStates.arrival_date)

    now = datetime.now()
    bot.send_message(
            ID,
            f'Выберите дату заезда:',
            reply_markup=calendar_keyboard(now.year, now.month)
            )


@bot.callback_query_handler(state=UserStates.arrival_date,
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_arrival(call: CallbackQuery):

    arrival_date = create_calendar_keyboard(
            call=call,
            text_if_correct='Дата заезда',
            text_if_incorrect='Дата заезда не может быть раньше сегодняшнего дня',
            offset_date=datetime.now(),
            bot=bot,
        )
    if arrival_date:
        with bot.retrieve_data(call.message.chat.id) as data:                        #type: ignore
            data['arrival_date'] = arrival_date

        bot.set_state(call.message.chat.id, UserStates.departure_date)

        bot.send_message(
                call.message.chat.id,
                f'Выберите дату выезда:',
                reply_markup=calendar_keyboard(arrival_date.year, arrival_date.month)
                )


@bot.callback_query_handler(state=UserStates.departure_date,
    func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def callback_departure(call: CallbackQuery):

    with bot.retrieve_data(call.message.chat.id) as data:        #type: ignore  
        offset_date = data['arrival_date'] + timedelta(days=1)   

    departure_date = create_calendar_keyboard(
            call=call,
            text_if_correct='Дата выезда',
            text_if_incorrect='Дата выезда не может не может быть раньше даты заезда',
            offset_date=offset_date,
            bot=bot,
        )

    if departure_date:
        with bot.retrieve_data(call.message.chat.id) as data:           #type: ignore
            data['departure_date'] = departure_date
            print(data)

        bot.set_state(call.message.chat.id, UserStates.hotels_amount)
        bot.send_message(call.message.chat.id, f'Введите количество отелей для поиска (максимум 25)')


@bot.callback_query_handler(state=UserStates.ask_for_photos, func=lambda c: c.data.endswith('photos'))
def callback_download_photos(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'yes_photos':
        bot.send_message(call.message.chat.id, 'Введите количество фотографий (максимум 5)')
        bot.set_state(call.message.chat.id, UserStates.photos_amount)
    elif call.data == 'no_photos':
        with bot.retrieve_data(call.message.chat.id) as data:                       #type: ignore
            data['photos_amount'] = 0

        bot.set_state(call.message.chat.id, UserStates.confirm_data)
        ask_for_input_confirmation(call.message.chat.id)


@bot.callback_query_handler(state=UserStates.confirm_data, func=lambda c: c.data.endswith('confirm'))
def callback_data_input_confirmation(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    match call.data:

        case 'reset_confirm':
            bot.send_message(call.message.chat.id, 'Хорошо, начнем заново.\nВведите город для поиска отелей:')
            bot.set_state(call.message.chat.id, UserStates.destination_id)

        case 'cancel_confirm':
            bot.delete_state(call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Поиск отменен')

        case 'yes_confirm':
            with bot.retrieve_data(call.message.chat.id) as data:                   #type: ignore
                data['query_id'] = add_query(data)

            with open('static/waiting.tgs', 'rb') as sticker:
                bot.send_sticker(call.message.chat.id, sticker)

            bot.set_state(call.message.chat.id, UserStates.wait_for_results)
            get_api_hotels_and_send_to_user(data)

            bot.delete_state(call.message.chat.id)



