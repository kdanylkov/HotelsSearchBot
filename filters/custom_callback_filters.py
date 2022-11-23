from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.types import Message


destinations_factory = CallbackData('destination_id', prefix='locations')


class LocationsCallbackFilter(AdvancedCustomFilter):

    key = 'locations_config'
    
    def check(self, call: CallbackData, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class HotelAmount(SimpleCustomFilter):

    key = 'is_hotels_amt_correct'

    def check(self, message: Message):
        try:
            amt = int(message.text)  #type: ignore
        except ValueError:
            return False
        return 0 < amt <= 25   

