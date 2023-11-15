from aiogram import F, Router, types
from aiogram.filters import StateFilter, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.make_keyboard import NumbersCallbackFactory
from keyboards.make_keyboard import get_keyboard_city
from utilities.find_destination_id import destination_city, destination_hotel

router = Router()
user_data = {}

possible_cities = {'553248633938945217': 'Rome City Centre, Rome, Lazio, Italy', '3023': 'Rome, Lazio, Italy',
                   '5194566': 'Rome, Italy )',  # (FCO-Fiumicino - Leonardo da Vinci Intl.
                   '6200441': 'Rome Historic Centre, Rome, Lazio, Italy',
                   '9699': 'Rome, Georgia, United States of America', '6046253': 'Vatican, Rome, Lazio, Italy',
                   None: 'Hilton Rome Airport, Fiumicino, Lazio, Italy',
                   '9605': 'Romeoville, Illinois, United States of America',
                   '6046256': 'Trastevere, Rome, Lazio, Italy', '6341167': 'Trevi Fountain, Rome, Lazio, Italy'}
possible_hotels = {'41723': 'Comfort Inn Denver Central', '10469': 'Radisson Hotel Denver Central',
                   '5658': 'Quality Inn Aurora Denver',
                   '119229': 'Extended Stay America Select Suites Denver Aurora South',
                   '82249': 'Hyatt Place Denver Tech Center', '6852': 'Warwick Denver',
                   '163662': 'Courtyard by Marriott Denver Southwest-Lakewood',
                   '17948096': 'MainStay Suites Near Denver Downtown',
                   '551057': 'Courtyard by Marriott Denver Golden/Red Rocks',
                   '41068': 'Extended Stay America Suites Denver Lakewood South',
                   '24321': 'Holiday Inn Denver Lakewood, an IHG Hotel',
                   '7505': 'Crowne Plaza Denver Airport Convention Ctr, an IHG Hotel',
                   '41739': 'Comfort Inn Denver East', '9500': 'Courtyard by Marriott Denver Central Park',
                   '4284318': 'La Quinta Inn & Suites by Wyndham Denver Gateway Park',
                   '1164': 'Comfort Suites Near Denver Downtown', '543': 'Best Western Premier Denver East',
                   '14162': 'Best Western Denver Southwest', '22056': 'Residence Inn by Marriott Denver Downtown',
                   '439787': 'Holiday Inn Express & Suites Wheat Ridge-Denver West, an IHG Hotel',
                   '182': 'DoubleTree by Hilton Denver - Westminster',
                   '57276017': 'Hampton Inn & Suites Aurora South Denver',
                   '1700715': 'Hilton Garden Inn Denver Downtown', '23684': 'Hampton Inn Denver West Federal Center',
                   '548760': 'Residence Inn by Marriott Denver Golden/Red Rocks',
                   '6432125': 'Holiday Inn Express Hotel & Suites Denver East-Peoria Street, an IHG Hotel',
                   '208594': 'Hampton Inn & Suites Denver Tech Center',
                   '6565869': 'Home2 Suites by Hilton Denver West - Federal Center, CO',
                   '74616': 'Hampton Inn Denver-Northwest/Westminster', '15690': 'Hyatt Place Denver/Cherry Creek',
                   '1797': 'DoubleTree by Hilton Denver - Aurora',
                   '19950073': 'Holiday Inn Express & Suites Denver - Aurora Medical Campus, an IHG Hotel',
                   '46990889': 'Courtyard by Marriott Denver Aurora', '90808900': 'Kasa Rino Denver',
                   '10162': 'DoubleTree by Hilton Denver Cherry Creek',
                   '63061767': 'Origin Westminster a Wyndham Hotel', '13328': 'Holiday Inn Denver East, an IHG Hotel',
                   '61508469': 'Hyatt House Denver Aurora', '202435': 'TownePlace Suites Denver Southeast',
                   '14257': 'Renaissance Denver Central Park Hotel',
                   '17085': 'Courtyard by Marriott Denver Cherry Creek', '6727': 'Sonesta Denver Downtown',
                   '5815022': 'Hampton Inn & Suites Denver Downtown-Convention Center',
                   '9082836': 'Aloft Denver Downtown',
                   '17771': 'Fairfield Inn & Suites by Marriott Denver Cherry Creek',
                   '551479': 'TownePlace Suites By Marriott Denver Downtown', '10195': 'Sheraton Denver West Hotel',
                   '447480': 'Hilton Garden Inn Denver Tech Center',
                   '884893': 'Hampton Inn & Suites Denver - Cherry Creek',
                   '116680': 'Residence Inn by Marriott Denver North-Westminster',
                   '12432979': 'Hyatt Regency Aurora-Denver Conference Center',
                   '35754488': 'Element Denver Downtown East',
                   '33296170': 'SpringHill Suites by Marriott Denver West/Golden'}


class ChoosDestination(StatesGroup):
    choos_city = State()
    choos_hotel = State()
    choos_min_price = State()
    choos_max_price = State()


# написать в меню бота /cansel, /minimum_price?
# 1.после команды /start запрос ввести город
# 2.запрос выбрать город
@router.message()  # F.text
async def find_city(message: Message):
    await message.answer("Hi there! Fucking price!")
    user_data = message.text
    print(user_data)
    await message.answer(text="Выберите город:",
                         reply_markup=get_keyboard_city(possible_cities))
    # destination_city(message.text))


# 3.запрос ввести минимальную цену :
# a.вывести две кнопки  "цена до 200$", "цена более 200$"
# b.запрос "введите максимальную цену"
# c.запрос "введите минимальную цену"


# 4.вывод гостиниц в выбранном городе
@router.callback_query(NumbersCallbackFactory.filter())
async def find_hotel(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    # Текущее значение
    print(f'callback_data {callback_data.name_city}')
    # callback_data id_city='3023'

    await callback.message.edit_text(text=f'Вы выбрали город {callback_data}')
    # await callback.message.edit_text(text="Выберите отель:",
    #                                  reply_markup=get_keyboard_city(possible_hotels))
    # reply_markup = get_keyboard_city(possible_hotels)
    # destination_hotel(id_city=str(callback_data)))

    await callback.answer()
