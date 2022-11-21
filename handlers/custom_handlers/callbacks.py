from loader import bot, storage
from telebot.types import CallbackQuery
from filters import locations_factory

def delete_inline_markup(msg):
    bot.edit_message_text(msg.text, msg.chat.id, msg.message_id, reply_markup=None)


@bot.callback_query_handler(func=lambda call: True, locations_config=locations_factory.filter())
def callback_location_choice_handler(call: CallbackQuery):
    callback_data: dict = locations_factory.parse(callback_data=call.data)
    location_id = callback_data['destination_id']
    bot.send_message(call.message.chat.id, 
            f'Вы выбрали город со таким id: {location_id}'
            )

    delete_inline_markup(call.message)

    storage.set_data(call.message.chat.id, call.message.chat.id, key='destination_id', value=location_id)
    data = storage.get_data(call.message.chat.id, call.message.chat.id)
    print(data)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery) -> None:
    '''Обработчик коллбэков от клавиатуры.'''
    try:
        if call.message:
            pass
    except Exception as exc:
        print(exc)
    
    delete_inline_markup(call.message)
                
