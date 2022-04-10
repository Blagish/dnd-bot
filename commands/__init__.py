from .dice import Dice
from .macros import Macros
from .talking import Talking

cogs = (Dice, Talking, Macros)


def setup(bot):
    for cog in cogs:
        try:
            print(f'loading {cog.__name__}...')
            bot.add_cog(cog(bot))
        except Exception as e:
            print(f'error loading {cog.__name__}: {e}')
    print('extensions loading finished :)')
