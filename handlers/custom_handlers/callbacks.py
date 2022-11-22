from loader import bot, storage, calendar_1_callback
from telebot.types import CallbackQuery
from filters import locations_factory
from datetime import datetime, timedelta
from states import UserStates
from keyboards.inline import create_calendar_keyboard, calendar_markup


def delete_inline_markup(msg):
    bot.edit_message_text(msg.text, msg.chat.id, msg.message_id, reply_markup=None)


@bot.callback_query_handler(func=lambda call: True, locations_config=locations_factory.filter())
def callback_location_choice_handler(call: CallbackQuery):

    ID = call.message.chat.id
    bot.delete_message(call.message.chat.id, call.message.message_id)

    callback_data: dict = locations_factory.parse(callback_data=call.data)
    location_id = callback_data['destination_id']
    storage.set_data(call.message.chat.id, call.message.chat.id, key='destination_id', value=location_id)

    bot.set_state(ID, UserStates.arrival_date)

    bot.send_message(
            ID,
            f'Выберите дату заезда:',
            reply_markup=calendar_markup
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
            offset_date=datetime.now(),
            bot=bot,
            storage=storage
        )
    if arrival_date:
        storage.set_data(call.message.chat.id, call.message.chat.id, 'arrival_date', arrival_date)
        bot.set_state(call.message.chat.id, UserStates.departure_date)
        bot.send_message(
                call.message.chat.id,
                f'Выберите дату выезда:',
                reply_markup=calendar_markup
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
            storage=storage
        )

    if departure_date:
        storage.set_data(call.message.chat.id, call.message.chat.id, 'departure_date', departure_date)
        bot.send_message(
                call.message.chat.id,
                f'SO FAR SO GOOD!',
                )


