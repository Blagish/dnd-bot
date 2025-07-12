from pydantic import BaseModel
from discord.message import Message

class MessageData(BaseModel):
    role: str
    content: str

    @classmethod
    def from_message(cls, msg:Message):
        pass