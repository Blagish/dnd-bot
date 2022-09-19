from random import choice, randint

from discord import Embed, Colour, ButtonStyle
from discord.ext import commands


class Cards(commands.Cog, name='Кубы кубы'):
    def __init__(self, bot):
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

    def gen_embed_picture(self, title, name, color):
        e = Embed(title=title, colour=color)
        e.set_image(url=f'cards/{name}.svg')
        return e

    @commands.command(name='card54', aliases=['54', 'карт54', 'к54', 'k54', 'c54'])
    async def card54(self, ctx):
        if randint(1, 54) < 3:  # Jokers:
            name = choice(self.jokers)
            color = self.colors[name]
            title = self.full_suits[name]
        else:
            card, suit = choice(self.cards), choice(self.suits)
            name = f"{card}{suit}"
            color = self.colors[suit]
            title = f"{self.full_cards.get(card, card)} of {self.full_suits[suit]}"
        ctx.send(embed=self.gen_embed_picture(title, name, color))
