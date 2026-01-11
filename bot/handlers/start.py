from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.language_menu import language_menu

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "Welcome! Please choose your language:",
        reply_markup=language_menu
    )
