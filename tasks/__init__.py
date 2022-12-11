from .gaming import Gaming
import logging

logger = logging.getLogger(__name__)
cogs = (Gaming,)


async def setup(bot):
    for cog in cogs:
        try:
            logger.info(f'loading task extension {cog.__name__}...')
            await bot.add_cog(cog(bot))
        except Exception as e:
            logger.error(f'error loading {cog.__name__}: {e}')
    logger.info('task extensions loading finished :)')