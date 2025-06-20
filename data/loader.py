from pydantic import BaseModel, field_validator
import json
from typing import List, Literal, Optional, Union
import os

FaqType = Literal["text", "document", "submenu"]


class FAQItem(BaseModel):
    id: str
    question: str
    answer: Union[str, List["FAQItem"]]
    faq_type: FaqType
    file_paths: Optional[List[str]] = None

    @field_validator("file_paths", mode="after")
    @classmethod
    def validate_file_paths(cls, value, info):
        if info.data.get("faq_type") == "document":
            if not value:
                raise ValueError("file_paths is required for document type FAQ")
            for path in value:
                if not os.path.exists(path):
                    raise ValueError(f"File path does not exist: {path}")
        elif info.data.get("faq_type") != "document" and value:
            raise ValueError(
                "file_paths should not be provided for non-document type FAQ"
            )
        return value

    @field_validator("answer", mode="after")
    @classmethod
    def validate_answer(cls, value, info):
        if info.data.get("faq_type") == "submenu":
            if not isinstance(value, list):
                raise ValueError("answer must be a list for submenu type FAQ")
        elif info.data.get("faq_type") in ["text", "document"]:
            if not isinstance(value, str):
                raise ValueError("answer must be a string for text/document type FAQ")
        return value


FAQItem.model_rebuild()


def load_faq_data(file_path: str) -> List[FAQItem]:
    with open(file_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    return [FAQItem(**item) for item in faq_data] if isinstance(faq_data, list) else []
