from pydantic import BaseModel
from discord import Embed
from typing import List

class Pf2Response(BaseModel):
    message: str = ''
    embed: Embed
    other_embeds: List[Embed] | None = None
    choices: List[dict] | None = None

    class Config:
        arbitrary_types_allowed = True