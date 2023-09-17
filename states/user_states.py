from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    input_city = State()  # город, который ввёл пользователь
    # date_of_entry = State()  # дата заезда
    # departure_date = State()  # дата выезда
