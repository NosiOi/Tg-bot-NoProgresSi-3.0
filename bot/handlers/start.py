from aiogram import Router, types
from aiogram.filters.command import CommandStart


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Бот працює на версії Aiogram 3.0!!!")
