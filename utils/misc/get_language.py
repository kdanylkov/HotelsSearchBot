from lingua import Language as lg, LanguageDetectorBuilder



language_codes = {
        'ENGLISH': 'en_US',
        'RUSSIAN': 'ru_RU',
    }

def get_locale_code(word: str) -> str:

    languages = [lg.ENGLISH, lg.RUSSIAN, lg.GERMAN, lg.FRENCH, lg.ITALIAN, lg.SPANISH]

    detector = LanguageDetectorBuilder.from_languages(*languages).build()

    locale_code = language_codes[detector.detect_language_of(word).name] #type: ignore

    return locale_code


if __name__ == '__main__':
    print(get_locale_code('Санкт-Петербург'))
    print(get_locale_code('Saint Petersburg'))
