from discord.ext import commands
import json

from parser import d2


class Macros(commands.Cog, name='Макросы'):
    def __init__(self, bot):
        self.bot = bot
        with open('commands/macros.json', 'r', encoding='utf-8') as file:
            self.macri = json.loads(file.read())

    @commands.command(name='макрос', aliases=['macros', 'mc', 'мк'])
    async def macros(self, ctx, *, arg):
        """использовать макрос кидания кубов"""
        command = arg.split(' ')[0]
        arg = arg[arg.find(' ')+1:]
        true_command = self.macri.get(command)
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

    @commands.command(name='мкхелп', aliases=['mchelp'])
    async def macros_list(self, ctx):
        """список доступных макросов"""
        s = ''
        for m in self.macri:
            data = self.macri[m]
            s += f'{m}: {data[2]} Аналог команды {data[0]}.\n'
        await ctx.send(s)
