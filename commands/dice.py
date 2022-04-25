from random import randint

import discord
from discord import Embed, Colour
from discord.ext import commands
from parser import d2
from game_data import get_spell_dnd_su, get_info_pf2
from util import ctx_send


class Dice(commands.Cog, name='Кубы кубы'):
    def __init__(self, bot):
        self.bot = bot
        self.fate_die = ('[-]', '[ ]', '[+]')

    @staticmethod
    def error_message(error):
        return Embed(title="Произошла непредвиденная ошибка :(",
                    description=f'**Код ошибки:** {error}.\nЧто бы это ни было, возможно, когда-нибудь это пофиксится.', 
                    colour=Colour.red())

    @commands.command(name='куб', aliases=['r', 'р', 'k', 'к', 'roll', 'ролл'])
    async def roll(self, ctx, *, string):
        """Кидаю кубы, прибавляю модификаторы~ Можно использовать сложение, вычитание, умножение, деление. Кубы с преимуществом - ad, с помехой - dd. Можно использовать скобки, короче, реально охуенный парсер, два года его писала """
        sol, ans = d2(string)
        s = f'Кидаю\n-> {sol}\n= **{ans}**'
        await ctx_send(ctx, s)

    @roll.before_invoke
    async def before_roll(self, ctx):
        name = 'their DMs'
        if hasattr(ctx.channel, 'name'):
            name = ctx.channel.name
        print(f'Roll! {ctx.author.name}: {ctx.message.content} at {name}')

    @roll.after_invoke
    async def after_roll(self, ctx):
        pass

    @commands.command(name='днд', aliases=['закл', 'спелл', 'dnd5', 'spell', 'dnd', 'днд5'])
    async def spell_dnd5(self, ctx, *, spell_name):
        """Узнать о заклинании из D&D 5e. Как на русском, так и на английском."""
        async with ctx.typing():
            try:
                message = get_spell_dnd_su(spell_name)
            except Exception as e:
                message = self.error_message(e)
        await ctx.send(embed=message)

    @commands.command(name='пф', aliases=['pf', 'пф2', 'pf2'])
    async def info_pf2(self, ctx, *, thing_name):
        """Узнать о любой вещи из Pathfinder 2e. На английском."""
        async with ctx.typing():
            try:
                message = get_info_pf2(thing_name)
            except Exception as e:
                message = self.error_message(e)
        await ctx.send(embed=message)

    @commands.command(name='фейт', aliases=['f', 'ф', 'fate'])
    async def fate(self, ctx, *mod):
        """Бросок четырех кубов системы Fate. Модификатор указывается по типу +3 или -1. Пустой аргумент равнозначен +0. """
        mod = ''.join(mod).replace(' ', '')
        if mod == '':
            mod = '+0'
        if (sign := mod[0]) not in ('+', '-'):
            return 'Ошибка: модификатор не найден'
        mod = int(mod[1:])
        if sign == '-':
            mod = -mod
        s = 'Кидаю\n-> **'
        res = 0
        for i in range(4):
            d = randint(-1, 1)
            s += self.fate_die[d + 1]
            res += d
        s += f'** {sign} {abs(mod)}\n= **{res + mod}**'
        await ctx.send(s)

