from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import types
from buttons import actions, exit_state_button, create_calendar
from aiogram.fsm.context import FSMContext
from state import Form
import datetime


async def say_hello(message: types.Message, session: AsyncSession):
    await message.answer(text="{}".format(message.chat.id), reply_markup=actions())


async def get_fio(message: types.Message, state: FSMContext):
    await state.set_state(Form.initials)
    await message.answer("Введите контактные данные", reply_markup=exit_state_button())


async def fill_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Form.enrollment_date)
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await message.answer(text=message.text, reply_markup=create_calendar(current_year, current_month, "first"))
