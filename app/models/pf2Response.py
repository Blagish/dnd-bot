from pydantic import BaseModel, ConfigDict
from discord import Embed
from typing import List

class Pf2Response(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    message: str = ''
    embed: Embed
    other_embeds: List[Embed] | None = None