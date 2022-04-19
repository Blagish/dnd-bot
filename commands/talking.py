from discord.ext import commands
from random import choice, randint
import os


class Talking(commands.Cog, name='Общение со мной :)'):
    def __init__(self, bot):
        self.bot = bot
        self.danika_react = ['а?', 'Я тут!', 'Меня звали?', 'Что-то нужно?', 'Чем могу быть полезна?']
        self.bot_id = os.environ.get('DISCORD_ID')
        self.yes_or_no = ['Ага', 'Неа']
        self.funny_words = ['пизда :)', 'пизда', 'пизда!', 'сковорода']
    
    @commands.Cog.listener('on_message')
    async def respond_to_her_name(self, message):
        if message.author == self.bot.user:
            return None
        ctx = message.channel
        print(message.content)
        text = message.content.lower()
        if self.bot_id in text:
            ctx.send(choice(self.danika_react))
        elif 'даник' in text:
            if '?' in text:
                ctx.send(self.funny_response(text))
            elif randint(1, 7) == 1:
                ctx.send(choice(self.danika_react))

    def funny_response(self, text):
        if text.replace(' ', '')[-3:] == 'да?':
            return choice(self.funny_words)
        elif text[:2] == 'да' and text.replace(' ', '')[-7:] == 'даника?':
            return choice(self.funny_words).replace('да', 'даника')
        else:
            return choice(self.yes_or_no)

    @commands.command(name='привет', aliases=['hello', 'hewwo', 'owo'])
    async def hello(self, ctx):
        """Привет :)"""
        res = choice(['Привет!', 'Привет :)', 'Hewwo', ' Hewwo :)', 'Привееееет :)'])
        await ctx.send(res)

    @commands.command(name='куку', hidden=True)
    async def kuku(self, ctx):
        """Ку ку?"""
        await ctx.send('быбы')

    @commands.command(name='спасибо', aliases=['спс', 'thanks', 'thx'])
    async def thanks(self, ctx):
        """Поблагодарить меня :)"""
        res = choice(['Пожалуйста!', 'Рада помочь!', 'Всегда пожалуйста', 'Стараюсь :)'])
        await ctx.send(res)

    @commands.command(name='слышь', aliases=['слыш', 'э', 'слiш', 'bruh', 'брух'])
    async def anger(self, ctx):
        """Быкануть на меня :("""
        res = choice(['Виноваты кубики', 'Оно само', 'Это не я', 'Я честно не виновата', 'Все вопросы к кубам!'])
        await ctx.send(res)
