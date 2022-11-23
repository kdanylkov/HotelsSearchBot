from lingua import Language as lg, LanguageDetectorBuilder



language_codes = {
        'ENGLISH': ('en_US', 'USD'),
        'RUSSIAN': ('ru_RU', 'RUB')
    }

def get_locale_code_and_currency(word: str) -> str:

    languages = [lg.ENGLISH, lg.RUSSIAN]

    detector = LanguageDetectorBuilder.from_languages(*languages).build()

    locale_code_and_currency = language_codes[detector.detect_language_of(word).name] #type: ignore

    return locale_code_and_currency


if __name__ == '__main__':
    print(get_locale_code_and_currency('Санкт-Петербург'))
    print(get_locale_code_and_currency('Saint Petersburg'))
