from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaDocument
from data import ALL_QUESTIONS, FAQ_BY_QUESTION
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.reply_keyboard import create_reply_keyboard
from data import FAQ_DATA, BACK_BUTTON_TEXT
from state.menu import MenuState

router = Router()


@router.message(
    StateFilter(MenuState.in_main_menu, MenuState.in_submenu), F.text.in_(ALL_QUESTIONS)
)
async def process_any_menu_press(message: Message, state: FSMContext):
    # Если нажата кнопка "Назад"
    if message.text == BACK_BUTTON_TEXT:
        text = "Вы вернулись в главное меню."
        keyboard = create_reply_keyboard(FAQ_DATA)
        await message.answer(text, reply_markup=keyboard)
        await state.set_state(MenuState.in_main_menu)
        return

    # Ищем нажатую кнопку в нашем "плоском" словаре
    item = FAQ_BY_QUESTION.get(message.text)
    if not item:
        await message.answer("Неизвестная команда. Пожалуйста, используйте кнопки.")
        return

    if item.faq_type == "text":
        await message.answer(item.answer, parse_mode="HTML")

    elif item.faq_type == "document":
        if item.answer:
            await message.answer(item.answer, parse_mode="HTML")
        if len(item.file_paths) == 1:
            await message.answer_document(FSInputFile(item.file_paths[0]))
        else:
            media = [
                InputMediaDocument(media=FSInputFile(path)) for path in item.file_paths
            ]
            await message.answer_media_group(media=media)

    elif item.faq_type == "submenu":
        keyboard = create_reply_keyboard(item.answer, is_submenu=True)
        await message.answer(
            f"Вы выбрали раздел: *{item.question}*",
            reply_markup=keyboard,
            parse_mode="MarkdownV2",
        )
        await state.set_state(MenuState.in_submenu)
