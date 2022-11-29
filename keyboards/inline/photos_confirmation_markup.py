from telebot.util import quick_markup


def if_need_photos_keyboard():
    '''Создание inline клавиатуры для ответа на вопрос о необходимости загрузки фотографий'''
    return quick_markup(
            {
                'Да': {'callback_data': 'yes_photos'},
                'Нет': {'callback_data': 'no_photos'}
            }
        )
