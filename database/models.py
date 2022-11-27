import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('database/hotels-search.db')


class BaseModel(pw.Model):
    
    class Meta:
        database = db


class User(BaseModel):

    telegram_id = pw.PrimaryKeyField()
    name = pw.CharField()


class Query(BaseModel):

    destination_id = pw.CharField()
    destination_name = pw.CharField()
    user_id = pw.ForeignKeyField(User)
    arrival_date = pw.DateField()
    departure_date = pw.DateField()
    creation_time = pw.DateTimeField(default=datetime.now)
    hotels_to_find = pw.IntegerField()
    photos_to_find = pw.IntegerField()
    currency = pw.CharField()

class Hotel(BaseModel):

    id = pw.PrimaryKeyField()
    name = pw.CharField()
    url = pw.CharField()
    

class QueryToHotel(BaseModel):

    query_id = pw.ForeignKeyField(Query)
    hotel_id = pw.ForeignKeyField(Hotel)


db.create_tables([
    User,
    Hotel,
    Query,
    QueryToHotel
    ])
