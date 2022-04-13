from discord.ext import commands, tasks
import discord
from random import choice


class Gaming(commands.Cog, name='Гейминг'):
    def __init__(self, bot):
        self.bot = bot
        self.game = None
        self.games = ('D&D 5e', 'Pathfinder 2e', 'Fate', 'City of Mist', 'Prowlers & Paragons', 'Minecraft')
        await self.start_new_game.start()

    def cog_unload(self):
        await self.start_new_game.cancel()

    @tasks.loop(hours=8)
    async def start_new_game(self):
        game_title = self.choose_a_game()
        self.game = discord.Game(name=game_title)
        print(f'Starting playing {game_title}')
        await self.bot.change_presence(activity=self.game)

    def choose_a_game(self):
        return choice(self.games)

