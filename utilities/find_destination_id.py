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
# 'min_price': '100'
# 'max_price': '300'
# 'check_in_day': '20'
# 'check_in_mon': '12'
# 'check_in_year': '2023'
# 'exit_day': '25'
# 'exit_mon': '12'
# 'exit_year': '2023'


def destination_hotel(id_city, min_price, max_price, check_in_day,
                      check_in_mon, check_in_year, exit_day, exit_mon, exit_year):
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
            "day": check_in_day,  # check_in_day
            "month": check_in_mon,  # check_in_mon
            "year": check_in_year  # check_in_year
        },
        "checkOutDate": {
            "day": exit_day,  # exit_day
            "month": exit_mon,  # exit_mon
            "year": exit_year  # exit_year
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
            "max": max_price,  # max_price
            "min": min_price  # min_price
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

    print(f'possible_hotels: {possible_hotels}')
    return possible_hotels


# https://hotels4.p.rapidapi.com/properties/v2/detail детали отеля по id отеля


# if __name__ == "__main__":
#     destination_city('rome')

user_data = {'id_city': '553248633938945217',
             'name_city': 'Rome, Lazio, Italy', 'min_price': '100',
             'max_price': '200', 'check_in_day': '01', 'check_in_mon': '02',
             'check_in_year': '2024', 'exit_day': 10, 'exit_mon': 2,
             'exit_year': 2024}

if __name__ == "__main__":
    destination_hotel('553248633938945217', 100,
                      500, 1, 2,
                      2024, 1, 2,
                      2024)

# # создаем словарь
# mydict = {"title": string, "code": integer, "data": array}
# # 1.проводим десериализацию JSON-объекта
# y = json.loads(x)
#  # 2.сериализуем его в JSON-структуру, как строку
#  x = json.dumps(mydict)

