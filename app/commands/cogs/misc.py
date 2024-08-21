from random import choice, randint

from discord import Embed, Colour, ButtonStyle, File
from app.commands.base import BaseCog
from discord.ext import commands
import loguru

logger = loguru.logger


class Cards(BaseCog, name="Разное: игральные карты"):
    def __init__(self, bot):
        super().__init__(bot)
        self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.suits = ["D", "H", "S", "C"]
        self.jokers = ["Joker1", "Joker2"]

        self.full_cards = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
        self.full_suits = {
            "D": "Diamonds",
            "H": "Hearts",
            "S": "Spades",
            "C": "Clubs",
            "Joker1": "Joker (Black)",
            "Joker2": "Joker (Red)",
        }
        self.colors = {
            "D": 0xDF0000,
            "H": 0xDF0000,
            "S": 0x000000,
            "C": 0x000000,
            "Joker1": 0x000000,
            "Joker2": 0xDF0000,
        }

    @staticmethod
    def gen_embed_picture(title, name, color):
        filename = name + ".png"
        e = Embed(title=title, colour=color)
        path = "app/commands/cards/"
        file = File(f"{path}{filename}", filename=filename)
        e.set_image(url=f"attachment://{filename}")
        return file, e

    @commands.hybrid_command(name="card52", aliases=["52", "карт52", "к52", "k52", "c52"])
    async def card52(self, ctx):
        """Случайная карта из стандартной колоды в 52 карты."""
        card, suit = choice(self.cards), choice(self.suits)
        name = f"{card}{suit}"
        color = self.colors[suit]
        title = f"{self.full_cards.get(card, card)} of {self.full_suits[suit]}"
        file, embed = self.gen_embed_picture(title, name, color)
        await ctx.send(file=file, embed=embed)

    @commands.hybrid_command(name="card54", aliases=["54", "карт54", "к54", "k54", "c54"])
    async def card54(self, ctx):
        """Случайная карта из стандартной колоды в 52 карты + 2 джокера."""
        if randint(1, 54) < 3:  # Jokers:
            name = choice(self.jokers)
            color = self.colors[name]
            title = self.full_suits[name]
        else:
            card, suit = choice(self.cards), choice(self.suits)
            name = f"{card}{suit}"
            color = self.colors[suit]
            title = f"{self.full_cards.get(card, card)} of {self.full_suits[suit]}"
        file, embed = self.gen_embed_picture(title, name, color)
        await ctx.send(file=file, embed=embed)
