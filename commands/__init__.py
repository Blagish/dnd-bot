from .dice import Dice
# from .macros import Macros
from .talking import Talking
from .technical import Technical
from .misc import Cards
import logging

logger = logging.getLogger(__name__)
cogs = (Dice, Talking, Technical, Cards)


async def setup(bot):
    for cog in cogs:
        try:
            logger.info(f'loading command extension {cog.__name__}...')
            await bot.add_cog(cog(bot))
        except Exception as e:
            logger.error(f'error loading {cog.__name__}: {e}')
    logger.info('command extensions loading finished :)')
