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


def destination_hotel(id_city, min_price, max_price, check_in_day,
                      check_in_mon, check_in_year, exit_day, exit_mon, exit_year):
    """Функция поиска отелей в выбранном городе.
    Возвращает словарь id отеля: отель."""
    # properties/v2/list # по id локации

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

# if __name__ == "__main__":
#     destination_hotel(user_data['id_city'], user_data['min_price'],
#                       user_data['max_price'], user_data['check_in_day'],
#                       user_data['check_in_mon'],
#                       user_data['check_in_year'], user_data['exit_day'],
#                       user_data['exit_mon'],
#                       user_data['exit_year'])

# # создаем словарь
# mydict = {"title": string, "code": integer, "data": array}
# # 1.проводим десериализацию JSON-объекта
# y = json.loads(x)
#  # 2.сериализуем его в JSON-структуру, как строку
#  x = json.dumps(mydict)

def destination_room(hotel):
    """
    Функция поиска отеля по id отеля.
    Возвращает фото номера.
    """
    # properties/v2/detail детали отеля по id отеля

    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel  # id отеля "9209612"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    # print(response)
    possible_rooms = {}
    ans = []
    for i in response['data']['propertyInfo']['propertyGallery']['images']:
        # print(i)
        ans.append(i)
    # print(ans)
    for k in ans:
        # print(k['accessibilityText'])
        possible_rooms[k.get('accessibilityText')] = k['image']['url']
    # print(possible_rooms)
    return possible_rooms['Exterior, image']  # это url

# if __name__ == "__main__":
#     destination_room('9209612')

