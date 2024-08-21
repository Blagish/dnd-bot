from random import choice, randint

from discord import Embed, Colour, ButtonStyle, File
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)


class Cards(commands.Cog, name='Разное: игральные карты'):
    def __init__(self, bot):
        print(__file__)
        self.bot = bot
        self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.suits = ["D", "H", "S", "C"]
        self.jokers = ["Joker1", "Joker2"]

        self.full_cards = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
        self.full_suits = {"D": "Diamonds", "H": "Hearts", "S": "Spades", "C": "Clubs",
                           "Joker1": "Joker (Black)", "Joker2": "Joker (Red)"}
        self.colors = {"D": 0xdf0000, "H": 0xdf0000,
                       "S": 0x000000, "C": 0x000000,
                       "Joker1": 0x000000,
                       "Joker2": 0xdf0000}

    @staticmethod
    def gen_embed_picture(title, name, color):
        print(os.curdir)
        filename = name+'.png'
        e = Embed(title=title, colour=color)
        path = './commands/cards/'
        file = File(f"{path}{filename}", filename=filename)
        e.set_image(url=f"attachment://{filename}")
        return file, e

    @commands.command(name='card52', aliases=['52', 'карт52', 'к52', 'k52', 'c52'])
    async def card52(self, ctx):
        """Случайным образом вытягивает одну карту из стандартной колоды в 52 карты."""
        card, suit = choice(self.cards), choice(self.suits)
        name = f"{card}{suit}"
        color = self.colors[suit]
        title = f"{self.full_cards.get(card, card)} of {self.full_suits[suit]}"
        file, embed = self.gen_embed_picture(title, name, color)
        await ctx.send(file=file, embed=embed)

    @commands.command(name='card54', aliases=['54', 'карт54', 'к54', 'k54', 'c54'])
    async def card54(self, ctx):
        """Случайным образом вытягивает одну карту из стандартной колоды в 52 карты + 2 джокера."""
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
