from datetime import datetime
from config_data.config import criterias


def get_history_text(query, hotels_list: list) -> str:

    '''
    Функция для получения текста сообщения для истории запросов. 

    Arguments:
        * query - Model: запрос из истории поиска
        * hotels_list - list: список из словарей, содержащих информацию об отелях, найденных по
        данному запросу.

    Returns:
        * text - str: Текст сообщения.
    '''

    query_time: datetime = query.creation_time.strftime('%d.%m.%Y %H:%M:%S')
    arr_date: datetime = query.arrival_date.strftime('%d.%m.%Y')
    dep_date: datetime = query.departure_date.strftime('%d.%m.%Y')

    text = f'''
1. <b><u>Дата и время запроса</u></b>: {query_time}
2. <b><u>Дата прибытия</u></b>: {arr_date};
3. <b><u>Дата выезда</u></b>: {dep_date}
4. <b><u>Город поиска</u></b>: {query.destination_name}
5. <b><u>Критерий поиска</u></b>: {criterias[query.sort_order]}\n
<b><u>Список найденных отелей</u></b>:\n
'''
    for hotel in hotels_list:
        hotel_link = f'\t<a href="{hotel["url"]}">{hotel["name"]}</a>\n'
        text = ''.join([text, hotel_link])

    return text

