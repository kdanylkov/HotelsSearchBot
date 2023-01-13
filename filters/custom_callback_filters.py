from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.types import Message


destinations_factory = CallbackData('destination_id', prefix='locations')


class LocationsCallbackFilter(AdvancedCustomFilter):
    '''
    Создание фильтра для обработки callback данних при нажатии клавиатуры вариантов городов.
    Наследуется от класса AdvancedCustomFilter.
    '''

    key = 'locations_config'
    
    def check(self, call: CallbackData, config: CallbackDataFilter) -> bool:
        '''Метод для проверки на соответствие условиям фильтра'''

        return config.check(query=call)


class BaseDigitFilter(SimpleCustomFilter):
    '''
    Создание базового класса фильтра, в котором сообщение пользователя проверяется на соответствие условиям:
        1. Сообщение состоит из цифр
        2. Число, введённое пользователем, находится в диапазоне от min_val до max_val. (по умолчанию - от 1 до 25)
    '''
    min_val = 1
    max_val = 25
    
    def check(self, message: Message) -> bool:
        '''Метод для проверки на соответствие условиям фильтра'''
        try:
            amt = int(message.text)  #type: ignore
        except ValueError:
            return False
        return self.min_val <= amt <= self.max_val   
        

class HotelAmount(BaseDigitFilter):
    '''
    Класс-фильтр HotelAmount, наследуется от класса BaseDigitFilter. Значения диапазона по умолчания (1-25)

    Применяется для проверки правильности введения количества отелей для поиска.
    '''

    key = 'is_hotels_amt_correct'


class PhotosAmount(BaseDigitFilter):
    '''
    Класс-фильтр PhotosAmount, наследуется от класса BaseDigitFilter. Верхнее значениео диапазона (max_val)
    изменено на 5.
    
    Применяется для проверки правильности введения количества фотографий, загружаемых для каждого отеля.
    '''

    key = 'is_photos_amt_correct'
    max_val = 5

class PriceRangeCorrect(SimpleCustomFilter):
    '''
    Класс-фильтр PriceRangeCorrect, наследник класса SimpleCustomFilter. Используется для проверки 
    на соответствие пользовательского ввода следующим критериям:
        1. Ввод состоит двух цифр
        2. Введённые цифры разделены пробелом
    '''

    def check(self, message: Message) -> bool:
        try:
            numbers = [int(number) for number in message.text.split()]        #type: ignore
        except ValueError:
            return False
        return len(numbers) == 2



