import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import choosing_hotel


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Если не указать storage, то по умолчанию всё равно будет MemoryStorage
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(BOT_TOKEN)
    # dp.include_router(common.router)
    dp.include_router(choosing_hotel.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

