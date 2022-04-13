from discord.ext import commands
import discord
import os
from random import randint, choice
from bot_config import command_prefix


danika_react = ['а?', 'Я тут!', 'Меня звали?', 'Что-то нужно?']
yeno = ['Ага', 'Неа']

discord_id = os.environ.get('DISCORD_ID')

bot = commands.Bot(command_prefix=command_prefix)
bot.load_extension('commands')


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)


bot.help_command = MyHelpCommand()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return None
    text = message.content
    print(text)
    if discord_id in text:
        await message.channel.send(choice(danika_react+[':eyes: '*randint(1, 3)]))
    elif 'даник' in text.lower():
        if '?' in text:
            await message.channel.send(choice(yeno))
        elif randint(1, 8) == 1:
            await message.channel.send(choice(danika_react))
    await bot.process_commands(message)  # maybe make a real listener later and remove this

bot.run(os.environ.get('DISCORD_TOKEN'))
