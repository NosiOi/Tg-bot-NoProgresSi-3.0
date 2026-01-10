import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers.start import router as start_router


BOT_TOKEN = "8383656149:AAHU6a8xUof8MTxUmj238C3rX-2shKaaDI0"


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
