from loader import bot, calendar_1_callback
from telebot.types import CallbackQuery
from filters import destinations_factory
from datetime import datetime, timedelta
from states import UserStates
from keyboards.inline import create_calendar_keyboard, calendar_keyboard
from utils import ask_for_input_confirmation
from database import add_query
from rapid_api import get_hotels_from_api


@bot.callback_query_handler(func=None, locations_config=destinations_factory.filter())
def callback_location_choice_handler(call: CallbackQuery):

    '''
    Обработчик callback запросов при выборе города из списка вариантов, предложенных поиском.
    Применяется фильтр LocationsCallbackFilter

    После получения выбора пользователя, id и имя города сохраняется в память сценария 
    под ключами "destination_id" и "destination_name".

    После получения данных устанавливается новое состояние пользователя - UserStates.arrival_date 
    (выбор даты заезда)
    '''

    ID = call.message.chat.id
    bot.delete_message(call.message.chat.id, call.message.message_id)

    callback_data: dict = destinations_factory.parse(callback_data=call.data)

    destination_id = callback_data['destination_id']

    with bot.retrieve_data(call.message.chat.id) as data:                   #type: ignore
        destination_name = data['names_and_ids'][destination_id]
        data['destination_name'] = destination_name
        data['destination_id'] = int(destination_id)
        data.pop('names_and_ids')

    bot.set_state(ID, UserStates.arrival_date)

    now = datetime.now()
    bot.send_message(
            ID,
            f'Выберите дату заезда:',
            reply_markup=calendar_keyboard(now.year, now.month)
            )


@bot.callback_query_handler(state=UserStates.arrival_date,
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_arrival(call: CallbackQuery):
    '''
    Обработчик callback запросов нажатии одной из кнопок inline клавиатуры - календаря при выборе даты
    заезда.

    Вызывается функция create_calendar_keyboard, которая возвращает либо объект datetime (выбранную
    пользователем дату заезда), либо None, если пользователь выбрал неправильную дату. В последнем случае 
    пользователь получит сообщение о неправильном выборе даты, и ему будет предложено сделать выбор заново.
    
    Если create_calendar_keyboard возвращает дату, она сохраняется в память сценария 
    под ключём "arrival_date". 

    После получения данных устанавливается новое состояние пользователя - UserStates.departure_date 
    (выбор даты выезда)

    '''

    arrival_date: datetime | None = create_calendar_keyboard(
            call=call,
            text_if_correct='Дата заезда',
            text_if_incorrect='Дата заезда не может быть раньше сегодняшнего дня',
            offset_date=datetime.now(),
            bot=bot,
        )
    if arrival_date:
        with bot.retrieve_data(call.message.chat.id) as data:                        #type: ignore
            data['arrival_date'] = arrival_date

        bot.set_state(call.message.chat.id, UserStates.departure_date)

        bot.send_message(
                call.message.chat.id,
                f'Выберите дату выезда:',
                reply_markup=calendar_keyboard(arrival_date.year, arrival_date.month)
                )


@bot.callback_query_handler(state=UserStates.departure_date,
    func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def callback_departure(call: CallbackQuery):
    '''
    Обработчик callback запросов нажатии одной из кнопок inline клавиатуры - календаря при выборе даты
    выезда.

    Вызывается функция create_calendar_keyboard, которая возвращает либо объект datetime (выбранную
    пользователем дату заезда), либо None, если пользователь выбрал неправильную дату. В последнем случае 
    пользователь получит сообщение о неправильном выборе даты, и ему будет предложено сделать выбор заново.
    
    Если create_calendar_keyboard возвращает дату, она сохраняется в память сценария 
    под ключём "departure_date". 

    После получения данных устанавливается новое состояние пользователя - UserStates.departure_date 
    (ввод количества отелей для поиска)
    '''

    with bot.retrieve_data(call.message.chat.id) as data:        #type: ignore  
        offset_date = data['arrival_date'] + timedelta(days=1)   

    departure_date: datetime | None = create_calendar_keyboard(
            call=call,
            text_if_correct='Дата выезда',
            text_if_incorrect='Дата выезда не может не может быть раньше даты заезда',
            offset_date=offset_date,
            bot=bot,
        )

    if departure_date:
        with bot.retrieve_data(call.message.chat.id) as data:           #type: ignore
            data['departure_date'] = departure_date
            print(data)

        bot.set_state(call.message.chat.id, UserStates.hotels_amount)
        bot.send_message(call.message.chat.id, f'Введите количество отелей для поиска (максимум 25)')


@bot.callback_query_handler(state=UserStates.ask_for_photos, func=lambda c: c.data.endswith('photos'))
def callback_download_photos(call: CallbackQuery):
    '''
    Обработчик callback запросов нажатии одной из кнопок inline клавиатуры при ответе на вопрос бота
    о необходимости загрузки фотографий отелей вместе с результатами поиска.

        * Если call.data == "yes_photos", устанавливается состояние пользователя UserStates.photos_amount
    (ввод количества загружаемых для каждого отеля фотографий)

        * Если call.data == "no_photos", количество фотографий устанавливается как ноль и сохраняется в
    память сценария под ключём "photos_amount", а также устанавливается состояние пользователя
    UserStates.confirm_data (подтверждение ранее введенной информации). UserStates.photos_amount пропускается
    '''
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'yes_photos':
        bot.send_message(call.message.chat.id, 'Введите количество фотографий (максимум 5)')
        bot.set_state(call.message.chat.id, UserStates.photos_amount)
    elif call.data == 'no_photos':
        with bot.retrieve_data(call.message.chat.id) as data:                       #type: ignore
            data['photos_amount'] = 0

        bot.set_state(call.message.chat.id, UserStates.confirm_data)
        ask_for_input_confirmation(call.message.chat.id)


@bot.callback_query_handler(state=UserStates.confirm_data, func=lambda c: c.data.endswith('confirm'))
def callback_data_input_confirmation(call: CallbackQuery):
    '''
    Обработчик callback запросов нажатии одной из кнопок inline клавиатуры при ответе на запрос бота
    на подтверждение ранее введённой информации.

        * Если call.data == "reset_confirm", процесс сбора информации для поиска сбрасывается в начало,
    состояние устанавливается в UserStates.destination_id, пользователю будет предложено ввести город
    для поиска заново.

        * Если call.data == "cancel_confirm", то процесс сбора информации будет отменён, текущее состояние
    пользователя будет удалено.

        * Если call.data == "yes_confirm":
            - вызывается функция add_query для записи информации о запросе в БД. Функция возвращает id
            запроса в БД (для дальнейшего заполнения таблицы QueryToHotel), id запроса записывается в 
            память сценария под ключём "query_id".
            - устанавливается состояние пользователя UserStates.wait_for_results (для контроля ввода
            пользователем сообщений во времы выполнения запросов к api)
            - вызывается функция get_api_hotels_and_send_to_user, которая отвечает за поиск вариантов отлей
            и за формирование сообщений с найденной информацией, которая отправляется в чат пользователю.
            После завершения работы функции все состояния пользователя удаляются.

            '''


    bot.delete_message(call.message.chat.id, call.message.message_id)
    match call.data:

        case 'reset_confirm':
            bot.send_message(call.message.chat.id, 'Хорошо, начнем заново.\nВведите город для поиска отелей:')
            bot.set_state(call.message.chat.id, UserStates.destination_id)

        case 'cancel_confirm':
            bot.delete_state(call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Поиск отменен')

        case 'yes_confirm':
            with bot.retrieve_data(call.message.chat.id) as data:                   #type: ignore
                data['query_id'] = add_query(data)

            with open('static/waiting.tgs', 'rb') as sticker:
                bot.send_sticker(call.message.chat.id, sticker)

            bot.set_state(call.message.chat.id, UserStates.wait_for_results)

            get_hotels_from_api(data)

            bot.delete_state(call.message.chat.id)


