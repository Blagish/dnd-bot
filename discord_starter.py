import discord
from config import token_discord
from random import randint, choice
import server


client = discord.Client()

danika_react = ['а?', 'Я тут!', 'Меня звали?', 'Что-то нужно?']
daniel_react = ['О, вы знакомы с моим братом', 'Хоть мы и близнецы, но я немного младше.',
                'Многие говорят, что мой брат похож на какого-то Страда... кто это?',
                'У Даниеля есть огромная коллекция ножей. Он любит их точить.', 'Не хочу показаться грубой, но давайте не будем о нем.']
yeno = ['Ага', 'Неа']


@client.event
async def on_message(message):
    if message.author == client.user:
        return None
    text = message.content
    print(text)
    if text[0] == '/':
        output = server.process(text)
        for msg in output:
            await message.channel.send(msg)
    elif '684755387408580623' in text:
        await message.channel.send(choice(danika_react+[':eyes: '*randint(1, 3)]))
    elif 'даник' in text.lower():
        if '?' in text:
            await message.channel.send(choice(yeno))
        elif randint(1, 10) == 10:
            await message.channel.send(choice(danika_react))
##    elif 'Даниел' in text or 'Даниэл' in text:
##        if randint(1, 10) == 10:
##            await message.channel.send(choice(daniel_react))
client.run(token_discord)
