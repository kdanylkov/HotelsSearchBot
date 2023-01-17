from loader import bot
from keyboards.inline import confirm_query_keyboard
from config_data.config import criterias


def get_query_info_text(data: dict) -> str:

    arrival_date = data['arrival_date'].strftime('%d.%m.%Y')
    departure_date = data['departure_date'].strftime('%d.%m.%Y')

    text = f'''
1) Критерий поиска: {criterias[data["sortOrder"]]};
2) Город: {data["destination_name"]}
3) Количество отелей для поиска: {data["hotels_amount"]}
4) Количество фотографий для каждого отеля: {data["photos_amount"]}
5) Дата заезда: {arrival_date}
6) Дата выезда: {departure_date}'''

    if data['sortOrder'] == 'DISTANCE':

        bestdeal_amendment = f'''
7) Минимальная цена: {data["price_min"]} USD
8) Максимальная цена: {data["price_max"]} USD
'''
        text = ''.join([text, bestdeal_amendment])

    return text


def ask_for_input_confirmation(id: int) -> None:
    '''
    Функция формирует из введённых ранее пользователем данных инфомационное сообщение. Пользователю предлагается
    подтвердить ввод, начать ввод заново либо отменить поиск.

    Arguments:
        * id: int - Telegram-id пользователя
    '''

    with bot.retrieve_data(id) as data:                                         #type: ignore
        text = get_query_info_text(data)

    text = ''.join(['Вы запрашиваете поиск отелей по следующим параметрам:\n', text])

    bot.send_message(id, text, reply_markup=confirm_query_keyboard())


