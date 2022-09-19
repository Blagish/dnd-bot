from random import randint

from discord import Embed, Colour, ButtonStyle
from discord.ext import commands
from parser import d2
from game_data import get_spell_dnd_su, get_spell_wikidot, get_info_pf2, get_english_name
from util import ctx_send
import re


class Dice(commands.Cog, name='Кубы кубы'):
    def __init__(self, bot):
        self.bot = bot
        self.fate_die = ('[-]', '[ ]', '[+]')

    @staticmethod
    def error_message(error):
        return Embed(title="Произошла непредвиденная ошибка :(",
                     description=f'**Код ошибки:** {error}.\nЧто бы это ни было, возможно, когда-нибудь это пофиксится',
                     colour=Colour.red())

    @commands.command(name='куб', aliases=['r', 'р', 'k', 'к', 'roll', 'ролл'])
    async def roll(self, ctx, *, string):
        """Кидаю кубы, прибавляю модификаторы~ Можно использовать сложение, вычитание, умножение, деление. Кубы с преимуществом - ad, с помехой - dd. Можно использовать скобки, короче, реально охуенный парсер, два года его писала """
        # if string.strip() == '':
        #     view = ui.View()
        #     d4 = ui.Button(style=ButtonStyle.green, label='d4')
        #     d6 = ui.Button(style=ButtonStyle.gray, label='d6')
        #     d8 = ui.Button(style=ButtonStyle.green, label='d8')
        #     d10 = ui.Button(style=ButtonStyle.gray, label='d10')
        #     d12 = ui.Button(style=ButtonStyle.green, label='d12')
        #     d20 = ui.Button(style=ButtonStyle.red, label='d20')
        #     d100 = ui.Button(style=ButtonStyle.blurple, label='d100')
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
        """Узнать о заклинании из D&D 5e. Как на русском, так и на английском; Укажите "ru" или "en" перед названием заклинания для выбора соответствующего языка."""
        get_from_spell_source = get_spell_dnd_su
        if spell_name[:3] in ('ru ', 'ру '):
            spell_name = spell_name[3:]
            get_from_spell_source = get_spell_dnd_su
        elif spell_name[:3] in ('en ', 'ен ', 'ан '):
            spell_name = spell_name[3:]
            get_from_spell_source = get_spell_wikidot
            if any('а' <= c <= 'я' for c in spell_name):  # если название спелла на русском
                spell_name = get_english_name(spell_name)
                if not spell_name:
                    spell_name = 'aaaaaaaaa'
        elif any('a' <= c <= 'z' for c in spell_name):  # если есть английские буквы
            get_from_spell_source = get_spell_wikidot

        async with ctx.typing():
            try:
                message = get_from_spell_source(spell_name)
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

    @commands.command(name='клинки', aliases=['квт', 'кт', 'bd', 'blades'])
    async def blades(self, ctx, *, mod):
        """Бросок системы Blades in the Dark. 0 для худшего результата из двух, любое другое число для лучшего результата."""
        n = int(mod)
        s = 'Кидаю\n-> '
        if n == 0:
            a, b = randint(1, 6), randint(1, 6)
            s += f'[**{a}**], [**{b}**]\n'
            s += f'**Худший результат: {min(a, b)}**'
        else:
            nums = [randint(1, 6) for i in range(n)]
            s += (len(nums) * '[**{}**], ').format(*nums)[:-2]
            s += f'\n**Лучший результат: {max(nums)}**'
        await ctx.send(s)

    @commands.command(name='пбта', aliases=['apoc', 'pb', 'pbta', 'пб'])
    async def pbta(self, ctx, *mod):
        """Бросок системы PBTA. Может принимать в себя любое вычисляемое выражение."""
        arg = ''.join(mod)
        if arg[0] not in ('*', '-', '/'):
            arg = f'+{arg}'
        command = f'2d6{arg}'
        sol, ans = d2(command)
        ans = ans.ops[0]
        res = 'успех'
        if ans < 7:
            res = 'провал'
        elif ans > 9:
            res = 'полный успех'
        s = f'Кидаю\n-> {sol}\n**Результат: {ans}, {res}**'
        await ctx.send(s)

    @commands.command(name='см', aliases=['сома', 'мист', 'сити', 'com', 'cm', 'cum'])
    async def com(self, ctx, *mod):
        """Бросок системы City of Mist. Может принимать в себя любое вычисляемое выражение."""
        arg = ''.join(mod)
        if arg[0] not in ('*', '-', '/'):
            arg = f'+{arg}'
        command = f'2d6{arg}'
        sol, ans = d2(command)
        s = f'Кидаю\n-> {sol}\n**Результат: {ans}**'
        await ctx.send(s)

    @commands.command(name='пп', aliases=['пнп', 'pp', 'pnp'])
    async def pnp(self, ctx, *, rolls):
        """Бросок системы Prowlers & Paragons. Принимает один параметр - число бросков."""
        n = int(rolls)
        command = f"sum(map(((it=2)+(it=4)+2*(it=6)):{n}x(d6)))"
        sol, ans = d2(command)
        sol = sol[4:-1]
        s = f'Кидаю\n-> {sol}\n**Успехов: {ans}**'
        await ctx.send(s)

    @commands.command(name='св', aliases=['sw', 'sav', 'сав'])
    async def sw(self, ctx, *, string):
        """Бросок системы Savage Worlds. Принимает в себя вычисляемую строку, автоматически добавляет дикий куб d6."""
        wild_die = 'b6'
        grade_text = {0: 'ями', 1: 'ем'}
        throw_wild_die = True
        success_bar = 4
        uprise_bar = 4
        string = string.replace(' ', '')
        is_bar = string.rfind('/')
        if is_bar > 0:
            success_bar = int(string[is_bar+1:])
            string = string[:is_bar]

        string = re.sub(r'([dд])(\d+)', r'b\2', string)  # + f', {wild_die}'
        string = re.sub(r'(\d+)*b(\d+)([\+\-]\d+)*', r'<\1x>(b\2\3)', string)
        string = string.replace('<x>', '1x').replace('<', '').replace('>', '')

        sol, ans = d2(f'max({string})')
        ans = ans.ops[0]
        if ans < success_bar:
            msg = 'провал'
        elif (grade := (ans-success_bar)//uprise_bar) == 0:
            msg = 'успех'
        else:
            msg = f'успех с {grade} повышени{grade_text.get(grade%10==1)}'

        s = f'Кидаю; целевое число = {success_bar}\n-> {sol[4:-1]}\n**Результат: {ans}, {msg}!**'
        await ctx.send(s)
