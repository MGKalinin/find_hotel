from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NumbersCallbackFactory(CallbackData, prefix="city"):
    id_city: str
    name_city: str


def get_keyboard_city(ans: dict):
    """Функция возвращает кнопки с названием городов."""
    builder = InlineKeyboardBuilder()
    trimmed = {key: ' '.join(value.split()[:6]) for key, value in ans.items()}
    for i in trimmed:
        builder.button(
            text=str(trimmed.get(i)), callback_data=NumbersCallbackFactory(id_city=str(i), name_city=str(trimmed.get(i))))
        builder.adjust(1)
    return builder.as_markup()


