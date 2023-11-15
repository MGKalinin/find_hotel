from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NumbersCallbackFactory(CallbackData, prefix="city"):
    id_city: str
    name_city: str


def get_keyboard_city(ans: dict):
    """Функция возвращает кнопки с названием городов."""
    builder = InlineKeyboardBuilder()
    for i in ans:
        builder.button(
            text=ans.get(i), callback_data=NumbersCallbackFactory(id_city=str(i), name_city=str(ans.get(i))))
        builder.adjust(1)
    return builder.as_markup()
