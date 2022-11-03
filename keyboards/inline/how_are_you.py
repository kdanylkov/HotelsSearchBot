from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def how_are_you_reply() -> InlineKeyboardMarkup:
    '''Инлайн клавиатура для ответа на вопрос пользователю "Как дела?"'''
    markup = InlineKeyboardMarkup(row_width=2)
    
    item_1 = InlineKeyboardButton(text='Хорошо👍', callback_data='good')
    item_2 = InlineKeyboardButton(text='Не очень👎', callback_data='bad')
    
    markup.add(item_1, item_2)

    return markup
    
