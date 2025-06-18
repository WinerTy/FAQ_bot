from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.reply_keyboard import create_main_menu_keyboard
from aiogram.types import ReplyKeyboardRemove

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    text = "Привет! 👋\n\nЯ бот-помощник. Выбери вопрос из меню ниже, чтобы получить на него ответ."
    keyboard = create_main_menu_keyboard()
    await message.answer(text=text, reply_markup=keyboard)


@router.message(lambda message: message.text == "Скрыть меню")
async def hide_menu(message: Message):
    await message.answer(
        text="Меню скрыто. Чтобы открыть его снова, введите /start",
        reply_markup=ReplyKeyboardRemove(),  # Убираем клавиатуру
    )
