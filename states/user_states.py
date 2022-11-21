from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    destination_id = State()
    arrival_data = State()

