from database import db, User, Hotel, Query, QueryToHotel
from datetime import datetime


def add_user(message):
    with db.connection_context():
        User.get_or_create(name=message.from_user.full_name, telegram_id=int(message.from_user.id))


def add_query(data: dict):
    
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


def add_hotel_and_query_to_hotel(hotel_id, hotel_name, query_id):

    with db.connection_context():
        hotel_url = f'hotels.com/ho{hotel_id}'
        Hotel.get_or_create(id=int(hotel_id), name=hotel_name, url=hotel_url)

        QueryToHotel.create(query_id=query_id, hotel_id=hotel_id)


