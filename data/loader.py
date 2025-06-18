from pydantic import BaseModel, field_validator
import json
from typing import List, Literal, Optional
import os


class FAQItem(BaseModel):
    id: str
    question: str
    answer: str
    faq_type: Literal["text", "document"]
    file_path: Optional[str] = None

    @field_validator("file_path", mode="after")
    @classmethod
    def validate_file_path(cls, value: str, info):
        if info.data.get("faq_type") == "document":
            if not value:
                raise ValueError("file_path is required for document type FAQ")
            if not os.path.exists(value):
                raise ValueError(f"File not found: {value}")
        if info.data.get("faq_type") == "text" and value:
            raise ValueError("file_path should not be provided for text type FAQ")
        return value


def load_faq_data(file_path: str) -> List[FAQItem]:
    with open(file_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    return [FAQItem(**item) for item in faq_data] if isinstance(faq_data, list) else []
