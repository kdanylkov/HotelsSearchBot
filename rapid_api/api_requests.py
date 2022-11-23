import requests
from typing import List, Dict, Tuple
from config_data.config import HEADERS, URLS
from json import loads
from utils.misc import get_destination_options_list


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

def get_api_destinations_options(destination_to_find: str, locale_code: str):

    querystring = {"query": destination_to_find, "locale": locale_code, "currency":"RUB"}

    try:
        response = request_to_api(URLS['locations'], HEADERS, querystring)
        return get_destination_options_list(loads(response))

    except TypeError as err:
        print(f'The TypeError has occured: {err}')
        raise


if __name__ == '__main__':
    dest_options = get_api_destinations_options('New York', 'en_US')
    if dest_options:
        for dest in dest_options:
            print(dest)

    
    


