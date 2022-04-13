from discord.ext import commands
from random import choice


class Talking(commands.Cog, name='Общение со мной :)'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='привет', aliases=['hello', 'hewwo', 'owo'])
    async def hello(self, ctx):
        """привет :)"""
        res = choice(['Привет!', 'Привет :)', 'Hewwo', ' Hewwo :)', 'Привееееет :)'])
        await ctx.send('hewwo OwO')

    @commands.command(name='куку', hidden=True)
    async def kuku(self, ctx):
        """ку ку?"""
        return ctx.send('быбы')

    @commands.command(name='спасибо', aliases=['спс', 'thanks', 'thx'])
    async def thanks(self, ctx):
        """поблагодарить меня :)"""
        res = choice(['Пожалуйста!', 'Рада помочь!', 'Всегда пожалуйста', 'Стараюсь :)'])
        await ctx.send(res)

    @commands.command(name='слышь', aliases=['слыш', 'э', 'слiш', 'bruh', 'брух'])
    async def anger(self, ctx):
        """быкануть на меня :("""
        res = choice(['Виноваты кубики', 'Оно само', 'Это не я', 'Я честно не виновата', 'Все вопросы к кубам!'])
        await ctx.send(res)
