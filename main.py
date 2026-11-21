import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(name)s | %(level)s | %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"

)

logger = logging.getLogger(__name__)

dp = Dispatcher()


async def main():
    load_dotenv()
    bot = Bot(os.getenv("BOT_TOKEN"))
    await bot.delete_webhook(drop_pending_updates = True) 
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")