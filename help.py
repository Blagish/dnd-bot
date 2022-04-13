from discord.ext import commands
import discord


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

    def get_opening_note(self):
        command_name = self.invoked_with
        return "Используйте `{0}{1} [command]` для получения информации по команде.\n" \
               "Можно также делать `{0}{1} [category]` для информации по категории.".format(self.clean_prefix, command_name)
