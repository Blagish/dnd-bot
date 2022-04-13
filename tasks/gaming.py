from discord.ext import commands, tasks
from discord import Game
from random import choice


class Gaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = ('D&D 5e', 'Pathfinder 2e', 'Fate', 'City of Mist', 'Prowlers & Paragons', 'Minecraft')
        self.game = None

    @tasks.loop(hours=8)
    async def start_new_game(self):
        game_title = self.choose_a_game()
        self.game = Game(game_title)
        print(f'Starting playing {game_title}')
        await self.bot.change_presence(activity=self.game)

    def choose_a_game(self):
        return choice(self.games)
