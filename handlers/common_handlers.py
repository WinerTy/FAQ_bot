from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_keyboard import create_reply_keyboard
from data import FAQ_DATA
from state.menu import MenuState

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    text = "Привет! 👋\n\nЯ бот-помощник. Выбери вопрос из меню ниже, чтобы получить на него ответ."
    keyboard = create_reply_keyboard(FAQ_DATA)
    await message.answer(text=text, reply_markup=keyboard)
    await state.set_state(MenuState.in_main_menu)
