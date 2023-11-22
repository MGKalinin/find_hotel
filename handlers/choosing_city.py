from aiogram import F, Router, types
from aiogram.filters import StateFilter, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
# from aiogram.handlers import message
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from keyboards.make_keyboard import NumbersCallbackFactory
from keyboards.make_keyboard import get_keyboard_city
from utilities.find_destination_id import destination_city, destination_hotel

router = Router()
user_data = {}

possible_cities_shot = {'553248633938945217': 'Rome City Centre', '3023': 'Rome',
                        '5194566': 'Rome (FCO-Fiumicino - Leonardo da Vinci Intl.)', '6200441': 'Rome Historic Centre',
                        '9699': 'Rome', '6046253': 'Vatican', None: 'Hilton Rome Airport', '9605': 'Romeoville',
                        '6046256': 'Trastevere', '6341167': 'Trevi Fountain'}


class ChoosDest(StatesGroup):
    city = State()  # выбор города
    hotel = State()  # выбор отеля
    min_price = State()  # выбор минимальной цены
    max_price = State()  # выбор макимальрной цены


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
                         reply_markup=get_keyboard_city(possible_cities_shot))
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


@router.message(F.text, ChoosDest.min_price)
async def min_max_price(message: Message, state: FSMContext):
    await message.answer(f'Минимальная стоимость отеля: {message.text}')
    user_data['min'] = message.text
    print(f'user_data {user_data}')
    await message.answer(f'Введите максимальную стоимость отеля:')
    await state.set_state(ChoosDest.max_price)


@router.message(F.text, ChoosDest.max_price)
async def min_max_price(message: Message, state: FSMContext):
    await message.answer(f'Ммаксимальная стоимость отеля: {message.text}')
    user_data['max'] = message.text
    print(f'user_data {user_data}')
    await message.answer(f'{user_data}')

# TODO запросить город- выбрать город-
#  запроосить мин.цену(внести в словарь?)-
#  запросить макс.цену(внести в словарь?)-
#  вывести итог:город/цена мин&макс

# TODO прописать проверку на числа мин/макс

# TODO прописать проверку на ввод буквы город
