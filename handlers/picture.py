from aiogram import Router, types
from aiogram.filters import Command
import aiohttp
import os

picture_router = Router()


@picture_router.message(Command("picture"))
async def picture_handler(message: types.Message):
    photo_url = "https://i.pinimg.com/474x/b0/f1/37/b0f137be3afc3375c669d25f153c8d17.jpg"
    local_photo_path = "temp_photo.jpg"

    # Скачиваем изображение
    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as response:
            if response.status == 200:
                with open(local_photo_path, "wb") as file:
                    file.write(await response.read())

    # Отправляем изображение как локальный файл
    photo = types.FSInputFile(local_photo_path)
    await message.answer_photo(photo=photo, caption="Котейка!")

    # Удаляем временный файл
    os.remove(local_photo_path)
