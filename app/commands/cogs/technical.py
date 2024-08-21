from discord.ext import commands
from app.commands.base import BaseCog


class Technical(BaseCog, name="Важное"):
    @commands.Cog.listener("on_message_edit")
    async def process_command_on_edit(self, before, after):
        if before.author == self.bot.user:
            return None
        await self.bot.process_commands(after)

    @commands.command(name="хелп", aliases=["помощь"], hidden=True)
    async def help_rus(self, ctx, *arg):
        if arg:
            arg = " ".join(arg)
            await ctx.send_help(arg)
        else:
            await ctx.send_help()
