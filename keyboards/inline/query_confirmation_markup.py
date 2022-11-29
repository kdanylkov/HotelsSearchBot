from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_query_keyboard():
    '''Создание inline клавиатуры для подтверждения введённой информации'''
    markup = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(text='Подтвердить', callback_data='yes_confirm')
    item2 = InlineKeyboardButton(text='Ввести данные заново', callback_data='reset_confirm')
    item3 = InlineKeyboardButton(text='Отмена операции', callback_data='cancel_confirm')

    return markup.add(item1, item2, item3)
    
