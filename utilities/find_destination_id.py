import requests

from config import RAPID_API_KEY


# city = 'Rome'


def destination_city(city):
    """Функция поиска городов по наименованию введённому пользователем.
    Возвращает словарь id города: город."""
    # locations/v3/search
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    response = response.json()
    possible_cities = {}
    for i in response['sr']:
        possible_cities[i.get('gaiaId')] = i['regionNames']['fullName']
    # print(possible_cities)
    possible_cities.pop(None)
    possible_cities = possible_cities.items()
    return possible_cities


# '3023': 'Rome, Lazio, Italy'
# id_city = '3023'


def destination_hotel(id_city):
    """Функция поиска отелей в выбранном городе.
    Возвращает словарь id отеля: отель."""
    # properties/v2/list # по id локации
    import requests

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": id_city},  # id локации из
        # предыдущего запроса
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 150,
            "min": 100
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    # print(response.json())
    response = response.json()
    possible_hotels = {}
    for i in response['data']['propertySearch']['properties']:
        possible_hotels[i.get('id')] = i['name']
    # print(possible_hotels)
    return possible_hotels


# if __name__ == "__main__":
#     destination_city('rome')

# if __name__ == "__main__":
#     destination_hotel(id_city)
