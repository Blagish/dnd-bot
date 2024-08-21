from discord.ext import commands
from discord import Embed, Colour
import loguru

logger = loguru.logger


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def error_message(error: str):
        logger.error(error)
        return Embed(
            title="Произошла непредвиденная ошибка :(",
            description=f"**Код ошибки:** {error}.\nПожалуйста, сообщите об этой проблеме разработчику: **@blagish**.",
            colour=Colour.red(),
        )

    @staticmethod
    def foreseen_error_message(error: str):
        logger.error(error)
        return Embed(title="Ошибка :(", description=error, colour=Colour.red())
