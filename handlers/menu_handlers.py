from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaDocument
from data import ALL_QUESTIONS, FAQ_BY_QUESTION

router = Router()


@router.message(F.text.in_(ALL_QUESTIONS))
async def process_question_press(message: Message):
    answer_item = FAQ_BY_QUESTION.get(message.text)
    if answer_item:
        if answer_item.faq_type == "text":
            await message.answer(answer_item.answer, parse_mode="HTML")
        elif answer_item.faq_type == "document":
            print(answer_item.file_paths)
            if len(answer_item.file_paths) == 1:
                await message.answer_document(
                    FSInputFile(answer_item.file_paths[0]),
                    caption=answer_item.answer,
                    parse_mode="HTML",
                )
            else:
                media = []
                for i, file_path in enumerate(answer_item.file_paths):
                    media.append(
                        InputMediaDocument(
                            media=FSInputFile(file_path),
                            parse_mode="HTML",
                        )
                    )
                await message.answer_media_group(media=media)
                await message.answer(answer_item.answer, parse_mode="HTML")
    else:
        await message.answer("Извините, не могу найти ответ на этот вопрос.")
