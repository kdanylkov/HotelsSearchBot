from telebot.util import quick_markup


def currency_keyboard():
    '''
    Создание inline клавиатуры для выбора валюты
    '''

    return quick_markup({
        'USD': {'callback_data': 'USD'},
        'EUR': {'callback_data': 'EUR'},
        'GBP': {'callback_data': 'GBP'},
        'RUB': {'callback_data': 'RUB'},
        'CNY': {'callback_data': 'CNY'},
        'UAH': {'callback_data': 'UAH'},
        'BYN': {'callback_data': 'BYN'},
        'KZT': {'callback_data': 'KZT'}
    },
    row_width=4)
        
