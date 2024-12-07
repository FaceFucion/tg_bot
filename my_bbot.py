import asyncio
import logging

from moi_config import bot, dp
from handlers.other_message import echo_router
from handlers.picture import picture_router
from handlers.na4alo import start_router


async def main():
    dp.include_router(start_router)
    dp.include_router(picture_router)

    dp.include_router(echo_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())