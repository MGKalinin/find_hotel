import requests
import json
from config_data import config

url = "https://hotels4.p.rapidapi.com/locations/v3/search"
headers = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def destination_id(city):
    """Фукнция создаёт запрос API и возвращает словарь со значениями id-город."""
    querystring = {"q": city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    ans = json.loads(response.text)
    possible_cities = {}
    for i in ans['sr']:
        possible_cities[i.get('gaiaId')] = i.get('regionNames')['fullName']
    # print(possible_cities)
    return possible_cities
