from discord.ext import commands
import os
from random import randint, choice
from bot_config import command_prefix
from commands import BasicCommands, FunctionCommands, MacrosCommands, RandomCommands

danika_react = ['а?', 'Я тут!', 'Меня звали?', 'Что-то нужно?']
yeno = ['Ага', 'Неа']

discord_id = os.environ.get('DISCORD_ID')

bot = commands.Bot(command_prefix)

bot.add_cog(BasicCommands(bot))
bot.add_cog(FunctionCommands(bot))
bot.add_cog(MacrosCommands(bot))
bot.add_cog(RandomCommands(bot))


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

bot.run(os.environ.get('DISCORD_TOKEN'))
