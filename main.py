from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands


def main() -> None:
    '''Функция для запуска бота и создания его меню.'''
    set_default_commands(bot)
    bot.polling(non_stop=True, interval=0)


if __name__ == '__main__':
    main()
