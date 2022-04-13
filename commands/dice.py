from random import randint
from discord.ext import commands
from parser import d2
from game_data import get_spell_dnd_su, get_info_pf2


class Dice(commands.Cog, name='Кубы кубы'):
    def __init__(self, bot):
        self.bot = bot
        self.fate_die = ('[-]', '[ ]', '[+]')

    @commands.command(name='куб', aliases=['r', 'р' 'k', 'к', 'roll', 'ролл'])
    async def roll(self, ctx, *, arg):
        """кидаю кубы, прибавляю модификаторы~"""
        sol, ans = d2(arg)
        s = f'Кидаю\n-> {sol}\n= **{ans}**'
        await ctx.send(s)

    @commands.command(name='днд', aliases=['закл', 'спелл', 'dnd5', 'spell', 'dnd', 'днд'])
    async def spell_dnd5(self, ctx, *, arg):
        """узнать о заклинании из D&D 5e"""
        await ctx.send(get_spell_dnd_su(arg))

    @commands.command(name='пф', aliases=['pf', 'пф2', 'pf2'])
    async def info_pf2(self, ctx, *, arg):
        """узнать о любой вещи из Pathfinder 2e"""
        await ctx.send(get_info_pf2(arg))

    @commands.command(name='фейт', aliases=['f', 'ф', 'фейт', 'fate'])
    async def fate(self, ctx, *, arg):
        """бросок четырех кубов системы Fate"""
        mod = arg.replace(' ', '')
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

