from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from data import ALL_QUESTIONS, FAQ_BY_QUESTION

router = Router()


@router.message(F.text.in_(ALL_QUESTIONS))
async def process_question_press(message: Message):
    answer_item = FAQ_BY_QUESTION.get(message.text)
    if answer_item:
        if answer_item.faq_type == "text":
            await message.answer(answer_item.answer, parse_mode="HTML")
        elif answer_item.faq_type == "document":
            answer_file = FSInputFile(answer_item.file_path)
            await message.answer_document(
                answer_file, caption=answer_item.answer, parse_mode="HTML"
            )
    else:
        await message.answer("Извините, не могу найти ответ на этот вопрос.")
