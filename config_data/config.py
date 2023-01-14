'''
Конфигурационный модуль бота. 
    * BOT_TOKEN: Токен бота, полученный от BotFather (подтягивается из .env)
    * API_TOKEN: Токен для взаимодействия с api сайта hotels.com, полученный от сервиса rapidapi.com (подтягивается из .env)
    * DEFAULT_COMMANDS: список команд бота, используется для создания меню бота, а также для вывод текста справки.
    * HEADERS: Хедеры для запросов к api, содержит токен и адрес хоста.
    * URLS: Эндпоинты для взаимодействия с api сайта hotels.com
'''


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
        ('rating', 'Поиск наивысшим оценкам пользователей'),
        ('bestdeal', 'Поиск по удаленности от центра города и цене')
    )

HEADERS = {
    "content-type": "application/json",
	"X-RapidAPI-Key": API_TOKEN,
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

URLS = {
    "locations": "https://hotels4.p.rapidapi.com/locations/v3/search",
    "hotels": "https://hotels4.p.rapidapi.com/properties/v2/list",
    "photos": "https://hotels4.p.rapidapi.com/properties/v2/detail"
}
