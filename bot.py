from asgiref.sync import sync_to_async
from dotenv import load_dotenv
from os import environ
import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import F
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.declarative import declarative_base
from middleware import DbSessionMiddleware
from handlers import say_hello, get_fio, fill_fio
from callback import exit_callback
from db import Client, Order, Base
from state import Form
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import django
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'self_storage'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()
from storage.models import Cell, CellTariff, Client, Order, Warehouse

@sync_to_async
def test():
    return Client.objects.filter(tg_id="558086562").first().client_name
async def send_message(bot: Bot):

    await bot.send_message(chat_id="247176848", text=await test())


async def init_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    load_dotenv()
    engine = create_async_engine(url=environ['DATABASE_URL'], echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    await init_db(engine)
    bot_token = environ['BOT_TOKEN']
    bot = Bot(token=bot_token, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.message.register(say_hello, CommandStart())
    dp.callback_query.register(exit_callback, F.data == "exit")
    dp.message.register(get_fio, F.text == "Создать заказ")
    dp.message.register(fill_fio, F.text, Form.initials)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, "interval", minutes=1, args=[bot])
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
