from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    destination_id = State()
    arrival_date = State()
    departure_date = State()
    hotels_amount = State()
    ask_for_photos = State()
    photos_amount = State()
    confirm_data = State()
    wait_for_results = State()

