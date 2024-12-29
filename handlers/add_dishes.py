from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import database
import os

router = Router()

@router.message(F.text == "/add_dish")
async def add_dish_command(message: Message):
    await message.answer("Введите название блюда:")

@router.message(F.text)
async def process_dish_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Введите цену блюда:")

@router.message(F.text)
async def process_dish_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("Цена должна быть числом.")
        return
    data = await state.get_data()
    name = data["name"]
    await state.update_data(price=price)
    await message.answer("Введите описание блюда:")

@router.message(F.text)
async def process_dish_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("Введите категорию блюда:")

@router.message(F.text)
async def process_dish_category(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)
    await message.answer("Теперь отправьте изображение блюда:")

@router.message(content_types=ContentType.PHOTO)
async def process_dish_image(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    photo = await message.bot.get_file(photo_id)
    file_path = photo.file_path
    save_path = os.path.join("images", f"{message.message_id}.jpg")
    await message.bot.download_file(file_path, save_path)

    data = await state.get_data()
    name = data["name"]
    price = data["price"]
    description = data["description"]
    category = data["category"]

    database.save_book({
        "name": name,
        "price": price,
        "cover": save_path,
        "genre": category,
        "description": description,
        "category": category,
        "image_path": save_path
    })
    await message.answer(f"Блюдо '{name}' добавлено с изображением!")

    await state.finish()
