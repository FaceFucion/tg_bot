from aiogram import Router
from aiogram.types import Message
from config import database

router = Router()

@router.message(commands=["dishes"])
async def show_dishes(message: Message):
    cursor = database.cursor()
    cursor.execute("SELECT name, price FROM dishes ORDER BY name ASC")  # Сортировка по названию
    dishes = cursor.fetchall()

    if not dishes:
        await message.answer("Список блюд пуст.")
    else:
        response = "Список блюд:\n"
        for dish in dishes:
            response += f"🍽 {dish[0]} - {dish[1]:.2f} руб.\n"
        await message.answer(response)
