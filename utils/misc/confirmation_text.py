

criterias = {
        'PRICE': 'Топ самых дешёвых отелей',
        'PRICE_HIGHEST_FIRST': 'Топ самых дорогих отелей',
        'DISTANCE_FROM_LANDMARK': 'Топ отелей, наиболее подходящим по цене и расположению от центра'
    }



def get_query_confirmation_text(storage, id) -> str:

    data = storage.get_data(id, id)

    arrival_date = data['arrival_date'].strftime('%d.%m.%Y')
    departure_date = data['departure_date'].strftime('%d.%m.%Y')

    text = f'Вы запрашиваете поиск отелей по следующим параметрам:\n \
            1) Критерий поиска: {criterias[data["sortOrder"]]};\n \
            2) Город: {data["destination_name"]}  \n \
            3) Количество отелей для поиска: {data["hotels_amount"]}\n \
            4) Дата заезда: {arrival_date} \n \
            5) Дата выезда: {departure_date}'

    return text
