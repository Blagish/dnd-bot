import json
from discord.ext import commands
from game_data import get_spell_dnd_su, get_info_pf2
from random import choice, randint
from parser import d2
from bot_config import command_prefix

bot = commands.Bot(command_prefix)
fate_die = ('[-]', '[ ]', '[+]')
with open('macros.json', 'r', encoding='utf-8') as file:
    macri = json.loads(file.read())


@bot.command(name='hello', aliases=['привет', 'hewwo', 'owo'])
async def hello(ctx):
    await ctx.send('hewwo OwO')

# help


@bot.command(name='roll', aliases=['r', 'р' 'k', 'к'])
async def roll(ctx, *, arg):
    sol, ans = d2(arg)
    s = f'Кидаю\n-> {sol}\n= **{ans}**'
    await ctx.send(s)


@bot.command(name='fate', aliases=['f', 'ф', 'фейт'])
async def fate(ctx, *, arg):
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
        s += fate_die[d + 1]
        res += d
    s += f'** {sign} {abs(mod)}\n= **{res + mod}**'
    await ctx.send(s)


@bot.command(name='макрос', aliases=['macros', 'mc', 'мк'])
async def macros(ctx, command, *, arg):
    true_command = macri.get(command)
    if true_command is not None:
        try:
            full = true_command[0].format(*arg)
            print(full)
        except IndexError:
            return 'Ошибка: не хватает значений.'
        sol, ans = d2(full)
        s = f'Кидаю\n-> {sol}\n{true_command[1].format(ans)}'
        await ctx.send(s)
    await ctx.send(f'Ошибка: макрос "{command}" не найден.')


@bot.command(name='mchelp', aliases=['мкхелп'])
async def macros_list(ctx):
    s = ''
    for m in macri:
        data = macri[m]
        s += f'{m}: {data[2]} Аналог команды {data[0]}.\n'
    await ctx.send(s)


@bot.command(name='spell', aliases=['закл', 'спелл'])
async def spell_dnd5(ctx, *, arg):
    await ctx.send(get_spell_dnd_su(arg))


@bot.command(name='pf2', aliases=['pf', 'пф', 'пф2'])
async def info_pf2(ctx, *, arg):
    await ctx.send(get_info_pf2(arg))


@bot.command(name='спасибо', aliases=['спс', 'thanks', 'thx'])
async def thanks(ctx):
    res = choice(['Пожалуйста!', 'Рада помочь!', 'Всегда пожалуйста', 'Стараюсь :)'])
    await ctx.send(res)


@bot.command(name='слышь', aliases=['слыш', 'э', 'слiш', 'bruh', 'брух'])
async def anger(ctx):
    res = choice(['Виноваты кубики', 'Оно само', 'Это не я', 'Я честно не виновата', 'Все вопросы к кубам!'])
    await ctx.send(res)


@bot.command(name='куку', hidden=True)
async def kuku(ctx):
    return ctx.send('быбы')
