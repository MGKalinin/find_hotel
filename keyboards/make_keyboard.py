from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Либо собирай билдером и делай adjust(1),
# либо поправь код выше так, чтобы каждая кнопка была в отдельном листе
# b = [[x] for x in a]
class NumbersCallbackFactory(CallbackData, prefix="city"):
    id_city: str


def get_keyboard_city(ans):
    """Функция возвращает кнопки с названием городов."""
    builder = InlineKeyboardBuilder()
    for i in ans:
        builder.button(
            text=i[1], callback_data=NumbersCallbackFactory(id_city=i[0])
        )
        builder.adjust(1)
    # print(builder.as_markup())
    return builder.as_markup()

