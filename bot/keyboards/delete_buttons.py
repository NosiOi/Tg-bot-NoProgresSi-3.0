from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def delete_button(goal_id: int, lang: str):
    texts = {
        "en": "Delete",
        "uk": "Видалити",
        "pl": "Usuń",
        "ru": "Удалить",
    }

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=texts[lang], callback_data=f"del:{goal_id}")]
        ]
    )
