from discord.ext import commands


class Technical(commands.Cog, name='Важное'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message_edit')
    async def process_command_on_edit(self, message):
        if message.author == self.bot.user:
            return None
        await self.bot.process_command(message)

    @commands.command(name='хелп', aliases=['помощь'], hidden=True)
    async def help_rus(self, ctx, *arg):
        if arg:
            arg = ' '.join(arg)
            await ctx.send_help(arg)
        else:
            await ctx.send_help()
