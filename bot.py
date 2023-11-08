import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# from config_reader import config
from handlers import common, choosing_a_city
from config import BOT_TOKEN


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Если не указать storage, то по умолчанию всё равно будет MemoryStorage
    # Но явное лучше неявного =]
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(BOT_TOKEN)  # config.bot_token.get_secret_value()

    # dp.include_router(ordering_food.router)

    # сюда импортируйте ваш собственный роутер - поиск городов
    dp.include_router(common.router)  # потом вернуть-здесь старт/отмена
    dp.include_router(choosing_a_city.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

