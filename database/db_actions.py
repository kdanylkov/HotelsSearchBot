from database import db, User, Hotel, Query, QueryToHotel


def add_user(message):
    User.get_or_create(name=message.from_user.full_name, telegram_id=int(message.from_user.id))

