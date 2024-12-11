from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


opros_router = Router()

class Opros(StatesGroup):
    name = State()
    age = State()
    genre = State()

@opros_router.message(Command("opros"))
async def start_opros(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(Opros.name)

@opros_router.message(Opros.name)
async def start_opros(message: types.Message, state: FSMContext):
    name = message.text
    print(name)
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Opros.age)

@opros_router.message(Opros.age)
async def start_opros(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, вводите только цифры")
        return
    age = int(age)
    if age < 4 or age > 90:
        await message.answer("Укажите ваш текущий возраст")
        return
    await state.update_data(age=message.text)
    await message.answer("Укажите ваш любимый жанр фильмов")
    await state.set_state(Opros.genre)

@opros_router.message(Opros.genre)
async def start_opros(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("Спасибо за пройденный опрос!")
    data = await state.get_data()
    print(data)
    await state.clear()