from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.main_menu import main_menu

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "Привіт! Обери дію з меню нижче:",
        reply_markup=main_menu
    )
