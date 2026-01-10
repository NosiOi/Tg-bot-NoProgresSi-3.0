from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.db import add_goal, get_goals, get_stats


router = Router()


class AddGoalStates(StatesGroup):
    waiting_for_text = State()


@router.message(lambda msg: msg.text == "Мої цілі")
async def goals(message: Message):
    user_id = message.from_user.id
    goals_list = get_goals(user_id)

    if not goals_list:
        await message.answer("У тебе поки немає жодної цілі.\nНатисни “Додати задачу”, щоб створити першу.")
        return

    text_lines = ["Твої цілі:\n"]
    for goal_id, goal_text, created_at in goals_list:
        text_lines.append(f"• {goal_text}")

    await message.answer("\n".join(text_lines))


@router.message(lambda msg: msg.text == "Додати задачу")
async def add_task_start(message: Message, state: FSMContext):
    await message.answer("Введи назву задачі/цілі одним повідомленням:")
    await state.set_state(AddGoalStates.waiting_for_text)


@router.message(AddGoalStates.waiting_for_text)
async def add_task_save(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text:
        await message.answer("Текст задачі не може бути порожнім. Введи, будь ласка, ще раз.")
        return

    add_goal(user_id=user_id, text=text)
    await state.clear()

    await message.answer(f"Я додав твою ціль:\n• {text}")


@router.message(lambda msg: msg.text == "Статистика")
async def stats(message: Message):
    user_id = message.from_user.id
    stats_data = get_stats(user_id)

    total_goals = stats_data["total_goals"]

    await message.answer(
        f"Твоя статистика:\n"
        f"• Усього цілей/задач: {total_goals}"
    )
