from aiogram import Bot, Dispatcher, types
from datetime import datetime
import calendar


def create_calendar(year, month, type_callback):
    # keyboard = types.InlineKeyboardMarkup()
    keyboard_buttons = [[types.InlineKeyboardButton(
        text='<<', callback_data=f'prev_month_{year}_{month}'),
        types.InlineKeyboardButton(
            text=calendar.month_name[month], callback_data='ignore'),
        types.InlineKeyboardButton(
            text='>>', callback_data=f'next_month_{year}_{month}')],]

    month_days = calendar.monthcalendar(year, month)
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(
                    text=' ', callback_data='ignore'))
            else:
                row.append(types.InlineKeyboardButton(text=str(day),
                           callback_data=f'{type_callback}_day_{year}_{month}_{day}'))
        keyboard_buttons += [row]
    keyboard_buttons += [types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
