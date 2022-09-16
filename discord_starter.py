import os
import asyncio
import discord
from discord.ext import commands
from bot_config import command_prefix
from help import MyHelpCommand

intents = discord.Intents(guilds=True, members=True, messages=True, reactions=True, message_content=True)
bot = commands.Bot(intents=intents, command_prefix=command_prefix,
                   activity=discord.Activity(type=discord.ActivityType.listening,
                                             name=f'{command_prefix}help'))

bot.help_command = MyHelpCommand(sort_commands=False,
                                 commands_heading='(команды):',
                                 aliases_heading='Варианты:',
                                 no_category='Просто')


async def main():
    async with bot:
        await bot.load_extension('commands')
        await bot.load_extension('tasks')

        await bot.start(os.environ.get('DISCORD_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())

