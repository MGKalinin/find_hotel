import requests
import json
import re
from config_data import config

city_url = 'https://hotels4.p.rapidapi.com/locations/v3/search'
headers = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def destination_id(city):
    pattern = '<[^>]*>'
    querystring = {"q": city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    responce = requests.request("GET", city_url, headers=headers, params=querystring)
    data = json.loads(responce.text)
    with open('step_1', 'w') as r_file:
        json.dump(data, r_file, indent=4)
        # создаём словарь с destination_id(ключ) города ,его описание
    possible_cities = {}
    for i in data['suggestions'][0]['entities']:
        possible_cities[i['destinationId']] = re.sub(pattern, '', i['caption'])
    return possible_cities
