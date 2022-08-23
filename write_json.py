import json


def write_to_json_file(data, filename):
    with open(f'{filename}.json', 'w', encoding='utf-8') as json_file:
        json.dump(
            data,
            json_file,
            indent=4,
            default=lambda x: x.strftime('%Y-%m-%d %H:%M')
        )
