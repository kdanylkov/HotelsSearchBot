from loader import bot
from json import dump
import requests
from config_data.config import HEADERS, URLS
from telebot.types import InputMediaPhoto
from database import add_hotel_and_query_to_hotel
from typing import Dict, List, Optional, Tuple


def request_to_api(method: str, url: str, headers: dict, querystring: dict) -> dict:
    '''
    Общая функция получения ответа от сервера. При получение статус-кода 200, возвращает сериализированый ответ
    от api в формате словаря. В противном случае вызывается исключение.
    '''
    try:
        if method == 'GET':
            response = requests.request(method=method, url=url, headers=headers, params=querystring)
        else:
            response = requests.request(method=method, url=url, headers=headers, json=querystring)

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print(response.text)
            raise requests.RequestException(
                    f'There was an issue with the request, no "200" status code returned({response.status_code})')
    except requests.RequestException as exc:
        print(exc)
        raise


def get_api_destinations_options(destination_to_find: str, locale_code: str):

    '''
    Функция отправляет запрос к api для получения вариантов городов. При успешном ответе от сервера возвращает
    список из словарей, содержащий названия и id городов - результатов поиска введённого пользователем города.
    '''

    querystring = {"q": destination_to_find, "locale": locale_code}

    headers = HEADERS.copy()
    headers.pop('content-type')

    try:
        response_serialized = request_to_api('GET', URLS['locations'], HEADERS, querystring)
        return get_destination_options_list(response_serialized)

    except TypeError as err:
        print(f'The TypeError has occured: {err}')
        raise


def get_destination_options_list(response_serialized: dict) -> Optional[List[Dict[str, str]]]:
    '''
    Функция получает на вход сериализированый ответ от сервера (варианты поиска по введённому пользователем
    названию города). 
    Если в ответe от сервера содержатся сущности с типом "CITY", формируется и возвращается список
    из словарей - вариантов поиска.
    Если в ответе от сервера нет таких сущностей, возвращается пустой список.
    Arguments:
        * response_serialized: dict - Сериализированный ответ от сервера.
    '''
    list_of_names = []

    suggestions: list = response_serialized['sr']

    for sug in suggestions:
        if sug['type'] == 'CITY':
            destination_id = sug['gaiaId']
            destination_name = sug['regionNames']['fullName']
            list_of_names.append(
                        {'id': destination_id, 'name': destination_name}
                    )

    return list_of_names


def get_hotels_from_api(query_data: dict) -> None:
    '''
    Функция отправляет запрос к api для получения вариантов отелей по заданным параметрам. Ответ по сервера
    передаётся в функцию send_hotel_info_to_user
    '''

    sort = 'PRICE_LOW_TO_HIGH' if query_data['sortOrder'] in ('lowprice', 'highprice') else 'DISTANCE'

    payload = {
	"currency": "USD",
	"eapid": 1,
	"locale": query_data["locale"],
	"siteId": 300000001,
	"destination": {"regionId": str(query_data['destination_id'])},
	"checkInDate": {
		"day": query_data["arrival_date"].day,
		"month": query_data["arrival_date"].month,
		"year": query_data["arrival_date"].year
	},
	"checkOutDate": {
		"day": query_data["departure_date"].day,
		"month": query_data["departure_date"].month,
		"year": query_data["departure_date"].year
	},
	"rooms": [{"adults": 1}],
	"resultsSize": int(query_data["hotels_amount"]),
	"sort": sort
    }

    try:
        response_serialized = request_to_api(method='POST', url=URLS['hotels'], headers=HEADERS, querystring=payload)
        send_hotels_info_to_user(response_serialized, query_data)
    except TypeError as err:
        print(f'The TypeError has occured: {err}')
        raise


def get_hotel_info_and_photos(i: int, info: dict, query_data: dict) -> Tuple[str, list]:

    '''
    Формирование текста информации об отеле.

    Arguments:
        * i: int - индекс, номер отеля по порядку в списке вариантов.
        * info: dict - информация об отеле, полученная от api
        * query_data: dict - Словарь, содержащий информацию о запросе.
    Returns:
        * info_text: str - Строка, содержащая инфомацию об отеле для вывода пользователю
        * hotel_id: int - id отеля
    '''
    
    locale = query_data['locale']

    hotel_id = info['id']

    star_rating, address, photos_urls = get_rating_adderess_and_photos_from_api(
            hotel_id,
            query_data['photos_amount'],
            locale,
        )

    hotel_name = info['name']

    dates_delta = query_data['departure_date'] - query_data['arrival_date']
    nights_to_stay = dates_delta.days

    price_per_night = info['price']['lead']['amount']
    total_price = round(price_per_night * nights_to_stay, 2)

    customer_rating = info.get('reviews', {}).get('score')

    distance_from_center = info['destinationInfo']['distanceFromDestination']['value']
    distance_unit = 'км' if info['destinationInfo']['distanceFromDestination']['unit'] == 'KILOMETER' else 'miles'

    add_hotel_and_query_to_hotel(hotel_id, hotel_name, query_data['query_id'])

    info_text = f'''{i + 1}) <b><a href="hotels.com/h{hotel_id}.Hotel-Information">{hotel_name}</a></b>
<i>Адрес: </i><b>{address if address else 'нет данных'}</b>
<i>Категория отеля ("звездность"): </i><b>{star_rating if star_rating else 'нет данных'}/5</b>
<i>Пользовательский рейтинг: </i><b>{customer_rating if customer_rating else 'нет данных'}</b>
<i>Расстояние от центра города: </i><b>{distance_from_center} {distance_unit}</b>
<i>Средняя стоимость номера за ночь на указанные даты (без учета налогов)</i>: <b>{price_per_night} USD</b>
<i>Примерная общая стоимость проживания (без учета налогов)</i>: <b>{total_price} USD</b>

'''
    return info_text, photos_urls


def send_hotels_info_to_user(response_serialized: dict, query_data: dict):
    '''
    Формирование и отправка пользователю информации (и, при необходимости, фото) об отелях.
    Текст сообщения получаем из функции get_hotel_info_text, список с url фотографий отеля - из функции
    get_api_hotel_photos_urls.

    Arguments:
        * response_serialized: dict - Сериализированный ответ от сервера.
        * query_data: dict - Словарь, содержащий информацию о запросе.
    '''

    results = response_serialized['data']['propertySearch']['properties']
    chat_id = query_data['user_id']

    for index, result in enumerate(results):

        info_text, photos_urls = get_hotel_info_and_photos(index, result, query_data)

        photos_amount = int(query_data['photos_amount'])
        if not photos_amount:
            bot.send_message(chat_id, info_text, parse_mode='html')
        elif photos_amount == 1:
            photo_url = photos_urls[0]
            bot.send_photo(chat_id, photo=photo_url, caption=info_text, parse_mode='html')
        else:
            bot.send_media_group(
                chat_id,
                media=[
                    InputMediaPhoto(media=url, caption=info_text if index == 0 else '', parse_mode='html')
                    for index, url in enumerate(photos_urls)
                ]
            )


def get_distance_from_center(landmarks: list) -> str:
    ''' Получение расстояния от центра города (либо "нет данных" при отсутствии соответствующей информации)'''
    for l in landmarks:
        if l['label'] in ('City center', 'Центр города'):
            return l['distance']
    return 'нет данных'


def get_rating_adderess_and_photos_from_api(hotel_id: str, photos_amount: int, locale) -> tuple:
    '''
    Получение от api дополнительной информации о рейтинге, адресе отеля, а также получение списка url'ов
    фотографий отеля. Количество фотографий зависит от ранее введённых пользователем данных.

    Arguments:
        * hotel_id: str - Уникальный идентификатор отеля.
        * photos_amount: int - Желаемое количество фотографий (может быть от 0 до 5)
        * locale: str - Локаль, которая может быть либо en_US, либо ru_RU (зависит от того, на каком языке
    пользователь вводил название города.
    '''

    print(hotel_id)
    payload = {
            'propertyId': hotel_id,
            'currency': "USD",
            'locale': locale
            }

    print(payload)
    response_serialized = request_to_api('POST', URLS['photos'], HEADERS, payload)
    print(response_serialized)

    property_info = response_serialized['data']['propertyInfo']
    with open('temp.json', 'w', encoding='utf-8') as wf:
        dump(property_info, wf, ensure_ascii=False, indent=4)

    photos: list = property_info['propertyGallery']['images'][0:int(photos_amount)]

    photos_urls = [photo['image']['url'] for photo in photos] if photos_amount else []
    address = property_info.get('summary', {}).get('location', {}).get('address', {}).get('addressLine')
    star_rating = property_info.get('summary', {}).get('overview', {}).get('propertyRating')
    if star_rating:
        star_rating = star_rating.get('rating')

    return star_rating, address, photos_urls


