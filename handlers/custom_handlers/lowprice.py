from states.user_states import UserInfoState
from loader import bot
from telebot.types import Message
from config_data import config
import requests
import json


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    bot.reply_to(message, 'Ищу дешёвые отели, введите город:')


@bot.message_handler(state=UserInfoState.input_city)
def find_city(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        bot.reply_to(message, f'Выполняю поиск в городе {data["city"]}')
        # создаём запрос к API
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": message.text, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
        headers = {
            "X-RapidAPI-Key": config.RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        ans = json.loads(response.text)
        print(ans)

