import discord
from discord.ext import commands
import os
from random import randint, choice
from bot_config import command_prefix
from help import MyHelpCommand

danika_react = ['а?', 'Я тут!', 'Меня звали?', 'Что-то нужно?']
yeno = ['Ага', 'Неа']

discord_id = os.environ.get('DISCORD_ID')

bot = commands.Bot(command_prefix=command_prefix,
                   activity=discord.Activity(type=discord.ActivityType.listening, name='/help'))
bot.load_extension('commands')
bot.load_extension('tasks')

bot.help_command = MyHelpCommand(sort_commands=False, commands_heading='(команды):',
                                 aliases_heading='Варианты:', no_category='Просто')


@bot.command(name='хелп', aliases=['помощь'], hidden=True)
async def help_rus(ctx, *arg):
    if arg:
        arg = ' '.join(arg)
        await ctx.send_help(arg)
    else:
        await ctx.send_help()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return None
    text = message.content
    print(text)
    if discord_id in text:
        await message.channel.send(choice(danika_react + [':eyes: ' * randint(1, 3)]))
    elif 'даник' in text.lower():
        if '?' in text:
            await message.channel.send(choice(yeno))
        elif randint(1, 8) == 1:
            await message.channel.send(choice(danika_react))
    await bot.process_commands(message)  # maybe make a real listener later and remove this


bot.run(os.environ.get('DISCORD_TOKEN'))
