from handlers import bot
from utils import set_default_commands, set_custom_filters


def main() -> None:
    '''Функция для запуска бота, установки фильтров и создания его меню.'''

    set_default_commands(bot)
    set_custom_filters(bot)

    bot.infinity_polling()


if __name__ == '__main__':
    main()
