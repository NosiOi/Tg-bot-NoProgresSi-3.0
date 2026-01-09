from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = [
        [KeyboardButton(text="Мої цілі")],
        [KeyboardButton(text="Профіль")],
        [KeyboardButton(text="Допомога")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
