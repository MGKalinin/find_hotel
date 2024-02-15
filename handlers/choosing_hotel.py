from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
# from aiogram.handlers import message
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from keyboards.make_keyboard import NumbersCallbackFactory
from keyboards.make_keyboard import get_keyboard_city

from aiogram.types import CallbackQuery

from db.database import *
from utilities.find_destination_id import destination_city, destination_hotel, destination_room

router = Router()
user_data = {}


class ChoosDest(StatesGroup):
    city = State()  # выбор города
    hotel = State()  # выбор отеля
    min_price = State()  # выбор минимальной цены
    max_price = State()  # выбор макимальрной цены
    calend = State()  # календарь
    check_in = State()  # дата заезда
    exit = State()  # дата выезда
    show_room = State()  # показть фото номера в отеле


# .isalpha()
@router.message(Command(commands=["start"]))
# Начало работы бота по команде /start
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ChoosDest.city)
    # создать таблицу
    metadata.create_all(engine)
    print(f'бд создана')

    # message.from_user.id
    print(f'message.from_user.id {message.from_user.id}')
    user_data['user_id'] = message.from_user.id
    print(f'user_data {user_data}')
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
    """
    Выбор города из доступных.
    """
    await message.answer(text="Выберите город:",
                         # reply_markup=get_keyboard_city(possible_cities_full))  # это для теста
                         reply_markup=get_keyboard_city(destination_city(message.text)))  # это реал
    await state.set_state(ChoosDest.hotel)


@router.callback_query(NumbersCallbackFactory.filter(), ChoosDest.hotel)
async def find_hotel(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext
):
    """
    Получение id выбранного города.
    """
    # user_data[callback_data.id_city] = callback_data.name_city
    user_data['id_city'] = callback_data.id_city
    user_data['name_city'] = callback_data.name_city
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
    Проверка что введённая минимальная стоимость является числом.
    """
    return await message.reply("Введите числовое значение\nВведите минимальную стоимость отеля:")


@router.message(F.text, ChoosDest.min_price)
async def min_max_price(message: Message, state: FSMContext):
    """
    Получение минимальной стоимости отеля.
    """
    await message.answer(f'Минимальная стоимость отеля: {message.text}')
    user_data['min_price'] = int(message.text)
    print(f'user_data {user_data}')
    await message.answer(f'Введите максимальную стоимость отеля:')
    await state.set_state(ChoosDest.max_price)


@router.message(lambda message: not message.text.isdigit(), ChoosDest.max_price)
async def max_price_invalid(message: types.Message):
    """
    Проверка что введённая максимальная стоимость является числом.
    """
    return await message.reply("Введите числовое значение\nВведите максимальную стоимость отеля:")


@router.message(F.text, ChoosDest.max_price)
async def min_max_price(message: Message, state: FSMContext):
    """
    Получение максимальной стоимости отеля.
    """
    await message.answer(f'Максимальная стоимость отеля: {message.text}')
    user_data['max_price'] = int(message.text)
    print(f'user_data {user_data}')
    # await message.answer(f'{user_data}')
    await message.answer(text="Выберите дату заезда:",
                         reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(ChoosDest.check_in)


@router.callback_query(SimpleCalendarCallback.filter(), ChoosDest.check_in)
async def process_simple_calendar(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext):
    """
    Выбор даты заезда.
    """
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали дату заезда: {date.strftime("%d/%m/%Y")}')
        check_in_ans = date.strftime("%d/%m/%Y")
        user_data['check_in_ans'] = check_in_ans
        user_data['check_in_day'] = int(check_in_ans.split('/')[0])
        user_data['check_in_mon'] = int(check_in_ans.split('/')[1])
        user_data['check_in_year'] = int(check_in_ans.split('/')[2])
        await callback_query.message.answer(f'Введите дату выезда:',
                                            reply_markup=await SimpleCalendar().start_calendar())
    # print(f'user_data {user_data}')
    await state.set_state(ChoosDest.exit)


@router.callback_query(SimpleCalendarCallback.filter(), ChoosDest.exit)
async def process_simple_calendar(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext):
    """
    Выбор даты выезда.
    """
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали дату выезда: {date.strftime("%d/%m/%Y")}')
        check_out_ans = date.strftime("%d/%m/%Y")
        user_data['check_out_ans'] = check_out_ans
        user_data['exit_day'] = int(check_out_ans.split('/')[0])
        user_data['exit_mon'] = int(check_out_ans.split('/')[1])
        user_data['exit_year'] = int(check_out_ans.split('/')[2])
    # print(f'user_data {user_data}')
    await callback_query.message.answer(text="Выберите отель:",
                                        # reply_markup=get_keyboard_city(possible_hotels))  # это тест
                                        reply_markup=get_keyboard_city(
                                            destination_hotel(id_city=str(callback_data),
                                                              min_price=user_data['min_price'],
                                                              max_price=user_data['max_price'],
                                                              check_in_day=user_data['check_in_day'],
                                                              check_in_mon=user_data['check_in_mon'],
                                                              check_in_year=user_data['check_in_year'],
                                                              exit_day=user_data['exit_day'],
                                                              exit_mon=user_data['exit_mon'],
                                                              exit_year=user_data['exit_year'])))  # это реал

    await state.set_state(ChoosDest.show_room)


@router.callback_query(NumbersCallbackFactory.filter(), ChoosDest.show_room)
async def show_foto_rooms(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext

):
    """
    По id отеля показывает фото.
    """
    user_data['id_hotel'] = callback_data.id_city
    user_data['name_hotel'] = callback_data.name_city
    # print(f'user_data {user_data}')

    # url = possible_rooms['Exterior, image']

    # url = [value for value in possible_rooms.values()]  # это тест здесь написать функцию destination_room
    # await callback.message.answer_photo(text="Просмотрите фото:", photo=url)  # reply_photo

    url = [value for value in destination_room(user_data['id_hotel']).values()]  # это реал
    for i in url:
        await callback.message.answer_photo(photo=i)  # text="Просмотрите фото:",

    # добавить элементы в базу данных
    make_entry = hotels.insert().values([
        {'user_id': user_data['user_id'],
         'name_city': user_data['name_city'],
         'name_hotel': user_data['name_hotel'],
         'min_price': user_data['min_price'],
         'max_price': user_data['max_price'],
         'check_in_day': user_data['check_in_ans'],
         'exit_day': user_data['check_out_ans']
         }])

    # запись новых данных
    conn.execute(make_entry)

    await callback.message.answer(f'Ввод данных окончен.')


@router.message(Command(commands=["history"]))
# Начало работы бота по команде /start
async def cmd_start(message: Message, state: FSMContext):
    """
    По команде /history выводит историю запросов.
    """

    # select_all_query = db.select([hotels])
    select_all_query = db.select([hotels]).where(hotels.columns.user_id == '400997168')
    # select_all_query = db.select([hotels]).where(hotels.columns.min_price == 200)
    select_all_results = conn.execute(select_all_query)
    res = select_all_results.fetchall()
    print(f'это res: {res}')

    await message.answer(
        text=f"История запросов")

    for item in res:
        await message.answer(text=' '.join(item[2:4]))
