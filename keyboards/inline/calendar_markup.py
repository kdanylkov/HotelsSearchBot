from loader import calendar, calendar_1_callback
from datetime import datetime
from telebot.types import ReplyKeyboardRemove

now = datetime.now()

calendar_keyboard = calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=now.year,
                month=now.month,
                )


def create_calendar_keyboard(call, text_if_correct, text_if_incorrect, offset_date, bot):

    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day #type: ignore
    )
    if action == "DAY":
        if date < offset_date:
            bot.send_message(call.message.chat.id,
                    text_if_incorrect,
                    reply_markup=calendar_keyboard)
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
