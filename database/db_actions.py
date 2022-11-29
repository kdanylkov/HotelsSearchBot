from database import db, User, Hotel, Query, QueryToHotel
from telebot.types import Message


def add_user(message: Message) -> None:
    '''
    Добавление пользователя в БД, в таблицу "User".

    Используется метод pewee.Model.get_or_create: добавление записи о пользователе происходит только
    в том случае, если такой записи еще нет в таблице.
    '''

    with db.connection_context():
        User.get_or_create(name=message.from_user.full_name, telegram_id=int(message.from_user.id))


def add_query(data: dict) -> int:
    '''
    Добавление информации о запросе в БД, в таблицу "Query".

    Используется метод peewee.Model.create

    Функция возвращает id записи о запросе в таблице, для дальнейшего заполнения таблицы QueryToHotel.
    '''

    
    with db.connection_context():
        query = Query.create(
            destination_id=data['destination_id'],
            destination_name=data['destination_name'],
            user_id=data['user_id'],
            arrival_date=data['arrival_date'].date(),
            departure_date=data['departure_date'].date(),
            hotels_to_find=data['hotels_amount'],
            photos_to_find=data['photos_amount'],
            currency=data['currency']
            )
    return query.id


def add_hotel_and_query_to_hotel(hotel_id: int, hotel_name: str, query_id: int) -> None:
    '''
    Добавление информации об отеле в БД, в таблицу "Hotel", а также создание связи "many-to-many" между 
    таблицами Hotel и Query.

    Arguments:
        * hotel_id: int - id отеля
        * hotel_name: str - название отеля
        * query_id: int - id запроса

    '''

    with db.connection_context():
        hotel_url = f'hotels.com/ho{hotel_id}'
        Hotel.get_or_create(id=hotel_id, name=hotel_name, url=hotel_url)

        QueryToHotel.create(query_id=query_id, hotel_id=hotel_id)


