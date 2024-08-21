from discord.ext import commands, tasks
import discord
from random import choice
import logging

logger = logging.getLogger(__name__)


class Gaming(commands.Cog, name="Гейминг"):
    def __init__(self, bot):
        self.bot = bot
        with open("app/tasks/games.txt", "r", encoding="utf-8") as file:
            games = file.read().split("\n")
            self.games = list(filter(lambda x: x != "", games))
        self.start_new_game.start()

    def cog_unload(self):
        self.start_new_game.cancel()

    @tasks.loop(hours=6.0)
    async def start_new_game(self):
        game_title = self.choose_a_game()
        logger.info(f"Starting playing {game_title}")
        await self.bot.change_presence(activity=discord.Game(name=game_title))

    @start_new_game.before_loop
    async def before_start_new_game(self):
        await self.bot.wait_until_ready()

    def choose_a_game(self):
        return choice(self.games)
