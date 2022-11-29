from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from filters import destinations_factory


def destinations_keyboard(destinations_list):
    '''Создание inline клавиатуры для выбора города из списка предложенных вариантов'''

    return InlineKeyboardMarkup(
            keyboard=[
                [
                    InlineKeyboardButton(
                        text=city['name'],
                        callback_data=destinations_factory.new(destination_id=city['id'])
                    )
                ]
            for city in destinations_list
        ]
    )



