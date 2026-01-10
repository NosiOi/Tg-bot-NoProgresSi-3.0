import os
import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers.start import router as start_router
from bot.handlers.menu import router as menu_router

print("REDEPLOY TEST")
print("ENV BOT_TOKEN:", os.getenv("BOT_TOKEN"))
print("CONFIG BOT_TOKEN:", BOT_TOKEN, type(BOT_TOKEN))


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
