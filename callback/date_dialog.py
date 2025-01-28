from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext

from datetime import datetime
import calendar
from state import Form


async def process_enrollment_date(callback_query: types.CallbackQuery, state: FSMContext):
    day, month, year = map(int, callback_query.data.split('_')[1:])
    async with state.proxy() as data:
        data['enrollment_date'] = f"{year}-{month:02d}-{day:02d}"
    await callback_query.answer('test')


async def exit_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await callback_query.answer("Вы отменили заполнение заявки")


async def switch_month(callback_query: types.CallbackQuery):
    action = callback.data.split("_")[1]
