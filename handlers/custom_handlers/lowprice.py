from states.user_states import UserInfoState
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    bot.reply_to(message, 'Ищу дешёвые отели, введите город:')


@bot.message_handler(state=UserInfoState.city)
def find_city(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        bot.reply_to(message, f'Выполняю поиск в городе {data["city"]}')
