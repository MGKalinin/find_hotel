from aiogram import F, Router, types
from aiogram.filters import StateFilter, state
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
# from aiogram.handlers import message
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from keyboards.make_keyboard import NumbersCallbackFactory
from keyboards.make_keyboard import get_keyboard_city
from utilities.find_destination_id import destination_city, destination_hotel
from datetime import date

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar

router = Router()
user_data = {}

possible_cities_shot = {'553248633938945217': 'Rome City Centre', '3023': 'Rome',
                        '5194566': 'Rome (FCO-Fiumicino - Leonardo da Vinci Intl.)', '6200441': 'Rome Historic Centre',
                        '9699': 'Rome', '6046253': 'Vatican', None: 'Hilton Rome Airport', '9605': 'Romeoville',
                        '6046256': 'Trastevere', '6341167': 'Trevi Fountain'}

possible_cities_full = {'553248633938945217': 'Rome City Centre, Rome, Lazio, Italy', '3023': 'Rome, Lazio, Italy',
                        '5194566': 'Rome, Italy (FCO-Fiumicino - Leonardo da Vinci Intl.)',
                        '6200441': 'Rome Historic Centre, Rome, Lazio, Italy',
                        '9699': 'Rome, Georgia, United States of America', '6046253': 'Vatican, Rome, Lazio, Italy',
                        None: 'Hilton Rome Airport, Fiumicino, Lazio, Italy',
                        '9605': 'Romeoville, Illinois, United States of America',
                        '6046256': 'Trastevere, Rome, Lazio, Italy', '6341167': 'Trevi Fountain, Rome, Lazio, Italy'}

possible_cities_disp = {'553248633938945217': 'Rome, Lazio, Italy', '3023': 'Lazio, Italy', '5194566': 'Italy',
                        '6200441': 'Rome, Lazio, Italy', '9699': 'Georgia, United States',
                        '6046253': 'Rome, Lazio, Italy', None: 'Fiumicino, Lazio, Italy',
                        '9605': 'Illinois, United States', '6046256': 'Rome, Lazio, Italy',
                        '6341167': 'Rome, Lazio, Italy'}


class ChoosDest(StatesGroup):
    city = State()  # выбор города
    hotel = State()  # выбор отеля
    min_price = State()  # выбор минимальной цены
    max_price = State()  # выбор макимальрной цены
    calend = State()  # календарь
    check_in = State()  # дата заезда
    exit = State()  # дата выезда


# .isalpha()
@router.message(Command(commands=["start"]))
# Начало работы бота по команде /start
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ChoosDest.city)
    await message.answer(
        text="Введите город:",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
# Отмена работы бота по команде /cancel
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text, ChoosDest.city)
# выбор города из доступных
async def find_city(message: Message, state: FSMContext):
    await message.answer(text="Выберите город:",
                         reply_markup=get_keyboard_city(possible_cities_disp))
    # destination_city(message.text))
    await state.set_state(ChoosDest.hotel)


@router.callback_query(NumbersCallbackFactory.filter(), ChoosDest.hotel)
async def find_hotel(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext
):
    user_data[callback_data.id_city] = callback_data.name_city
    print(f'user_data {user_data}')
    # await callback.message.edit_text(text=f'Вы выбрали город {callback_data.name_city}')

    # await callback.message.edit_text(text="Выберите отель:",
    #                                  reply_markup=get_keyboard_city(possible_hotels))
    # reply_markup = get_keyboard_city(destination_hotel(id_city=str(callback_data))))
    await callback.message.answer(f'Введите минимальную стоимость отеля:')
    await state.set_state(ChoosDest.min_price)


@router.message(lambda message: not message.text.isdigit(), ChoosDest.min_price)
async def min_price_invalid(message: types.Message):
    """
    Если введёное минимальное значение не числовое.
    """
    return await message.reply("Введите числовое значение\nВведите минимальную стоимость отеля:")


@router.message(F.text, ChoosDest.min_price)
async def min_max_price(message: Message, state: FSMContext):
    await message.answer(f'Минимальная стоимость отеля: {message.text}')
    user_data['min'] = message.text
    print(f'user_data {user_data}')
    await message.answer(f'Введите максимальную стоимость отеля:')
    await state.set_state(ChoosDest.max_price)


@router.message(lambda message: not message.text.isdigit(), ChoosDest.max_price)
async def max_price_invalid(message: types.Message):
    """
    Если введёное максимальное значение не числовое.
    """
    return await message.reply("Введите числовое значение\nВведите минимальную стоимость отеля:")


@router.message(F.text, ChoosDest.max_price)
async def min_max_price(message: Message, state: FSMContext):
    await message.answer(f'Максимальная стоимость отеля: {message.text}')
    user_data['max'] = message.text
    print(f'user_data {user_data}')
    await message.answer(f'{user_data}')
    await message.answer(text="Выберите дату заезда:",
                         reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(ChoosDest.check_in)


@router.callback_query(SimpleCalendarCallback.filter(), ChoosDest.check_in)
async def process_simple_calendar(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали дату заезда: {date.strftime("%d/%m/%Y")}')
        user_data['check_in'] = date.strftime("%d/%m/%Y")
        await callback_query.message.answer(f'Введите дату выезда:',
                                            reply_markup=await SimpleCalendar().start_calendar())
    print(f'user_data {user_data}')
    await state.set_state(ChoosDest.exit)


@router.callback_query(SimpleCalendarCallback.filter(), ChoosDest.exit)
async def process_simple_calendar(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали дату выезда: {date.strftime("%d/%m/%Y")}')
        user_data['exit'] = date.strftime("%d/%m/%Y")
    print(f'user_data {user_data}')


