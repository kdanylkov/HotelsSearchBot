import peewee as pw

db = pw.SqliteDatabase('hotels-search.db')


class BaseModel(pw.Model):
    
    class Meta:
        database = db


class User(BaseModel):

    telegram_id = pw.PrimaryKeyField()
    name = pw.CharField()


class Query(BaseModel):

    destination_id = pw.PrimaryKeyField()
    user_id = pw.ForeignKeyField(User)
    arrival_date = pw.DateField()
    departure_date = pw.DateField()
    query_time = pw.DateTimeField()
    hotels_to_find = pw.IntegerField()


class Hotel(BaseModel):

    hotel_id = pw.PrimaryKeyField()
    url = pw.CharField()
    description = pw.TextField()
    

class QueryToHotel(BaseModel):

    query_id = pw.ForeignKeyField(Query)
    hotel_id = pw.ForeignKeyField(Hotel)


db.create_tables([
    User,
    Hotel,
    Query,
    QueryToHotel
    ])
