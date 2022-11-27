from loader import bot
from keyboards.inline import confirm_query_keyboard


criterias = {
        'PRICE': 'Топ самых дешёвых отелей',
        'PRICE_HIGHEST_FIRST': 'Топ самых дорогих отелей',
        'DISTANCE_FROM_LANDMARK': 'Топ отелей, наиболее подходящим по цене и расположению от центра'
    }



def ask_for_input_confirmation(id) -> None:

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

    bot.send_message(id, text, reply_markup=confirm_query_keyboard())
