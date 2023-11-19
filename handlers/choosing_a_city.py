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


class ChoosDestination(StatesGroup):
    choos_city = State()  # выбор города
    choos_hotel = State()  # выбор отеля
    choos_min_price = State()  # выбор минимальной цены
    choos_max_price = State()  # выбор макимальрной цены


@router.message(Command(commands=["start"]))
# Начало работы бота по команде /start
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
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


# TODO после команды /start запрос ввести город; после ввода города выводит кнопки с городами
@router.message(F.text)
# выбор города из доступных
async def find_city(message: Message):
    await message.answer(text="Выберите город:",
                         reply_markup=get_keyboard_city(possible_cities_shot))
    # destination_city(message.text))


# TODO считывает callback_data выбранного города
@router.callback_query(NumbersCallbackFactory.filter())
# отображение выбраного города
async def find_hotel(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext
):
    # Текущее значение
    print(f'callback_data name:{callback_data.name_city},id:{callback_data.id_city}')
    # callback_data id_city='3023'
    await callback.message.edit_text(text=f'Вы выбрали город {callback_data.name_city}, введите цену:')
    # await callback.message.edit_text(text="Выберите отель:",
    #                                  reply_markup=get_keyboard_city(possible_hotels))
    # reply_markup = get_keyboard_city(destination_hotel(id_city=str(callback_data))))
    await callback.answer()
    await state.set_state(ChoosDestination.choos_min_price)


# TODO к выполнению этого шага не переходит
@router.message(F.text, ChoosDestination.choos_min_price)
async def min_max_price(message: Message, state: FSMContext):
    print(f'message.text {message.text}')
    # user_data['min'] = message.text
    # print(f'user_data {user_data}')
    await message.answer(f'Введите минимальнуюю стоимость отеля:{message.text}')
    await state.set_state(ChoosDestination.choos_max_price)

# @router.message(Command('start'))
# async def foo(_, state):
#     await _.answer('Хендлер 1')
#     await state.set_state(ChoosDestination.choos_city)
#
#
# @router.message(ChoosDestination.choos_city)
# async def boo(_, state):
#     await _.answer('Хендлер 2')
#     await state.set_state(None)

# Максим, [19 нояб. 2023 г., 16:13:43]:
# /start
#
# zaprosyan, [19 нояб. 2023 г., 16:13:43]:
# Хендлер 1
#
# Максим, [19 нояб. 2023 г., 16:14:11]:
# 12
#
# zaprosyan, [19 нояб. 2023 г., 16:14:11]:
# Хендлер 2
#
# Максим, [19 нояб. 2023 г., 16:14:21]:
# 12
