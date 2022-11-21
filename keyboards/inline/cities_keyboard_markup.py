from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from filters import locations_factory


def cities_keyboard(cities_list):
    print(cities_list)
    return InlineKeyboardMarkup(
            keyboard=[
                [
                    InlineKeyboardButton(
                        text=city['name'],
                        callback_data=locations_factory.new(destination_id=city['id'])
                    )
                ]
            for city in cities_list
        ]
    )



