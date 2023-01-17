from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    '''
    Класс UserState наследуется от класса telebot.handler_backends.StatesGroup. 
    Используется для задания состояний пользователя. 

    Каждый из атрибутов класса является экземпляром класса telebot.handler_backends.State (состояние)
    '''
    destination_id = State()
    arrival_date = State()
    departure_date = State()
    hotels_amount = State()
    ask_for_photos = State()
    photos_amount = State()
    confirm_data = State()
    wait_for_results = State()
    price_range = State()
    history_choice = State()

