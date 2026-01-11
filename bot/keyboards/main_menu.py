from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu(lang: str):
    texts = {
        "en": ["My goals", "Add task", "Statistics", "Settings"],
        "uk": ["Мої цілі", "Додати задачу", "Статистика", "Налаштування"],
        "pl": ["Moje cele", "Dodaj zadanie", "Statystyki", "Ustawienia"],
        "ru": ["Мои цели", "Добавить задачу", "Статистика", "Настройки"],
    }

    t = texts[lang]

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t[0])],
            [KeyboardButton(text=t[1])],
            [KeyboardButton(text=t[2])],
            [KeyboardButton(text=t[3])],
        ],
        resize_keyboard=True
    )
