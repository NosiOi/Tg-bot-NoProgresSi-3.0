import sqlite3
from pathlib import Path

# Шлях до файлу бази даних (bot/bot.db)
DB_PATH = Path(__file__).parent / "bot.db"


def init_db():
    """Створює таблиці, якщо їх ще немає."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def add_goal(user_id: int, text: str):
    """Додає нову ціль/задачу для користувача."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO goals (user_id, text) VALUES (?, ?)",
        (user_id, text)
    )

    conn.commit()
    conn.close()


def get_goals(user_id: int) -> list[tuple]:
    """Повертає всі цілі користувача (id, text, created_at)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, text, created_at FROM goals WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_stats(user_id: int) -> dict:
    """Повертає просту статистику по цілях."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM goals WHERE user_id = ?",
        (user_id,)
    )
    total_goals = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total_goals": total_goals
    }
