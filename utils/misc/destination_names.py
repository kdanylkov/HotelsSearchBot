from bs4 import BeautifulSoup as BS


def get_destination_options_list(response_dict: dict):
    list_of_names = []
    
    suggestions = response_dict['suggestions']
    
    for sug in suggestions:
        if sug['group'] == 'CITY_GROUP':
            for ent in sug['entities']:
                if ent['type'] == 'CITY':

                    destination_id = ent['destinationId']
                    destination_name = BS(ent['caption'], 'html.parser')


                    list_of_names.append(
                            {'id': destination_id, 'name': destination_name}
                    )
            
            return list_of_names


def set_id_to_name_data(storage, chat_id, list_of_names: list):
    ids_to_names = {option['id']: option['name'] for option in list_of_names}
    storage.set_data(chat_id, chat_id, 'ids_to_names', ids_to_names)


if __name__ == '__main__':
    import json

    with open('dump_london.json', 'r', encoding='utf-8') as rf:
        dump_dict = json.load(rf)
    names = get_destination_options_list(dump_dict)
    if names:
        for name in names:
            print(name)
