from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.types import Message


destinations_factory = CallbackData('destination_id', prefix='locations')


class LocationsCallbackFilter(AdvancedCustomFilter):

    key = 'locations_config'
    
    def check(self, call: CallbackData, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class BaseDigitFilter(SimpleCustomFilter):
    min_val = 1
    max_val = 25
    
    def check(self, message):
        try:
            amt = int(message.text)  #type: ignore
        except ValueError:
            return False
        return self.min_val <= amt <= self.max_val   
        

class HotelAmount(BaseDigitFilter):

    key = 'is_hotels_amt_correct'


class PhotosAmount(BaseDigitFilter):

    key = 'is_photos_amt_correct'
    max_val = 5

