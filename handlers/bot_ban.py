import re
from datetime import timedelta
from aiogram import Dispatcher, F
from aiogram.types import Message
from config import FORBIDDEN_WORDS
#я матерные слова на сайте скопировал и в конфиг внёс, надеюсь нормально
def contains_forbidden_words(message_text: str) -> bool:
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, FORBIDDEN_WORDS)) + r")\b", re.IGNORECASE)
    return bool(pattern.search(message_text))

def parse_duration(duration_str: str) -> int:
    match = re.match(r"(\d+)([smhd])", duration_str.strip().lower())
    if match:
        amount = int(match.group(1))
        unit = match.group(2)

        if unit == "s":
            return amount
        elif unit == "m":
            return amount * 60
        elif unit == "h":
            return amount * 3600
        elif unit == "d":
            return amount * 86400
    return None

async def check_messages(message: Message):
    if message.chat.type != "supergroup":
        return

    if message.text and contains_forbidden_words(message.text):
        try:
            await message.chat.ban(user_id=message.from_user.id)
            await message.reply(f"Пользователь {message.from_user.mention} заблокирован за использование запрещенных слов.")
        except Exception as e:
            await message.reply(f"Не удалось заблокировать пользователя: {e}")

async def ban_user(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    try:
        duration_str = message.get_args()
        if not duration_str:
            await message.reply("Пожалуйста, укажите длительность бана (например, 1h, 1d).")
            return

        duration_seconds = parse_duration(duration_str)
        if duration_seconds is None:
            await message.reply("Неверный формат длительности. Используйте, например, 1h, 1d.")
            return

        until_date = timedelta(seconds=duration_seconds)

        user = message.reply_to_message.from_user
        await message.chat.ban(user_id=user.id, until_date=until_date)
        await message.reply(
            f"Пользователь {user.mention} заблокирован {'на ' + str(duration_seconds // 60) + ' минут' if duration_seconds < 86400 else 'на ' + str(duration_seconds // 86400) + ' день'}."
        )
    except Exception as e:
        await message.reply(f"Не удалось заблокировать пользователя: {e}")

def register_handlers(dp: Dispatcher):
    dp.message.register(check_messages, F.text)
    dp.message.register(ban_user, F.text.startswith("/ban"))
