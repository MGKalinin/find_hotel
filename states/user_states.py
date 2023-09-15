from telebot.handler_backends import State, StatesGroup


class UserInputInfo(StatesGroup):
    input_city = State()  # что ввёл пользователь
    user_select_id = State()  # какой вариант выбрал пользователдь
    date_of_entry = State()  # дата заезда
    departure_date = State()  # дата выезда
