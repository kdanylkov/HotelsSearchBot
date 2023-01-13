from loader import bot
from telebot.types import Message
from states import UserStates


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
    with bot.retrieve_data(message.chat.id) as data:
        data['sortOrder'] = 'DISTANCE'

