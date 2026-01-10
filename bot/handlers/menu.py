from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda msg: msg.text == "Мої цілі")
async def goals(message: Message):
    await message.answer("Тут будуть твої цілі.")


@router.message(lambda msg: msg.text == "Додати задачу")
async def add_task(message: Message):
    await message.answer("Введи назву задачі.")


@router.message(lambda msg: msg.text == "Статистика")
async def stats(message: Message):
    await message.answer("Тут буде статистика.")
