from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.db import add_goal, get_goals, get_stats, set_language, get_language, delete_goal
from bot.keyboards.main_menu import main_menu
from bot.keyboards.language_menu import language_menu
from bot.keyboards.delete_buttons import delete_button

router = Router()


# FSM для задач
class AddGoalStates(StatesGroup):
    waiting_for_text = State()


class AddGoalWithDate(StatesGroup):
    choose_type = State()
    waiting_for_text = State()
    waiting_for_date = State()
    waiting_for_periodicity = State()


# Вибір мови
@router.message(lambda msg: msg.text in [
    "🇺🇦 Ukrainian", "🇬🇧 English", "🇵🇱 Polish", "🇷🇺 Russian"
])
async def choose_language(message: Message):
    user_id = message.from_user.id

    lang_map = {
        "🇺🇦 Ukrainian": "uk",
        "🇬🇧 English": "en",
        "🇵🇱 Polish": "pl",
        "🇷🇺 Russian": "ru",
    }

    lang = lang_map[message.text]
    set_language(user_id, lang)

    texts = {
        "en": "Language saved. Choose an option:",
        "uk": "Мову збережено. Обери дію:",
        "pl": "Język zapisany. Wybierz opcję:",
        "ru": "Язык сохранён. Выбери действие:",
    }

    await message.answer(texts[lang], reply_markup=main_menu(lang))


# Мої цілі
@router.message(lambda msg: msg.text in ["Мої цілі", "My goals", "Moje cele", "Мои цели"])
async def goals(message: Message):
    user_id = message.from_user.id
    lang = get_language(user_id)

    goals_list = get_goals(user_id)

    empty_text = {
        "en": "You have no goals yet.",
        "uk": "У тебе поки немає жодної цілі.",
        "pl": "Nie masz jeszcze żadnych celów.",
        "ru": "У тебя пока нет целей.",
    }

    header = {
        "en": "Your goals:",
        "uk": "Твої цілі:",
        "pl": "Twoje cele:",
        "ru": "Твои цели:",
    }

    if not goals_list:
        await message.answer(empty_text[lang])
        return

    await message.answer(header[lang])

    for goal_id, text, date, periodicity, created_at in goals_list:
        extra = ""

        if date:
            extra += f"\n📅 {date}"

        if periodicity != "none":
            icons = {
                "daily": "🔁 daily",
                "weekly": "🔁 weekly",
                "monthly": "🔁 monthly",
                "yearly": "🔁 yearly",
            }
            extra += f"\n{icons.get(periodicity, '')}"

        await message.answer(
            f"• {text}{extra}",
            reply_markup=delete_button(goal_id, lang)
        )


# Додати задачу → вибір типу
@router.message(lambda msg: msg.text in ["Додати задачу", "Add task", "Dodaj zadanie", "Добавить задачу"])
async def add_task_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_language(user_id)

    texts = {
        "en": "Choose task type:",
        "uk": "Обери тип задачі:",
        "pl": "Wybierz typ zadania:",
        "ru": "Выбери тип задачи:",
    }

    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    types = {
        "en": ["Simple task", "Task with date", "Repeating task"],
        "uk": ["Звичайна задача", "Задача з датою", "Повторювана задача"],
        "pl": ["Zwykłe zadanie", "Zadanie z datą", "Zadanie cykliczne"],
        "ru": ["Обычная задача", "Задача с датой", "Повторяющаяся задача"],
    }

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=types[lang][0])],
            [KeyboardButton(text=types[lang][1])],
            [KeyboardButton(text=types[lang][2])],
        ],
        resize_keyboard=True
    )

    await message.answer(texts[lang], reply_markup=keyboard)
    await state.set_state(AddGoalWithDate.choose_type)


# Обробка вибору типу задачі
@router.message(AddGoalWithDate.choose_type)
async def choose_task_type(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    text = message.text

    simple = ["Звичайна задача", "Simple task",
              "Zwykłe zadanie", "Обычная задача"]
    dated = ["Задача з датою", "Task with date",
             "Zadanie z datą", "Задача с датой"]
    repeating = ["Повторювана задача", "Repeating task",
                 "Zadanie cykliczne", "Повторяющаяся задача"]

    if text in simple:
        await state.update_data(type="simple")
    elif text in dated:
        await state.update_data(type="dated")
    elif text in repeating:
        await state.update_data(type="repeating")
    else:
        return

    ask_text = {
        "en": "Enter task name:",
        "uk": "Введи назву задачі:",
        "pl": "Wpisz nazwę zadania:",
        "ru": "Введите название задачи:",
    }

    await message.answer(ask_text[lang])
    await state.set_state(AddGoalWithDate.waiting_for_text)


# Введення тексту задачі
@router.message(AddGoalWithDate.waiting_for_text)
async def process_text(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    text = message.text.strip()

    await state.update_data(text=text)
    data = await state.get_data()

    if data["type"] == "simple":
        add_goal(message.from_user.id, text)
        await state.clear()
        await message.answer({"en": "Task added.", "uk": "Задачу додано.", "pl": "Zadanie dodane.", "ru": "Задача добавлена."}[lang])
        return

    if data["type"] == "dated":
        ask_date = {
            "en": "Enter date (DD-MM-YYYY):",
            "uk": "Введи дату (ДД-ММ-РРРР):",
            "pl": "Wpisz datę (DD-MM-RRRR):",
            "ru": "Введите дату (ДД-ММ-ГГГГ):",
        }
        await message.answer(ask_date[lang])
        await state.set_state(AddGoalWithDate.waiting_for_date)
        return

    if data["type"] == "repeating":
        ask_period = {
            "en": "Choose repetition: daily / weekly / monthly / yearly",
            "uk": "Обери повторення: щодня / щотижня / щомісяця / щороку",
            "pl": "Wybierz powtarzanie: codziennie / co tydzień / co miesiąc / co rok",
            "ru": "Выбери повторение: ежедневно / еженедельно / ежемесячно / ежегодно",
        }
        await message.answer(ask_period[lang])
        await state.set_state(AddGoalWithDate.waiting_for_periodicity)


# Задача з датою
@router.message(AddGoalWithDate.waiting_for_date)
async def save_dated_task(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    date = message.text.strip()
    data = await state.get_data()

    add_goal(message.from_user.id, data["text"], date=date)
    await state.clear()

    await message.answer({
        "en": "Task with date added.",
        "uk": "Задачу з датою додано.",
        "pl": "Zadanie z datą dodane.",
        "ru": "Задача с датой добавлена.",
    }[lang])


# Повторювана задача
@router.message(AddGoalWithDate.waiting_for_periodicity)
async def save_repeating_task(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    periodicity = message.text.lower().strip()

    mapping = {
        "daily": "daily", "щодня": "daily", "codziennie": "daily", "ежедневно": "daily",
        "weekly": "weekly", "щотижня": "weekly", "co tydzień": "weekly", "еженедельно": "weekly",
        "monthly": "monthly", "щомісяця": "monthly", "co miesiąc": "monthly", "ежемесячно": "monthly",
        "yearly": "yearly", "щороку": "yearly", "co rok": "yearly", "ежегодно": "yearly",
    }

    if periodicity not in mapping:
        await message.answer({"en": "Invalid option.", "uk": "Невірний варіант.", "pl": "Nieprawidłowa opcja.", "ru": "Неверный вариант."}[lang])
        return

    data = await state.get_data()
    add_goal(message.from_user.id, data["text"],
             periodicity=mapping[periodicity])
    await state.clear()

    await message.answer({
        "en": "Repeating task added.",
        "uk": "Повторювану задачу додано.",
        "pl": "Zadanie cykliczne dodane.",
        "ru": "Повторяющаяся задача добавлена.",
    }[lang])


# Статистика
@router.message(lambda msg: msg.text in ["Статистика", "Statistics", "Statystyki", "Статистика"])
async def stats(message: Message):
    user_id = message.from_user.id
    lang = get_language(user_id)

    stats_data = get_stats(user_id)
    total = stats_data["total_goals"]

    text = {
        "en": f"Your statistics:\n• Total goals: {total}",
        "uk": f"Твоя статистика:\n• Усього цілей: {total}",
        "pl": f"Twoje statystyki:\n• Łącznie celów: {total}",
        "ru": f"Твоя статистика:\n• Всего целей: {total}",
    }

    await message.answer(text[lang])


# Налаштування
@router.message(lambda msg: msg.text in ["Settings", "Налаштування", "Ustawienia", "Настройки"])
async def settings_menu(message: Message):
    lang = get_language(message.from_user.id)

    texts = {
        "en": "Settings:\n• Change language",
        "uk": "Налаштування:\n• Змінити мову",
        "pl": "Ustawienia:\n• Zmień język",
        "ru": "Настройки:\n• Изменить язык",
    }

    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    change_lang_btn = {
        "en": "Change language",
        "uk": "Змінити мову",
        "pl": "Zmień język",
        "ru": "Изменить язык",
    }

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=change_lang_btn[lang])]],
        resize_keyboard=True
    )

    await message.answer(texts[lang], reply_markup=keyboard)


# Змінити мову
@router.message(lambda msg: msg.text in ["Change language", "Змінити мову", "Zmień język", "Изменить язык"])
async def change_language(message: Message):
    lang = get_language(message.from_user.id)

    texts = {
        "en": "Choose your language:",
        "uk": "Обери мову:",
        "pl": "Wybierz język:",
        "ru": "Выбери язык:",
    }

    await message.answer(texts[lang], reply_markup=language_menu)


# Видалення задачі
@router.callback_query(lambda c: c.data.startswith("del:"))
async def delete_goal_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_language(user_id)

    goal_id = int(callback.data.split(":")[1])
    delete_goal(goal_id, user_id)

    texts = {
        "en": "Goal deleted.",
        "uk": "Ціль видалено.",
        "pl": "Cel usunięty.",
        "ru": "Цель удалена.",
    }

    await callback.message.edit_text(texts[lang])
    await callback.answer()
