from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard, create_a_keyboard
from utilities.find_destination_id import destination_id
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

router = Router()

# possible_cities = {'553248633938945217': 'Rome City Centre, Rome, Lazio, Italy', '3023': 'Rome, Lazio, Italy',
#                    '9699': 'Rome, Georgia, United States of America',
#                    '5194566': 'Rome, Italy (FCO-Fiumicino - Leonardo da Vinci Intl.)',
#                    '6200441': 'Rome Historic Centre, Rome, Lazio, Italy', '6046253': 'Vatican, Rome, Lazio, Italy',
#                    None: 'Hilton Rome Airport, Fiumicino, Lazio, Italy',
#                    '9605': 'Romeoville, Illinois, United States of America',
#                    '6046256': 'Trastevere, Rome, Lazio, Italy', '6341167': 'Trevi Fountain, Rome, Lazio, Italy'}

list_cities = ['Rome City Centre, Rome, Lazio, Italy', 'Rome, Lazio, Italy', 'Rome, Georgia, United States of America',
               'Rome, Italy (FCO-Fiumicino - Leonardo da Vinci Intl.)', 'Rome Historic Centre, Rome, Lazio, Italy',
               'Romeoville, Illinois, United States of America', 'Vatican, Rome, Lazio, Italy',
               'Hilton Rome Airport, Fiumicino, Lazio, Italy', 'Trastevere, Rome, Lazio, Italy',
               'Trevi Fountain, Rome, Lazio, Italy']


class ChoosingCity(StatesGroup):
    choosing_city = State()


# старт работы Введите город
@router.message(F.text)
async def find_city(message: Message):
    # possible_cities = destination_id(city=message.text)
    # list_cities = list(possible_cities.values())
    # print(f'list_cities {list_cities}')

    # await message.answer(text="Выберите город:", reply_markup=make_row_keyboard(list_cities))

    await message.answer(text="Выберите город:", reply_markup=create_a_keyboard(list_cities))



