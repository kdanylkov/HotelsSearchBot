from os import getenv
from dotenv import load_dotenv, find_dotenv


if find_dotenv():
    load_dotenv()
    BOT_TOKEN = getenv('BOT_TOKEN')
    API_TOKEN = getenv('RAPID_API_TOKEN')


else:
    exit('The virtual variables haven\'t been loaded, since the .env file has not been located.')

DEFAULT_COMMANDS = (
        ('start', 'Запустить бота'),
        ('help', 'Вывести справку'),
        ('lowprice', 'Поиск по самой низкой цене'),
    )

headers_default = {
	"X-RapidAPI-Key": API_TOKEN,
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
