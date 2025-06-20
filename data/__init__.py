from .loader import load_faq_data, FAQItem
from typing import List, Dict, Set

FAQItem.model_rebuild()


BACK_BUTTON_TEXT = "Назад"

FAQ_DATA: List[FAQItem] = []
FAQ_BY_ID: Dict[str, FAQItem] = {}
FAQ_BY_QUESTION: Dict[str, FAQItem] = {}
ALL_QUESTIONS: Set[str] = set()


# Рекурсивная функция для "выравнивания" данных
def _flatten_faq_data(items: List[FAQItem]):
    """
    Рекурсивно обходит все элементы FAQ, включая вложенные,
    и заполняет словари FAQ_BY_ID и FAQ_BY_QUESTION.
    """
    for item in items:
        # Проверка на дубликаты ID и вопросов, чтобы избежать конфликтов
        if item.id in FAQ_BY_ID:
            raise ValueError(f"Ошибка в faq.json: Найден дублирующийся ID '{item.id}'")
        if item.question in FAQ_BY_QUESTION:
            raise ValueError(
                f"Ошибка в faq.json: Найден дублирующийся вопрос (question) '{item.question}'"
            )

        # Добавляем элемент в словари
        FAQ_BY_ID[item.id] = item
        FAQ_BY_QUESTION[item.question] = item

        # Если элемент является подменю, рекурсивно вызываем эту же функцию для его дочерних элементов
        if item.faq_type == "submenu" and isinstance(item.answer, list):
            _flatten_faq_data(item.answer)


try:
    # 1. Загружаем данные верхнего уровня
    FAQ_DATA = load_faq_data("data/faq.json")

    # 2. "Выравниваем" данные, заполняя словари всеми элементами, включая вложенные
    _flatten_faq_data(FAQ_DATA)

    # 3. Создаем множество всех вопросов для использования в фильтрах aiogram
    # Добавляем также текст кнопки "Назад", чтобы фильтры его тоже ловили
    ALL_QUESTIONS = set(FAQ_BY_QUESTION.keys())
    ALL_QUESTIONS.add(BACK_BUTTON_TEXT)

except Exception as e:
    # Лучше логировать ошибку, чтобы понимать, что пошло не так
    print(f"Критическая ошибка при загрузке FAQ данных: {e}")
    # Оставляем структуры пустыми, чтобы бот не упал при запуске,
    # но в логах будет видно проблему.
    FAQ_DATA = []
    FAQ_BY_ID = {}
    FAQ_BY_QUESTION = {}
    ALL_QUESTIONS = set()
