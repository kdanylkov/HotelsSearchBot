from os import getenv
from dotenv import load_dotenv, find_dotenv


if find_dotenv():
    load_dotenv()
    BOT_TOKEN = getenv('BOT_TOKEN')
else:
    exit('The virtual variables haven\'t been loaded, since the .env file has not been located.')

DEFAULT_COMMANDS = (
        ('start', 'Запустить бота'),
        ('help', 'Вывести справку'),
    )
