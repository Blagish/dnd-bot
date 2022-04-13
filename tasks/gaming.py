from discord.ext import commands, tasks
import discord
from random import choice


class Gaming(commands.Cog, name='Гейминг'):
    def __init__(self, bot):
        self.bot = bot
        self.games = ('D&D 5e', 'Pathfinder 2e', 'Fate', 'City of Mist', 'Prowlers & Paragons', 'Minecraft')
        self.start_new_game.start()

    def cog_unload(self):
        self.start_new_game.cancel()

    @tasks.loop(hours=6.0)
    async def start_new_game(self):
        game_title = self.choose_a_game()
        await self.bot.change_presence(activity=discord.Game(name=game_title))
        print(f'Starting playing {game_title}')

    @start_new_game.before_loop
    async def before_start_new_game(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    def choose_a_game(self):
        return choice(self.games)

