import asyncio
import logging

from config import bot, dp, database
from handlers.other_message import echo_router
from handlers.picture import picture_router
from handlers.start import start_router
from handlers.dialoq import opros_router
from handlers.review import review_router

async def on_startup(bot):
    database.crate_tables()
    



async def main():
    dp.include_router(start_router)
    dp.include_router(picture_router)
    dp.include_router(opros_router)
    dp.include_router(review_router)
    dp.include_router(echo_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
