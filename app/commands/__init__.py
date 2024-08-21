from app.commands.cogs import Dice, Talking, Technical, Cards, Game, Systems
import loguru

cogs = (Dice, Talking, Technical, Cards, Game, Systems)
logger = loguru.logger


async def setup(bot):
    for cog in cogs:
        try:
            logger.info(f"loading command extension {cog.__name__}...")
            await bot.add_cog(cog(bot))
        except Exception as e:
            logger.error(f"error loading {cog.__name__}: {e}")
    logger.info("command extensions loading finished :)")
