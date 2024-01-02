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
from db.common.models import *

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

possible_hotels = {'790765': 'Hotel Franklin Feel The Sound', '4167485': "Hotel Giglio dell'Opera",
                   '892288': 'Hotel Cambridge', '9578388': 'Radio Hotel', '83496': 'Hotel Pineta Palace',
                   '803362': 'Hotel Medici', '89626321': 'Croce Apartments', '2794156': 'Ardeatina Park Hotel',
                   '975593': 'Pinewood Hotel Rome', '849188': 'Hotel Miami', '1570454': 'Rome Marriott Park Hotel',
                   '16515': 'Holiday Inn Rome- Eur Parco Dei Medici, an IHG Hotel', '1789376': 'Hotel Scott House Rome',
                   '9931': 'Tirreno Hotel', '1458367': 'Mancini Park Hotel', '11128712': 'Sallustio Luxury Suites',
                   '1137075': 'Best Western Blu Hotel Roma', '7316464': 'Parco De Medici Residence Hotel',
                   '2520414': 'Hotel Texas', '2046331': 'Augusta Lucilla Palace', '2533744': "Casa de' Fiori Biscione",
                   '2527992': 'Marini Park Hotel', '6622462': 'Le terrazze di San Giovanni',
                   '15880755': 'Vino e Oli Residenze', '688782': 'Mercure Eur Roma West',
                   '787218': 'Hotel Emona Aquaeductus', '852616': 'Hotel Verona', '1100496': 'Hotel Seiler',
                   '5172401': 'Hotel Giotto Flavia', '10500273': 'Roma Resort Termini', '1175865': '939 Hotel',
                   '2528760': 'Cressy', '1748604': 'Aparthotel Adagio Rome Vatican', '1054054': 'Hotel Orazia',
                   '1764788': 'Hotel Garda', '2440207': 'Garden Area Roma Eur', '893024': 'Hotel Paris',
                   '3566771': 'Novotel Roma Eur', '561909': 'Hotel Contilia', '795873': 'Hotel Torino',
                   '5438': 'Best Western Hotel Rivoli', '967942': 'Hotel del Corso', '4107722': 'Occidental Aurelia',
                   '1407349': 'Hotel Sisto V', '1060709': "Les Chambres d' Or", '1270041': 'Hotel Zone',
                   '63953': 'Quality Hotel Nova Domus', '795142': 'Antico Palazzo Rospigliosi',
                   '92498736': 'dotcampus roma city center', '1180093': 'Virginia Hotel',
                   '3523730': 'iH Hotels Roma Z3', '13928': 'Hotel Rome Garden', '793892': 'Hotel Julia',
                   '96360115': 'Borgo Ripa by Hostel Trastevere', '93012100': 'Moderno Hotel', '22841': 'Hotel Eliseo',
                   '2537397': "Town House Campo de' Fiori", '47050861': 'Hotel Varese Roma',
                   '10581311': 'Residenza Flaminio Gaio', '4916844': 'The Boutique Hotel',
                   '24710488': 'Buonanotte Roma 2', '22783660': 'Buonanotte Roma', '2532750': 'Hotel Relais dei Papi',
                   '6184234': 'Colosseo Gardens - My Extra Home', '3954728': 'Trevi 41 Hotel',
                   '20050': 'Albani Hotel Roma', '83390071': 'HOTEL NOVA DOMUS AURELIA', '11601144': 'Warmthotel',
                   '10230299': "C'est La Vie Suites", '2536108': 'Hotel City Palazzo dei Cardinali',
                   '2527645': 'LH Hotel Lloyd Rome', '915133': 'Hotel Santa Costanza', '10151959': 'Hotel Marisa',
                   '2301950': 'Suite Oriani - B&B', '87474265': 'Passepartout', '521344': 'Hotel Degli Aranci',
                   '2492730': 'Tmark Hotel Vaticano', '7472353': 'Navona Palace Luxury Inn',
                   '10411204': "Mama's Home Rome", '73565146': 'BELSTAY ROMA AURELIA',
                   '18163615': 'Rome as you feel - Grotta Pinta Apartments', '23543253': 'BoMa Country House',
                   '7520484': 'Hotel Villa Zaccardi', '11000046': '504 Corso Suites',
                   '10755': 'Radisson Blu GHR Hotel, Rome', '2535072': 'Hotel Corona', '22268731': 'The Republic Hotel',
                   '918919': 'Hotel Alpi', '1169330': 'Hotel Teatro Pace', '68528419': 'Hotel 77 Seventy-Seven',
                   '15634169': 'The Guardian Hotel', '793885': 'Hotel Pantheon', '100691369': 'Euphoria resort & spa',
                   '12984': 'Hotel Tritone', '2692239': 'Hotel La Giocca', '22914': 'Best Western Hotel President',
                   '2525872': 'Hotel Farnese', '976643': 'River Château Hotel',
                   '1179823': 'Trilussa Palace Wellness & Spa', '9309041': 'The Independent Suites',
                   '6064': 'Hotel Villa Pamphili Roma', '804918': 'Ariston', '10964': "Hotel Duca d'Alba",
                   '20611059': 'Boutique Hotel Campo dé Fiori', '112281': 'Hotel Columbia',
                   '10085': 'Starhotels Metropole', '30393800': 'Hotel San Giovanni Roma',
                   '15287533': 'Hotel The Building', '8202567': 'HiSuiteROME', '11036974': 'A.Roma Lifestyle Hotel',
                   '17114893': 'Vittoriano Suite', '519303': 'Best Western Globus Hotel',
                   '11948550': 'Unica Suites Rome', '18033670': "The H'All Tailor Suite Roma",
                   '1690280': ' ROMANICO PALACE LUXURY HOTEL & SPA', '15813797': 'Monti Palace Hotel',
                   '7567599': 'Splendor Suite Rome - Suites and Apartments ', '176648': 'Valadier Hotel',
                   '15433433': 'Hotel 87 Eighty seven', '6223984': 'Rome King Suite',
                   '15594779': 'Parlamento Boutique Hotel', '1406673': 'Golden Tulip Rome Piram',
                   '1211478': 'The Independent Hotel', '15888': 'NH Collection Roma Vittorio Veneto',
                   '18736945': 'DC Collection Spagna', '6024030': 'Rome Times Hotel',
                   '12432769': 'Piazza di Spagna Suite de Charme', '24627': ' Condotti Boutique Hotel',
                   '1443366': 'Trianon Borgo Pio', '16150648': 'Colonna Suite del Corso',
                   '792356': 'Rose Garden Palace Roma', '4850373': 'San Carlo Suite', '7785453': 'Hotel Celio'}


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
    db.create_tables([MainHotel])
    print(f'бд создана')
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
                         reply_markup=get_keyboard_city(possible_cities_disp))
    # destination_city(message.text))
    MainHotel(city=message.text).save()
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
    user_data['min_price'] = message.text
    print(f'user_data {user_data}')
    await message.answer(f'Введите максимальную стоимость отеля:')
    await state.set_state(ChoosDest.max_price)


@router.message(lambda message: not message.text.isdigit(), ChoosDest.max_price)
async def max_price_invalid(message: types.Message):
    """
    Провекра что введённая максимальная стоимость является числом.
    """
    return await message.reply("Введите числовое значение\nВведите максимальную стоимость отеля:")


@router.message(F.text, ChoosDest.max_price)
async def min_max_price(message: Message, state: FSMContext):
    """
    Получение максимальной стоимости отеля.
    """
    await message.answer(f'Максимальная стоимость отеля: {message.text}')
    user_data['max_price'] = message.text
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
    """
    Выбор даты заезда.
    """
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали дату заезда: {date.strftime("%d/%m/%Y")}')
        check_in_ans = date.strftime("%d/%m/%Y")
        user_data['check_in_day'] = check_in_ans.split('/')[0]
        user_data['check_in_mon'] = check_in_ans.split('/')[1]
        user_data['check_in_year'] = check_in_ans.split('/')[2]
        await callback_query.message.answer(f'Введите дату выезда:',
                                            reply_markup=await SimpleCalendar().start_calendar())
    print(f'user_data {user_data}')
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
        check_in_ans = date.strftime("%d/%m/%Y")
        user_data['exit_day'] = check_in_ans.split('/')[0]
        user_data['exit_mon'] = check_in_ans.split('/')[1]
        user_data['exit_year'] = check_in_ans.split('/')[2]
    print(f'user_data {user_data}')
    await callback_query.message.answer(text="Выберите отель:",
                                        reply_markup=get_keyboard_city(possible_hotels))
# user_data= {'553248633938945217': 'Rome, Lazio, Italy',
# 'min': '11', 'max': '22', 'check_in_day': '01',
# 'check_in_mon': '12', 'check_in_year': '2023',
# 'exit_day': '02', 'exit_mon': '12', 'exit_year': '2023'}
# TODO обработать Resulted callback data is too long! > 64 в кнопках
# TODO обработать выбор отеля,вывести картинки выбранного отеля
