from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
def get_inline(
        ss: dict[str, str],
        sizes: tuple = (2,)):
    keyboard = InlineKeyboardBuilder()
    for text, data in ss.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()
