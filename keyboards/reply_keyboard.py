from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data.loader import FAQItem
from typing import List
from data import BACK_BUTTON_TEXT


def create_reply_keyboard(
    items: List[FAQItem], is_submenu: bool = False
) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for item in items:
        builder.button(text=item.question)

    # Если это подменю, добавляем кнопку "Назад"
    if is_submenu:
        builder.button(text=BACK_BUTTON_TEXT)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
