from pydantic import BaseModel, ConfigDict
from discord import Embed, File
from typing import List

class Pf2Response(BaseModel):
    message: str = ''
    embed: Embed
    other_embeds: List[Embed] | None = None
    choices: List[dict] | None = None
    file: File | None = None

    class Config:
        arbitrary_types_allowed = True