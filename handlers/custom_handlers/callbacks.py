from loader import bot, storage, calendar_1_callback
from telebot.types import CallbackQuery
from filters import destinations_factory
from datetime import datetime, timedelta
from states import UserStates
from keyboards.inline import create_calendar_keyboard, calendar_keyboard


def delete_inline_markup(msg):
    bot.edit_message_text(msg.text, msg.chat.id, msg.message_id, reply_markup=None)


@bot.callback_query_handler(func=lambda call: True, locations_config=destinations_factory.filter())
def callback_location_choice_handler(call: CallbackQuery):

    ID = call.message.chat.id
    bot.delete_message(call.message.chat.id, call.message.message_id)

    callback_data: dict = destinations_factory.parse(callback_data=call.data)

    destination_id = callback_data['destination_id']

    with bot.retrieve_data(call.message.chat.id) as data:
        destination_name = data['names_and_ids'][destination_id]
        data['destination_name'] = destination_name
        data['destination_id'] = int(destination_id)
        data.pop('names_and_ids')

    bot.set_state(ID, UserStates.arrival_date)

    bot.send_message(
            ID,
            f'Выберите дату заезда:',
            reply_markup=calendar_keyboard
            )

    data = storage.get_data(ID, ID)
    print(data)


@bot.callback_query_handler(state=UserStates.arrival_date,
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_arrival(call: CallbackQuery):

    arrival_date = create_calendar_keyboard(
            call=call,
            text_if_correct='Дата заезда',
            text_if_incorrect='Дата заезда не может быть раньше сегодняшнего дня',
            offset_date=datetime.now().date(),
            bot=bot,
        )
    if arrival_date:
        storage.set_data(call.message.chat.id, call.message.chat.id, 'arrival_date', arrival_date)
        bot.set_state(call.message.chat.id, UserStates.departure_date)
        bot.send_message(
                call.message.chat.id,
                f'Выберите дату выезда:',
                reply_markup=calendar_keyboard
                )


@bot.callback_query_handler(state=UserStates.departure_date,
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_departure(call: CallbackQuery):

    data = storage.get_data(call.message.chat.id, call.message.chat.id)
    offset_date = data['arrival_date'] + timedelta(days=1)   #type: ignore

    departure_date = create_calendar_keyboard(
            call=call,
            text_if_correct='Дата выезда',
            text_if_incorrect='Дата выезда не может не может быть раньше даты заезда',
            offset_date=offset_date,
            bot=bot,
        )

    if departure_date:
        storage.set_data(call.message.chat.id, call.message.chat.id, 'departure_date', departure_date)
        data = storage.get_data(call.message.chat.id, call.message.chat.id)
        print(data)

        bot.set_state(call.message.chat.id, UserStates.hotels_amount)
        bot.send_message(call.message.chat.id, f'Введите количество отелей для поиска (максимум 25)')


