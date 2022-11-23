from .dice import Dice
# from .macros import Macros
from .talking import Talking
from .technical import Technical
from .misc import Cards

cogs = (Dice, Talking, Technical, Cards)


async def setup(bot):
    for cog in cogs:
        try:
            print(f'loading command extension {cog.__name__}...')
            await bot.add_cog(cog(bot))
        except Exception as e:
            print(f'error loading {cog.__name__}: {e}')
    print('command extensions loading finished :)')
