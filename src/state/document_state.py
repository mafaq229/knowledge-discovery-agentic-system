from typing import Optional, Any
from enum import Enum
from pydantic import BaseModel, computed_field, Field

# str is used to ensure that the enum values are serialized as strings in JSON (str mixing)
class DocumentType(str, Enum):
    TEXT = "text"
    PDF = "pdf"
    WEB = "web"

class Document(BaseModel):
    id: str
    source: str
    content: str
    doc_type: DocumentType
    metadata: dict[str, Any] = Field(default_factory=dict)

    @computed_field
    def length(self) -> int:
        return len(self.content)
    