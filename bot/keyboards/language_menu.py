from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇦 Ukrainian")],
        [KeyboardButton(text="🇬🇧 English")],
        [KeyboardButton(text="🇵🇱 Polish")],
        [KeyboardButton(text="🇷🇺 Russian")],
    ],
    resize_keyboard=True
)
