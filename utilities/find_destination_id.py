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
    response = response.json()
    possible_cities = {}
    for i in response['sr']:
        possible_cities[i.get('gaiaId')] = i['regionNames']['shortName']  # shortName  fullName
        # secondaryDisplayName

    print(f'possible_cities: {possible_cities}')
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
            "day": 10,  # check_in_day
            "month": 10,  # check_in_mon
            "year": 2022  # check_in_year
        },
        "checkOutDate": {
            "day": 15,  # exit_day
            "month": 10,  # exit_mon
            "year": 2022  # exit_year
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
            "max": 150,  # здесь max цена
            "min": 100  # здесь min цена
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    possible_hotels = {}
    for i in response['data']['propertySearch']['properties']:
        possible_hotels[i.get('id')] = i['name']

    # print(f'possible_hotels: {possible_hotels}')
    return possible_hotels

# https://hotels4.p.rapidapi.com/properties/v2/detail детали отеля по id отеля


# if __name__ == "__main__":
#     destination_city('rome')

# if __name__ == "__main__":
#     destination_hotel('3023')


# # создаем словарь
# mydict = {"title": string, "code": integer, "data": array}
# # 1.проводим десериализацию JSON-объекта
# y = json.loads(x)
#  # 2.сериализуем его в JSON-структуру, как строку
#  x = json.dumps(mydict)

