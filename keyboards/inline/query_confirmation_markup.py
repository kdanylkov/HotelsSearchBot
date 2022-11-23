from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_query_keyboard():
    markup = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Подтвердить', callback_data='yes_confirm')
    item2 = InlineKeyboardButton(text='Повторить', callback_data='no_confirm')

    return markup.add(item1, item2)
    
