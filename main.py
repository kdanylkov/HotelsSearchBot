from handlers import bot
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter


def main() -> None:
    '''Функция для запуска бота и создания его меню.'''
    set_default_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    bot.polling(non_stop=True, interval=0)


if __name__ == '__main__':
    main()
