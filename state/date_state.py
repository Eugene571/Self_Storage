from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    initials = State()
    enrollment_date = State()
    graduation_date = State()
