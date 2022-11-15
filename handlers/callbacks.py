from loader import bot
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery) -> None:
    '''Обработчик коллбэков от клавиатуры.'''
    try:
        if call.message:
            pass
    except Exception as exc:
        print(exc)
    
    bot.edit_message_text(
            chat_id=call.message.chat.id, \
            message_id=call.message.message_id, \
            text=call.message.text,
            reply_markup=None)
            
                
