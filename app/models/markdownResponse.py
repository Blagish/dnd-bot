from pydantic import BaseModel
from typing import List
from uuid import UUID

class MarkdownResponse(BaseModel):
    text: str
    pictures: List[UUID] | None