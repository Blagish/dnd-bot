import os
import discord
from discord.ext import commands
from bot_config import command_prefix
from help import MyHelpCommand

bot = commands.Bot(command_prefix=command_prefix,
                   activity=discord.Activity(type=discord.ActivityType.listening,
                                             name=f'{command_prefix}help'))
bot.load_extension('commands')
bot.load_extension('tasks')

bot.help_command = MyHelpCommand(sort_commands=False,
                                 commands_heading='(команды):',
                                 aliases_heading='Варианты:',
                                 no_category='Просто')
bot.run(os.environ.get('DISCORD_TOKEN'))
