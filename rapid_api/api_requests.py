import requests
from config_data.config import HEADERS, URLS
from json import loads
from utils.misc import get_location_options_list


def request_to_api(url, headers, querystring) -> str:
    try:
        response = requests.get(url=url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.text
        else:
            raise requests.ConnectionError('There is an issue with your connection, no "200" status code returned')
    except requests.RequestException as exc:
        print(exc)
        raise

def fetch_locations_options(location_to_find: str, locale_code: str):

    querystring = {"query": location_to_find, "locale": locale_code, "currency":"RUB"}

    try:
        locations_dump = request_to_api(URLS['locations'], HEADERS, querystring)
        list_of_options = get_location_options_list(loads(locations_dump))
        return list_of_options
    except TypeError as err:
        print(f'The TypeError has occured: {err}')
        raise


if __name__ == '__main__':
    for loc in fetch_locations_options('New York'):
        print(loc)

    
    


