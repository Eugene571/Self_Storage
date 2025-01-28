from aiogram import types


def actions():
    keyboard_buttons = [
        [types.KeyboardButton(text="Создать заказ")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons)


def exit_state_button():
    keyboard_buttons = [
        [types.InlineKeyboardButton(text="Отмена", callback_data="exit")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def exit_and_back_to_init_buttons():
    keyboard_buttons = [
        [types.InlineKeyboardButton(text="Отмена", callback_data="exit")],
        [types.InlineKeyboardButton(text="Назад", callback_data="back_init")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def exit_and_back_to_startdate_buttons():
    keyboard_buttons = [
        [types.InlineKeyboardButton(text="Отмена", callback_data="exit")],
        [types.InlineKeyboardButton(text="Назад", callback_data="back_init")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
