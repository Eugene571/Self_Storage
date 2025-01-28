from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
import sys

API_TOKEN = '7973097193:AAF-ySmei8yHRClvJ5irOCMX0hweLvgMUCk'


async def send_message(bot: Bot):
    await bot.send_message(chat_id="247176848", text="hello")


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, "interval", minutes=1, args=[bot])
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
