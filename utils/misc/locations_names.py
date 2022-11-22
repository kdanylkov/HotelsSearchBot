from bs4 import BeautifulSoup as BS


def get_location_options_list(response_dict: dict) -> list:
    list_of_names = []
    
    suggestions = response_dict['suggestions']
    
    for sug in suggestions:
        if sug['group'] == 'CITY_GROUP':
            for ent in sug['entities']:
                if ent['type'] == 'CITY':
                    list_of_names.append(
                            {'id': ent['destinationId'], 'name': BS(ent['caption'], 'html.parser').text}
                    )
    
    return list_of_names


if __name__ == '__main__':
    import json

    with open('dump_london.json', 'r', encoding='utf-8') as rf:
        dump_dict = json.load(rf)
    names = get_location_options_list(dump_dict)
    for name in names:
        print(name)
