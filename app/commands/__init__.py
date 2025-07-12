from app.commands.cogs import AiTalking, Dice, Talking, Technical, Cards, Game, Systems
from app.util.config import config
import loguru

logger = loguru.logger

async def load_cog(cog, bot):
    try:
        logger.info(f"loading command extension {cog.__name__}...")
        await bot.add_cog(cog(bot))
    except Exception as e:
        logger.error(f"error loading {cog.__name__}: {e}")


async def setup(bot):
    await load_cog(Dice, bot)
    await load_cog(Talking, bot)
    await load_cog(Technical, bot)
    await load_cog(Cards, bot)
    await load_cog(Game, bot)
    await load_cog(Systems, bot)

    if config.use_ai_talking:
        await load_cog(AiTalking, bot)
    logger.info("command extensions loading finished :)")
