import sqlite3
from pathlib import Path

# Шлях до файлу бази даних (bot/bot.db)
DB_PATH = Path(__file__).parent / "bot.db"


def init_db():
    # Створює таблиці, якщо їх ще немає.
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        date TEXT,
        periodicity TEXT DEFAULT 'none',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'en'
        )
    """)

    conn.commit()
    conn.close()


def add_goal(user_id: int, text: str, date: str | None = None, periodicity: str = "none"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO goals (user_id, text, date, periodicity) VALUES (?, ?, ?, ?)",
        (user_id, text, date, periodicity)
    )

    conn.commit()
    conn.close()


def get_goals(user_id: int) -> list[tuple]:
    # Повертає всі цілі користувача (id, text, date, periodicity, created_at).
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, text, date, periodicity, created_at
        FROM goals
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()
    return rows


def get_stats(user_id: int) -> dict:
    # Повертає просту статистику по цілях.
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


def delete_goal(goal_id: int, user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM goals WHERE id = ? AND user_id = ?",
        (goal_id, user_id)
    )

    conn.commit()
    conn.close()


def set_language(user_id: int, lang: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (user_id, language)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET language = excluded.language
    """, (user_id, lang))

    conn.commit()
    conn.close()


def get_language(user_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    conn.close()

    return row[0] if row else "en"
