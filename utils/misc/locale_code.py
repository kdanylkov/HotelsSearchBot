from lingua import Language as lg, LanguageDetectorBuilder



language_codes = {
        'ENGLISH': 'en_US',
        'RUSSIAN': 'ru_RU'
    }

def get_locale(word: str) -> str:
    '''
    Функция определяет язык строки и возвращает ru_RU, если строка на кириллице, либо en_US, если строка
    написана с использованием символов латиницы
    '''

    languages = [lg.ENGLISH, lg.RUSSIAN]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()

    locale_code_and_currency = language_codes[detector.detect_language_of(word).name] #type: ignore

    return locale_code_and_currency


if __name__ == '__main__':
    print(get_locale('Санкт-Петербург'))
    print(get_locale('Saint Petersburg'))
