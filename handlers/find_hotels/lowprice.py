from telebot.types import Message
from states.user_data import UserInputInfo
from loader import bot
from utils.find_destination_id import destination_id


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.set_state(message.from_user.id, UserInputInfo.input_city, message.chat.id)
    bot.send_message(message.from_user.id, 'Итак, ищем дешёвые гостиницы, введите город: ')


@bot.message_handler(state=UserInputInfo.input_city)
def find_city(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
        # выполняется запрос по тому что ввёл ползователь
    bot.send_message(message.from_user.id, f"Выполняется посик в городе: {data['input_city']}")
    # получены возможные варианты городов
    possible_options = destination_id(data['input_city'])
    print(possible_options)

