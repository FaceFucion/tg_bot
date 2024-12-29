from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3
from datetime import datetime

review_router = Router()

# FSM для отзывов
class RestaurantReview(StatesGroup):
    name = State()
    contact = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


reviewed_users = {}

# Подключение к базе данных
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            food_rating INTEGER NOT NULL,
            cleanliness_rating INTEGER NOT NULL,
            extra_comments TEXT,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()


@review_router.message(Command("review"))
async def start_review(message: types.Message, state: FSMContext):
    if message.from_user.id in reviewed_users:
        await message.answer("Вы уже оставляли отзыв! Спасибо.")
        return
    await message.answer("Как вас зовут? (от 2 до 50 символов)")
    await state.set_state(RestaurantReview.name)


@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    if not (2 <= len(message.text.strip()) <= 50):
        await message.answer("Имя должно быть длиной от 2 до 50 символов. Попробуйте снова.")
        return

    await state.update_data(name=message.text.strip())
    await message.answer("Введите ваш номер телефона.")
    await state.set_state(RestaurantReview.contact)


@review_router.message(RestaurantReview.contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact = message.text.strip()
    if len(contact) < 5:
        await message.answer("Контакт слишком короткий. Пожалуйста, введите корректный номер.")
        return

    await state.update_data(contact=contact)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1", "2", "3", "4", "5")
    await message.answer("Как вы оцениваете качество еды? (1 - плохо, 5 - отлично)", reply_markup=keyboard)
    await state.set_state(RestaurantReview.food_rating)


@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return

    await state.update_data(food_rating=int(message.text))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1", "2", "3", "4", "5")
    await message.answer("Как вы оцениваете чистоту заведения? (1 - плохо, 5 - отлично)", reply_markup=keyboard)
    await state.set_state(RestaurantReview.cleanliness_rating)


@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return

    await state.update_data(cleanliness_rating=int(message.text))
    await message.answer("Есть ли у вас дополнительные комментарии или жалобы?")
    await state.set_state(RestaurantReview.extra_comments)


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text.strip())

    data = await state.get_data()
    reviewed_users[message.from_user.id] = data

    # Сохранение отзыва в базу данных
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (user_id, name, contact, food_rating, cleanliness_rating, extra_comments, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        message.from_user.id,
        data["name"],
        data["contact"],
        data["food_rating"],
        data["cleanliness_rating"],
        data["extra_comments"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

    await message.answer(
        "Спасибо за ваш отзыв! Вот что вы указали:\n"
        f"\nИмя: {data['name']}"
        f"\nКонтакт: {data['contact']}"
        f"\nОценка еды: {data['food_rating']}"
        f"\nОценка чистоты: {data['cleanliness_rating']}"
        f"\nДополнительные комментарии: {data['extra_comments']}"
    )
    await state.clear()
class AddDish(StatesGroup):
    name = State()
    category = State()
    price = State()
    description = State()
admin_router = Router()
ADMIN_ID = 123456789  # Замените на ID вашего администратора


@admin_router.message(Command("add_dish"))
async def start_add_dish(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Команда доступна только администратору.")
        return
    await message.answer("Введите название блюда:")
    await state.set_state(AddDish.name)


@admin_router.message(AddDish.name)
async def process_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Введите категорию блюда (например, супы, вторые, напитки):")
    await state.set_state(AddDish.category)


@admin_router.message(AddDish.category)
async def process_dish_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text.strip())
    await message.answer("Введите цену блюда (в рублях):")
    await state.set_state(AddDish.price)


@admin_router.message(AddDish.price)
async def process_dish_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Цена должна быть числом. Попробуйте снова.")
        return
    await state.update_data(price=int(message.text))
    await message.answer("Введите описание блюда:")
    await state.set_state(AddDish.description)


@admin_router.message(AddDish.description)
async def process_dish_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data["description"] = message.text.strip()

    # Сохранение блюда в базу
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO dishes (name, category, price, description)
        VALUES (?, ?, ?, ?)
    """, (data["name"], data["category"], data["price"], data["description"]))
    conn.commit()
    conn.close()

    await message.answer(
        f"Блюдо добавлено:\n"
        f"\nНазвание: {data['name']}"
        f"\nКатегория: {data['category']}"
        f"\nЦена: {data['price']} руб."
        f"\nОписание: {data['description']}"
    )
    await state.clear()
