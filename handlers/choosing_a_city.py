from aiogram import F, Router, types
from aiogram.types import Message
from keyboards.make_keyboard import get_keyboard_city
from utilities.find_destination_id import destination_city, destination_hotel
from keyboards.make_keyboard import NumbersCallbackFactory

router = Router()
user_data = {}


# Есть понимание, что каждой записи из available cities
# надо сопоставить какой-нибудь айди и где-то это хранить. Ну например:
#
# 1 - Москва
# 2 - Вашингтон
# 3 - Рим
# 4 - Сызрань

# Создать объект callbackdata с общим префиксом. Например, city

# И при генерации клавиатуры тогда в кнопках будет зашито
# "city:1"
# "city:2"
# "city:3"

# res_city = {'553248633938945217': 'Rome City Centre, Rome, Lazio, Italy', '3023': 'Rome, Lazio, Italy',
#             '5194566': 'Rome, Italy (FCO-Fiumicino - Leonardo da Vinci Intl.)',
#             '6200441': 'Rome Historic Centre, Rome, Lazio, Italy', '9699': 'Rome, Georgia, United States of America',
#             '6165': 'Rome, New York, United States of America', '6046253': 'Vatican, Rome, Lazio, Italy',
#             None: 'Hilton Rome Airport, Fiumicino, Lazio, Italy',
#             '9605': 'Romeoville, Illinois, United States of America', '6046256': 'Trastevere, Rome, Lazio, Italy'}

# possible_hotels={'7316464': 'Parco De Medici Residence Hotel',
# '1458367': 'Mancini Park Hotel', '2542677': 'Mirage'}

@router.message(F.text)
async def find_city(message: Message):
    await message.answer(text="Выберите город:",
                         reply_markup=get_keyboard_city(destination_city(message.text)))


@router.callback_query(NumbersCallbackFactory.filter())
async def find_hotel(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    # Текущее значение
    print(f'callback_data {callback_data}')
    # callback_data id_city = '3023'

    await callback.message.edit_text(text="Выберите отель:",
                                     reply_markup=get_keyboard_city(destination_hotel(id_city=callback_data)))
    await callback.answer()

# if __name__ == '__main__':
#     get_keyboard_city(ans)
