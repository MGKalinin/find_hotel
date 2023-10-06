from states.user_states import UserInfoState
from loader import bot
from telebot.types import Message
from config_data import config
import requests
import json
from utils.misc.destination import destination_id


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    bot.reply_to(message, 'Ищу дешёвые отели, введите город:')


@bot.message_handler(state=UserInfoState.input_city)
def find_city(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        bot.reply_to(message, f'Выполняю поиск в городе {data["city"]}')
        possible_options_cities = destination_id(data['city'])
        print(possible_options_cities)
