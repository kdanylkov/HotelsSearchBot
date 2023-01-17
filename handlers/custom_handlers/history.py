from loader import bot
from telebot.types import Message
from keyboards.inline import history_periods_keyboard
from states import UserStates


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    '''
    Обработчик команды /history. Устанавливается состояние пользователя
    UserStates.history_choice, формируется клавиатура для вариантов отображения
    истории запросов.
    '''
    bot.send_message(message.chat.id,
            'За какой период отобразить историю поиска?',
            reply_markup=history_periods_keyboard())
    bot.set_state(message.chat.id, UserStates.history_choice)
