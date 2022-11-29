from loader import calendar, calendar_1_callback
from datetime import datetime
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, CallbackQuery
from telebot import TeleBot

now = datetime.now()

def calendar_keyboard(year: int, month: int) -> InlineKeyboardMarkup:
    '''
    Создание клавиатуры для выбора даты.

    Arguments:
        * year: int - Год календаря
        * month: int - Месяц календаря
    Returns:
        InlineKeyboardMarkup

    '''
    calendar_keyboard = calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=year,
                month=month,
                )
    return calendar_keyboard


def create_calendar_keyboard(
        call: CallbackQuery, text_if_correct: str, text_if_incorrect: str, offset_date: datetime, bot: TeleBot) -> datetime | None:
    '''
    Функция обрабатывает данные из callback запроса, полученного при нажатии одной из кнопок клавиатуры
    календаря.

    Данные из call.data сопоставляются с заранее заданными параметрами. 
        * Если дата, выбранная пользователем, подходит под параметры, пользователю выводится сообщение
    с выбранной датой, и функция возвращает дату.
        * Если дата не подходит под параметры, пользователю выводится сообщение об ошибочном вводе,
    а также предлагается выбрать дату еще раз.
        * Если пользователь нажимает на клавиатуре кнопку "Отмена" (action == "CANCEL"), состояния пользователя
    удаляются, выводится сообщение об отмене операции.

    Arguments:
        * call: CallbackQuery - callback-запрос
        * text_if_correct: str - Текст, который выводится пользователю при корректном выборе даты
        * text_if_incorrect: str -  Текст, который выводится пользователю при некорректном выборе даты
        * offset_date: datetime - Дата, на которую проводится проверка (выбранная пользователем на клавиатуре
    дата должна быть позже, чем offset_date). При выборе даты заезда это сегодняшний день, при выборе даты
    выезда - ранее выбранная дата заезда.
        * bot: TeleBot - объект экземпляра TeleBot, через который происходит взаимодействие с api Telgram
    '''

    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day #type: ignore
    )
    if action == "DAY":
        if date < offset_date:
            bot.send_message(call.message.chat.id,
                    text_if_incorrect,
                    reply_markup=calendar_keyboard(offset_date.year, offset_date.month))
        else:
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"{text_if_correct}: {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
            return date
        
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Операция отменена.",
            reply_markup=ReplyKeyboardRemove(),
        )
        bot.delete_state(call.message.chat.id)

