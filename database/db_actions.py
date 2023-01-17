from database import db, User, Hotel, Query, QueryToHotel
from telebot.types import Message
from datetime import datetime, timedelta
from utils.misc import get_history_text
from typing import List


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
            sort_order=data['sortOrder']
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
        hotel_url = f'hotels.com/h{hotel_id}.Hotel-Information'
        Hotel.get_or_create(id=hotel_id, name=hotel_name, url=hotel_url)

        QueryToHotel.create(query_id=query_id, hotel_id=hotel_id)


def get_history_from_db(period: str, user_id: int) -> List[str]:

    '''
    Получение истории запросов от пользователя.
    
    Arguments:
        * period - str: период, за который отображается история. (hist_day/hist_week/hist_month)
        * user_id - int: уникальный идентификатор пользователя.

    Returns:
        * list_of_messages - List[str]: Список сообщений - информации о запросе.
    '''

    list_of_messages = []

    deltas = {'hist_day': 1, 'hist_week': 7, 'hist_month': 30}
    delta = deltas[period]
    
    date_to = datetime.now()
    date_from = date_to - timedelta(days=delta)

    with db.connection_context():
        queries = Query.select().where(\
                    Query.creation_time\
                    .between(date_from, date_to),\
                    Query.user_id == user_id)

        for query in queries:
            hotels_query = Hotel.select().join(QueryToHotel).join(Query)\
                                .where(QueryToHotel.query_id == query.id)
            
            hotels_list = [{'name': hotel.name, 'url': hotel.url} for hotel in hotels_query]
            text = get_history_text(query, hotels_list)
            list_of_messages.append(text)

    return list_of_messages


def delete_user_query_history(user_id: int) -> None:
    '''
    Функция для удаления информации о запросах для конкретного пользователя.

    Arguments:
        * user_id - int: Уникальный идентификатор пользователя
    '''

    with db.connection_context():
        Query.delete().where(Query.user_id == user_id).execute()

