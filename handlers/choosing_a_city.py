from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

from utilities.find_destination_id import destination_id

router = Router()


# possible_cities = {'553248633938945217': 'Rome City Centre, Rome, Lazio, Italy', '3023': 'Rome, Lazio, Italy',
#                    '9699': 'Rome, Georgia, United States of America',
#                    '5194566': 'Rome, Italy (FCO-Fiumicino - Leonardo da Vinci Intl.)',
#                    '6200441': 'Rome Historic Centre, Rome, Lazio, Italy', '6046253': 'Vatican, Rome, Lazio, Italy',
#                    None: 'Hilton Rome Airport, Fiumicino, Lazio, Italy',
#                    '9605': 'Romeoville, Illinois, United States of America',
#                    '6046256': 'Trastevere, Rome, Lazio, Italy', '6341167': 'Trevi Fountain, Rome, Lazio, Italy'}


# list(d.keys())
class ChoosingCity(StatesGroup):
    choosing_city = State()


# старт работы
@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Введите город:",
        reply_markup=ReplyKeyboardRemove()
    )


# Введите город
@router.message(F.text)
async def find_city(message: Message):
    possible_cities = destination_id(city=message.text)
    list_cities = list(possible_cities.values())
    print(f'list_cities {list_cities}')

    # варианты городов в клавиатуру: две строки по 4 штуки?
    await message.answer(text="Выберите город:", reply_markup=make_row_keyboard(list_cities))
