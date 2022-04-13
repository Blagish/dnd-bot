from .basic_commands import BasicCommands
from .function_commands import FunctionCommands
from .macros_commands import MacrosCommands
from .random_commands import RandomCommands

cogs = (BasicCommands, FunctionCommands, MacrosCommands, RandomCommands)


async def setup(bot):
    for cog in cogs:
        try:
            print(f'loading {cog.__name__}...')
            bot.add_cog(cog(bot))
        except Exception as e:
            print(f'error loading {cog.__name__}: {e}')
    print('extensions loading finished :)')
