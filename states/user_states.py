from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    city = State()  # город, который ввёл пользователь
    user_select_id = State()  # какой вариант выбрал пользователдь
    date_of_entry = State()  # дата заезда
    departure_date = State()  # дата выезда
