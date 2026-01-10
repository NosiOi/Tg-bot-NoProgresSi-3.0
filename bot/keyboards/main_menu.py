from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мої цілі")],
        [KeyboardButton(text="Додати задачу")],
        [KeyboardButton(text="Статистика")],
    ],
    resize_keyboard=True
)
