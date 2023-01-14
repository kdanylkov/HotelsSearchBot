from loader import bot
from telebot.types import Message
from states import UserStates
from keyboards.inline import if_need_photos_keyboard


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    '''
    Обработчик для команды /bestdeal (Топ отелей, наиболее подходящих по расположению и цене).
    Пользователю предлагается ввести название города, в котором будет происходить поиск отелей.

    Устанавливается состояние пользователя UserStates.destination_id (получение id города)

    В память сценария записывается критерий поиска "DISTANCE" (поиск по пользовательскому рейтингу)
    под ключём "sortOrder".

    '''
    chat_id = message.chat.id
    msg = '''
    Запущен поиск по критерию: "Отели, наиболее подходящие по расположению и цене".
В каком городе ищем?
    '''
    bot.send_message(chat_id, msg)
    bot.set_state(chat_id, state=UserStates.destination_id)
    with bot.retrieve_data(message.chat.id) as data:    #type: ignore
        data['sortOrder'] = 'DISTANCE'


@bot.message_handler(state=UserStates.price_range, is_range_correct=False)
def price_range_incorrect(message: Message) -> None:
    '''
    Обработчик пользовательского ввода диапазона цен (для команды bestdeal), для некорректного ввода.
    '''
    bot.send_message(message.chat.id,
            'Неверный формат ввода! Введите минимальную и максимальную через пробел')


@bot.message_handler(state=UserStates.price_range, is_range_correct=True)
def price_range(message: Message) -> None:
    
    '''
    Обработчик пользовательского ввода диапазона цен (для команды bestdeal), для корректного ввода.
    Диапазон цен сохраняется в память сценария под ключами price_min и price_max.
    Состояние пользователя меняется на UserStates.ask_for_photos (вопрос пользователю о необходимости
    загрузки фотографий.
    '''

    range_list = [int(number) for number in message.text.split()]     #type: ignore
    price_min, price_max = range_list

    with bot.retrieve_data(message.chat.id) as data:                    #type: ignore
        data['price_min'] = price_min
        data['price_max'] = price_max

    bot.send_message(message.chat.id, 'Загружать фотографии?', reply_markup=if_need_photos_keyboard())  #type: ignore
    bot.set_state(message.chat.id, UserStates.ask_for_photos)


    



