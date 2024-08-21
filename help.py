from discord.ext import commands
import discord


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description="")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

    def get_opening_note(self):
        command_name = self.invoked_with
        return (
            f"Используйте `{self.context.clean_prefix}{command_name} [command]` для получения информации по команде.\n"
            f"Можно также делать `{self.context.clean_prefix}{command_name} [category]` для получения информации по категории."
        )
