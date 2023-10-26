import requests
from config import RAPID_API_KEY

# city = 'Rome'


def destination_id(city):
    """Функция поиска городов по наименованию введённому пользователем."""
    # locations/v3/search
    # вернуть список городов вида:
    # food_names = ["Суши", "Спагетти", "Хачапури"]
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
    print(possible_cities)
    return possible_cities


# if __name__ == "__main__":
#     destination_id('rome')

# x = list(d.keys())
#     print(x)        # ['A', 'B', 'C']
