from aiogram import Router, types
from aiogram.filters import Command

picture_router = Router()


@picture_router.message(Command("picture"))
async def picture_handler(message: types.Message):
    photo = types.FSInputFile("https://i.pinimg.com/474x/b0/f1/37/b0f137be3afc3375c669d25f153c8d17.jpg")
    await message.answer_photo(photo=photo, caption="Котейка!")


@picture_router.message(Command("pic"))
async def pic_handler(message: types.Message): ...