from loader import bot
import requests
from config_data.config import HEADERS, URLS
from bs4 import BeautifulSoup as BS
from telebot.types import InputMediaPhoto
from database import add_hotel_and_query_to_hotel
from typing import Dict, List, Optional, Tuple


def request_to_api(url: str, headers: dict, querystring: dict) -> dict:
    '''
    Общая функция получения ответа от сервера. При получение статус-кода 200, возвращает сериализированый ответ
    от api в формате словаря. В противном случае вызывается исключение.
    '''
    try:
        response = requests.get(url=url, headers=headers, params=querystring)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise requests.RequestException(
                    f'There was an issue with the request, no "200" status code returned({response.status_code})')
    except requests.RequestException as exc:
        print(exc)
        raise


def get_api_destinations_options(destination_to_find: str, locale_code: str):

    '''
    Функция отправляет запрос к api для получения вариантов городов. При успешном ответе от сервера возвращает
    список из словарей, содержащий названия и id городов - результов поиска введённого пользователем города.
    '''

    querystring = {"query": destination_to_find, "locale": locale_code}

    try:
        response_serialized = request_to_api(URLS['locations'], HEADERS, querystring)
        return get_destination_options_list(response_serialized)

    except TypeError as err:
        print(f'The TypeError has occured: {err}')
        raise


def get_destination_options_list(response_serialized: dict) -> Optional[List[Dict[str, str]]]:
    '''
    Функция получает на вход сериализированый ответ от сервера (варианты поиска по введённому пользователем
    названию города). 
    Если ответ от сервера содержит категорию CITY_GROUP, формируется и возвращается список из словарей -
    вариантов поиск.
    Если в ответе от сервера нет категории CITY_GROUP, функция возвращает None

    Arguments:
        * response_serialized: dict - Сериализированный ответ от сервера.
    '''
    list_of_names = []

    suggestions: list = response_serialized['suggestions']

    for sug in suggestions:
        if sug['group'] == 'CITY_GROUP':
            for ent in sug['entities']:
                if ent['type'] == 'CITY':

                    destination_id = ent['destinationId']
                    destination_name = BS(ent['caption'], 'html.parser').text


                    list_of_names.append(
                        {'id': destination_id, 'name': destination_name}
                    )

            return list_of_names


def get_api_hotels_and_send_to_user(query_data: dict) -> None:
    '''
    Функция отправляет запрос к api для получения вариантов отелей по заданным параметрам. Ответ по сервера
    передаётся в функцию send_hotel_info_to_user
    '''

    querystring = {
            "destinationId": str(query_data['destination_id']),
            "pageNumber":"1",
            "pageSize": query_data['hotels_amount'],
            "checkIn": query_data['arrival_date'].strftime('%Y-%m-%d'),
            "checkOut": query_data['departure_date'].strftime('%Y-%m-%d'),
            "adults1":"1",
            "sortOrder": query_data['sortOrder'],
            "locale": query_data['locale'],
            "currency": query_data['currency']
        }
    try:
        print(querystring)
        response_serialized = request_to_api(URLS['hotels'], HEADERS, querystring)
        send_hotel_info_to_user(response_serialized, query_data)
    except TypeError as err:
        print(f'The TypeError has occured: {err}')
        raise


def get_api_hotel_photos_urls(hotel_id, photos_amount: int) -> list:
    querystring = {'id': hotel_id}

    response_serialized = request_to_api(URLS['photos'], HEADERS, querystring)
    photos: list = response_serialized['hotelImages'][:photos_amount]

    photos_urls: list = [
        photo['baseUrl'].replace('{size}', 'z') for photo in photos
    ]

    return photos_urls


def get_hotel_info_text(i: int, info: dict, query_data: dict) -> Tuple[str, int]:

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

    address = f'{info["address"]["streetAddress"]}, {info["address"]["locality"]}, {info["address"]["countryName"]}'
    hotel_name = info['name']
    hotel_id = info['id']

    query_id = query_data['query_id']
    currency = query_data['currency']

    dates_delta = query_data['departure_date'] - query_data['arrival_date']
    nights_to_stay = dates_delta.days

    price_per_night = info['ratePlan']['price']['exactCurrent']
    total_price = round(price_per_night * nights_to_stay, 2)

    customer_rating = info.get('guestReviews', {}).get('rating')
    if customer_rating:
        customer_rating = f'{customer_rating}/{info["guestReviews"]["scale"]} ({info["guestReviews"]["total"]} голосов)'
    else:
        customer_rating = 'нет данных'

    distance_from_center = get_distance_from_center(info['landmarks'])


    add_hotel_and_query_to_hotel(hotel_id, hotel_name, query_id)

    info_text = f'''{i + 1}) <b><a href="hotels.com/ho{hotel_id}">{hotel_name}</a></b>
<i>Адрес: </i><b>{address}</b>
<i>Категория отеля ("звездность"): </i><b>{info['starRating']}/5</b>
<i>Пользовательский рейтинг: </i><b>{customer_rating}</b>
<i>Расстояние от центра города: </i><b>{distance_from_center}</b>
<i>Средняя стоимость номера за ночь на указанные даты (без учета налогов)</i>: <b>{price_per_night} {currency}</b>
<i>Примерная общая стоимость проживания (без учета налогов)</i>: <b>{total_price} {currency}</b>

'''
    return info_text, hotel_id


def send_hotel_info_to_user(response_serialized: dict, query_data: dict):
    '''
    Формирование и отправка пользователю информации (и, при необходимости, фото) об отелях.
    Текст сообщения получаем из функции get_hotel_info_text, список с url фотографий отеля - из функции
    get_api_hotel_photos_urls.

    Arguments:
        * response_serialized: dict - Сериализированный ответ от сервера.
        * query_data: dict - Словарь, содержащий информацию о запросе.
    '''

    results = response_serialized['data']['body']['searchResults']['results']
    chat_id = query_data['user_id']

    for index, result in enumerate(results):
        info_text, hotel_id = get_hotel_info_text(index, result, query_data)

        photos_amount = int(query_data['photos_amount'])
        if not photos_amount:
            bot.send_message(chat_id, info_text, parse_mode='html')
        elif photos_amount == 1:
            photo_url=get_api_hotel_photos_urls(hotel_id, 1)[0]
            bot.send_photo(chat_id, photo=photo_url, caption=info_text, parse_mode='html')
        else:
            photos_urls = get_api_hotel_photos_urls(hotel_id, photos_amount)
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

