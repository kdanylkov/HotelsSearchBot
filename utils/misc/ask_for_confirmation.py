from loader import bot
from keyboards.inline import confirm_query_keyboard


criterias = {
        'PRICE_LOW_TO_HIGH': 'Топ самых дешёвых отелей',
        'RATING': 'Топ отелей по оценкам пользователей',
        'DISTANCE': 'Топ отелей, наиболее подходящим по цене и расположению от центра'
    }



def ask_for_input_confirmation(id: int) -> None:
    '''
    Функция формирует из введённых ранее пользователем данных инфомационное сообщение. Пользователю предлагается
    подтвердить ввод, начать ввод заново либо отменить поиск.

    Arguments:
        * id: int - Telegram-id пользователя
    '''

    with bot.retrieve_data(id) as data:                                         #type: ignore
        arrival_date = data['arrival_date'].strftime('%d.%m.%Y')
        departure_date = data['departure_date'].strftime('%d.%m.%Y')

        text = f'Вы запрашиваете поиск отелей по следующим параметрам:\n \
                1) Критерий поиска: {criterias[data["sortOrder"]]};\n \
                2) Город: {data["destination_name"]}  \n \
                3) Количество отелей для поиска: {data["hotels_amount"]}\n \
                4) Количество фотографий для каждого отеля: {data["photos_amount"]}\n \
                5) Дата заезда: {arrival_date} \n \
                6) Дата выезда: {departure_date}'

        if data['sortOrder'] == 'DISTANCE':

            bestdeal_amendment = f'''
                 7) Минимальная цена: {data["price_min"]} USD
                 8) Максимальная цена: {data["price_max"]} USD
'''
            text = ''.join([text, bestdeal_amendment])
                            

    bot.send_message(id, text, reply_markup=confirm_query_keyboard())


