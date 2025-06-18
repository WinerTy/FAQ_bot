from .loader import load_faq_data

try:
    FAQ_DATA = load_faq_data("data/faq.json")
    FAQ_BY_ID = {item.id: item for item in FAQ_DATA}
    FAQ_BY_QUESTION = {item.question: item for item in FAQ_DATA}
    ALL_QUESTIONS = set(FAQ_BY_QUESTION.keys())
except Exception:
    FAQ_BY_ID = dict()
    FAQ_BY_QUESTION - dict()
    ALL_QUESTIONS = set()
