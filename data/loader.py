from pydantic import BaseModel, field_validator
import json
from typing import List, Literal, Optional
import os


class FAQItem(BaseModel):
    id: str
    question: str
    answer: str
    faq_type: Literal["text", "document"]
    file_paths: Optional[List[str]] = None

    @field_validator("file_paths", mode="after")
    @classmethod
    def validate_file_paths(cls, value, info):
        if info.data.get("faq_type") == "document":
            if not value:
                raise ValueError("file_path is required for document type FAQ")
            for path in value:
                if not os.path.exists(path):
                    raise ValueError(f"File does not exist: {path}")
        if info.data.get("faq_type") == "text" and value:
            raise ValueError("file_path should not be provided for text type FAQ")
        return value


def load_faq_data(file_path: str) -> List[FAQItem]:
    with open(file_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    return [FAQItem(**item) for item in faq_data] if isinstance(faq_data, list) else []
