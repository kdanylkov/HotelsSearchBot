from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter


locations_factory = CallbackData('destination_id', prefix='locations')


class LocationsCallbackFilter(AdvancedCustomFilter):

    key = 'locations_config'
    
    def check(self, call: CallbackData, config: CallbackDataFilter) -> bool:
        return config.check(query=call)

