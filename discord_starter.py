import discord
import os
from random import randint, choice
import server


client = discord.Client()

danika_react = ['а?', 'Я тут!', 'Меня звали?', 'Что-то нужно?']
yeno = ['Ага', 'Неа']

discord_id = os.environ.get('DISCORD_ID')

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
    elif discord_id in text:
        await message.channel.send(choice(danika_react+[':eyes: '*randint(1, 3)]))
    elif 'даник' in text.lower():
        if '?' in text:
            await message.channel.send(choice(yeno))
        elif randint(1, 10) == 10:
            await message.channel.send(choice(danika_react))

client.run(os.environ.get('DISCORD_TOKEN'))
