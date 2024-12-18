from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

review_router = Router()


class RestaurantReview(StatesGroup):
    name = State()
    contact = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


reviewed_users = {}


@review_router.message(Command("review"))
async def start_review(message: types.Message, state: FSMContext):
    if message.from_user.id in reviewed_users:
        await message.answer("Вы уже оставляли отзыв! Спасибо.")
        return
    await message.answer("Как вас зовут?")
    await state.set_state(RestaurantReview.name)


@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона или Instagram.")
    await state.set_state(RestaurantReview.contact)


@review_router.message(RestaurantReview.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1", "2", "3", "4", "5")
    await message.answer("Как вы оцениваете качество еды? (1 - плохо, 5 - отлично)", reply_markup=keyboard)
    await state.set_state(RestaurantReview.food_rating)


@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return
    await state.update_data(food_rating=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1", "2", "3", "4", "5")
    await message.answer("Как вы оцениваете чистоту заведения? (1 - плохо, 5 - отлично)", reply_markup=keyboard)
    await state.set_state(RestaurantReview.cleanliness_rating)


@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return
    await state.update_data(cleanliness_rating=message.text)
    await message.answer("Есть ли у вас дополнительные комментарии или жалобы?")
    await state.set_state(RestaurantReview.extra_comments)


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()
    reviewed_users[message.from_user.id] = data

    await message.answer(
        "Спасибо за ваш отзыв! Вот что вы указали:\n"
        f"\nИмя: {data['name']}"
        f"\nКонтакт: {data['contact']}"
        f"\nОценка еды: {data['food_rating']}"
        f"\nОценка чистоты: {data['cleanliness_rating']}"
        f"\nДополнительные комментарии: {data['extra_comments']}"
    )
    await state.clear()
