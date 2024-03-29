from discord.ext import commands
import json

from parser import d2
from util import send_long_message


class Macros(commands.Cog, name='Макросы'):
    def __init__(self, bot):
        self.bot = bot
        with open('commands/macros.json', 'r', encoding='utf-8') as file:
            self.macri = json.loads(file.read())

    @commands.command(name='макрос', aliases=['macros', 'mc', 'мк'])
    async def macros(self, ctx, *arg):
        """Использовать макрос кидания кубов. В бета-тестировании, пока есть макросы для City of Mist и Prowlers & Paragons"""
        command = arg[0]
        arg = [''.join(arg[1:])]
        true_command = self.macri.get(command)
        if true_command is not None:
            try:
                full = true_command[0].format(*arg)
                print(full)
            except IndexError:
                return 'Ошибка: не хватает значений.'
            sol, ans = d2(full)
            s = f'Кидаю\n-> {sol}\n{true_command[1].format(ans)}'
            await send_long_message(ctx, s)
        else:
            await ctx.send(f'Ошибка: макрос "{command}" не найден.')

    @commands.command(name='мкхелп', aliases=['mchelp'])
    async def macros_list(self, ctx):
        """Выводит список доступных макросов."""
        s = ''
        for m in self.macri:
            data = self.macri[m]
            s += f'{m}: {data[2]} Аналог команды {data[0]}.\n'
        await ctx.send(s)
