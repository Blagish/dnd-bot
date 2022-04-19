from .dice import Dice
from .macros import Macros
from .talking import Talking
from .technical import Technical

cogs = (Dice, Talking, Macros, Technical)


def setup(bot):
    for cog in cogs:
        try:
            print(f'loading command extension {cog.__name__}...')
            bot.add_cog(cog(bot))
        except Exception as e:
            print(f'error loading {cog.__name__}: {e}')
    print('command extensions loading finished :)')
