from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', aliases=['привет', 'hewwo', 'owo'])
    async def hello(self, ctx):
        await ctx.send('hewwo OwO')

    @commands.command(name='куку', hidden=True)
    async def kuku(self, ctx):
        return ctx.send('быбы')
