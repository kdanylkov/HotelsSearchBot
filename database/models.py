import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('database/hotels-search.db')


class BaseModel(pw.Model):
    '''Создание базовой модели класса peewee.Model'''
    
    class Meta:
        database = db


class User(BaseModel):

    '''
    Создание модели класса User, наследуется от BaseModel.
    Используется для сохранения в БД информации о пользователе

    Attributes:
        * telegram_id - Уникальный идентификатор пользователя в Telegram
    (первичный ключ для таблицы 'user')
        * name - Имя пользователя в Telegram
    '''

    telegram_id = pw.PrimaryKeyField()
    name = pw.CharField()


class Query(BaseModel):
    '''
    Создание модели класса Query, наследуется от BaseModel. 
    Используется для сохранения в БД информации о запросе к api

    Attributes:
        * destination_id - Уникальный идентификатор города в api
        * destination_name - Название города
        * user_id - Внешний ключ: id пользователя, осуществляющего запрос
        * arrival_date - Дата заезда
        * departure_date - Дата выезда
        * creation_time - Дата и время запроса
        * hotels_to_find - Количество отелей для поиска
        * photos_to_find - Количество фотографий для каждого отеля

    '''

    destination_id = pw.CharField()
    destination_name = pw.CharField()
    user_id = pw.ForeignKeyField(User)
    arrival_date = pw.DateField()
    departure_date = pw.DateField()
    creation_time = pw.DateTimeField(default=datetime.now)
    hotels_to_find = pw.IntegerField()
    photos_to_find = pw.IntegerField()


class Hotel(BaseModel):
    '''
    Создание модели класса Hotel, наследуется от BaseModel. 

    Используется для сохранения в БД информации об отеле

    Attributes:
        * id - Уникальный идентификатор отеля в api
        * name - Название отеля
        * url - веб-страница отеля на сайте hotels.com

    '''

    id = pw.PrimaryKeyField()
    name = pw.CharField()
    url = pw.CharField()
    

class QueryToHotel(BaseModel):

    '''
    Создание модели класса QueryToHotel, наследуется от BaseModel. 

    Отвечает за создание связи many-to-many между таблицами Hotel и Query

    Attributes:
        * query_id - Внешний ключ: id запроса
        * hotel_id - Внешний ключ: id отеля
    '''

    query_id = pw.ForeignKeyField(Query)
    hotel_id = pw.ForeignKeyField(Hotel)


db.create_tables([              # инициализация таблиц и их структуры в БД
    User,
    Hotel,
    Query,
    QueryToHotel
    ])
