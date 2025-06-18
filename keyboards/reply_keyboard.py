from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data import FAQ_DATA


def create_main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for item in FAQ_DATA:
        builder.button(text=item.question, callback_data=f"faq_{item.id}")

    builder.adjust(1)

    return builder.as_markup(
        resize_keyboard=True,
    )
