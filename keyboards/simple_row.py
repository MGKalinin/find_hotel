from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def create_a_keyboard(city_list) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру.
    :return: инлайн клавиатуру
    """
    buttons = [
        [[InlineKeyboardButton(text=sort_method_i, callback_data=sort_method_i, resize_keyboard=True)]
         for sort_method_i in city_list]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons[0])


# Либо собирай билдером и делай adjust(1),
# либо поправь код выше так, чтобы каждая кнопка была в отдельном листе
# b = [[x] for x in a]
