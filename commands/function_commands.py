from random import randint
from discord.ext import commands
from parser import d2
from game_data import get_spell_dnd_su, get_info_pf2


class FunctionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fate_die = fate_die = ('[-]', '[ ]', '[+]')

    @commands.command(name='roll', aliases=['r', 'р' 'k', 'к'])
    async def roll(self, ctx, *, arg):
        sol, ans = d2(arg)
        s = f'Кидаю\n-> {sol}\n= **{ans}**'
        await ctx.send(s)

    @commands.command(name='fate', aliases=['f', 'ф', 'фейт'])
    async def fate(self, ctx, *, arg):
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

    @commands.command(name='spell', aliases=['закл', 'спелл'])
    async def spell_dnd5(self, ctx, *, arg):
        await ctx.send(get_spell_dnd_su(arg))

    @commands.command(name='pf2', aliases=['pf', 'пф', 'пф2'])
    async def info_pf2(self, ctx, *, arg):
        await ctx.send(get_info_pf2(arg))


async def setup(bot):
    print('loading FunctionCommands...')
    bot.add_cog(FunctionCommands(bot))
