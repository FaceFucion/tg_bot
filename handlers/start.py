from aiogram import Router, F ,types
from aiogram.filters import Command


start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Наш сайт", url="https://online.geeks.kg/"),
                types.InlineKeyboardButton(text="Техподдержка", url="https://web.telegram.org/a/#7003773179")
            ],
            [
                types.InlineKeyboardButton(text="О нас", callback_data="about_us"),
                types.InlineKeyboardButton(text="Пожертвовать", callback_data="donate")
            ]
        ]
    )
    await message.reply(f"Привет, {name}! У меня пока что,"
                        f" всего 2 команд(/start, /picture)", reply_markup=keyboard)

@start_router.callback_query(F.data == "about_us")
async def about_us(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("На калени, На калени")

@start_router.callback_query(F.data == "donate")
async def donate(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Мбанк: +996 502 260 308, Бакай: +996 502 260 308")