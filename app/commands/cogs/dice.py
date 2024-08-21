from discord import app_commands
from discord.ext import commands
from app.parser import d2
from app.parser.custom_random import rangen
from app.commands.base import BaseCog
from typing import Optional
import loguru
from app.models.rollResponse import RollResponse
import re

logger = loguru.logger


class Dice(BaseCog, name="Кубы кубы"):
    async def fix_expression(self, ctx: commands.Context):
        if ctx.args:  # as non-slash command
            content = ctx.message.content
            line = content[content.find(" ") + 1 :]
            ctx.args[2] = line

    async def fix_comment(self, ctx: commands.Context):
        if ctx.args:  # as non-slash command
            cur_arg = ctx.args[2]
            content = ctx.message.content
            line = content[content.find(cur_arg) :]
            ctx.args[2] = line

    @commands.hybrid_command(
        name="roll",
        description="Кинуть куб",
        aliases=["r", "р", "k", "к", "куб", "ролл"],
    )
    @app_commands.describe(expression="Строка выражения")
    @commands.before_invoke(fix_expression)
    async def roll(self, ctx: commands.Context, expression: str):
        """Кидаю кубы, прибавляю модификаторы~
        - Куб указывается буквой **д**/**d** и числом за ним - `д20, d6, d69, д420`.
        - Чтобы кинуть куб с *преимуществом* (выбирается наибольший результат из двух бросков) или с *помехой* (наименьший), используйте **ad**/**ад** и **dd**/**дд** сооветственно.
        - Есть также опции для *тройного* или *четверного преимущества* - ed, kd.
        - Можно кинуть несколько кубов сразу, результат суммируется - `5d12, 2ad20, 20д4`.
        - Поддерживаются основные арифметические операции - *сложение, вычитание, умножение и деление*. И, само собой, целые и дробные числа.
        - Также поддерживаются *сравнения* двух чисел (больше, меньше, равно, больше или равно, меньше или равно, неравно) - **>**, **<**, **=**, **>=**/**=>**, **<=**/**=<**, **≠** или **!=** если вы погромист
        - Поддерживаются математические функции минимума, максимума и суммы - **min**, **max**, **sum**. Пример: `min(d20+4, d20+8)`.
        - Можно указывать несколько команд через запятую! `/roll d20+10, 5d8+2, 2d6+12`

        - Вы можете указать после выражения небольшой комментарий - например, тип урона или тему броска. Даника автоматически сгруппирует кубы с одинаковым комментарием, например: `/р 2д6 режущ + д8 огонь + д6 кислота + д10 огонь` выдаст что-то вроде `(7 режущ, 14 огонь, 3 кислота)`. Это можно использовать, если у монстров есть сопротивление или уязвимость к определенным видам урона, ну или просто для удобства, как тут: `д20+6 атака, д20+3 инициатива, д20+8 stealth` и т.д. **ВНИМАНИЕ** комментарий должен быть без пробелов, единым словом, и не содержать в себе чисел и специальных знаков.

        - В некоторых играх есть *"взрывающиеся"* кубы, когда куб *бросается еще раз*, если на нём выпадает максимум - **b**/**б**. `b6, b8`, т.д.
        - Если вы кидаете такой куб, что выпавшее на нём число *заменяется*, если оно меньше указанного (как способность разбойника Надёжный талант в D&D) - укажите **%** после куба. `d20%15, d6%2`
        """
        sol, ans = d2(expression)
        res = RollResponse(command=expression, lines=sol, result=f"= {ans}")
        await ctx.reply(res.to_str())

    @commands.hybrid_command(name="fate", aliases=["f", "ф", "фейт"])
    @app_commands.describe(mod="Число-модификатор. Удалить для нуля")
    async def fate(self, ctx: commands.Context, mod: Optional[int] = 0):
        """Бросок четырех кубов системы Fate"""
        fate_die = ("[-]", "[ ]", "[+]")
        sign = "+" if mod >= 0 else "-"
        s = ""
        res = 0
        for i in range(4):
            d = rangen.roll(3)
            s += fate_die[d - 1]
            res += d - 2
        result = RollResponse(
            command=f"4 куба {sign} {abs(mod)}", lines=s, result=f"= {res + mod}"
        )
        await ctx.reply(result.to_str(), mention_author=False)

    @commands.hybrid_command(name="blades", aliases=["квт", "кт", "bd", "клинки"])
    @app_commands.describe(mod="Число-модификатор. Удалить для нуля")
    async def blades(self, ctx: commands.Context, mod: Optional[int] = 0):
        """Бросок системы Blades in the Dark."""
        if mod == 0:
            a, b = rangen.roll(6, times=2)
            res = RollResponse(
                opening="Беру",
                command="худший результат из 2 кубов",
                lines=f"[**{a}**], [**{b}**]",
                result=f"Худший результат: {min(a, b)}",
            )
        else:
            nums = rangen.roll(6, times=mod)
            lines = (len(nums) * "[**{}**], ").format(*nums)[:-2]
            res = RollResponse(
                opening="Беру",
                command="худший результат из 2 кубов",
                lines=lines,
                result=f"Лучший результат: {max(nums)}",
            )
        await ctx.reply(res.to_str(), mention_author=False)

    @commands.hybrid_command(name="pbta", aliases=["apoc", "pb", "пбта", "пб"])
    @app_commands.describe(mod="Число-модификатор. Удалить для нуля")
    async def pbta(self, ctx: commands.Context, mod: Optional[int] = 0):
        """Бросок системы PBTA."""
        arg = str(mod)
        if arg[0] != "-":
            arg = f"+{arg}"
        command = f"2d6{arg}"
        sol, ans = d2(command)
        ans = int(ans)
        res = "успех"
        if ans < 7:
            res = "провал"
        elif ans > 9:
            res = "полный успех"
        result = RollResponse(
            command=command, lines=sol, result=f"Результат: {ans}, {res}"
        )
        await ctx.reply(result.to_str(), mention_author=False)

    @commands.hybrid_command(
        name="mist", aliases=["сома", "мист", "сити", "com", "cm", "см"]
    )
    @app_commands.describe(mod="Число-модификатор. Удалить для нуля")
    async def com(self, ctx: commands.Context, mod: Optional[int] = 0):
        """Бросок системы City of Mist. Может принимать в себя любое вычисляемое выражение."""
        arg = str(mod)
        if arg[0] != "-":
            arg = f"+{arg}"
        command = f"2d6{arg}"
        sol, ans = d2(command)
        res = RollResponse(command=command, lines=sol, result=f"Результат: {ans}")
        await ctx.reply(res.to_str(), mention_author=False)

    @commands.hybrid_command(name="пп", aliases=["пнп", "pp", "pnp"])
    @app_commands.describe(rolls="Число бросков", comment="Комментарий")
    @commands.before_invoke(fix_comment)
    async def pnp(self, ctx: commands.Context, rolls: int, comment: Optional[str] = ""):
        """Бросок системы Prowlers & Paragons."""
        command = f"sum(map(((it=2)+(it=4)+2*(it=6)):{rolls}x(d6)))"
        sol, ans = d2(command)
        res = RollResponse(
            command=f"{rolls}d",
            comment=comment,
            lines=sol[4:-1],
            result=f"Успехов: {ans}",
        )
        await ctx.reply(res.to_str(), mention_author=False)

    @commands.hybrid_command(name="sw", aliases=["св", "sav", "сав"])
    @app_commands.describe(expression="Строка выражения")
    @commands.before_invoke(fix_expression)
    async def sw(self, ctx: commands.Context, expression):
        """Бросок системы Savage Worlds."""
        wild_die = "b6"
        grade_text = {0: "ями", 1: "ем"}
        throw_wild_die = True
        success_bar = 4
        uprise_bar = 4
        string = expression.replace(" ", "")
        is_bar = string.rfind("/")
        if is_bar > 0:
            success_bar = int(string[is_bar + 1 :])
            string = string[:is_bar]

        string = re.sub(r"([dд])(\d+)", r"b\2", string)  # + f', {wild_die}'
        string = re.sub(r"(\d+)*b(\d+)([\+\-]\d+)*", r"<\1x>(b\2\3)", string)
        string = string.replace("<x>", "1x").replace("<", "").replace(">", "")

        sol, ans = d2(f"max({string})")
        ans = int(ans)
        if ans < success_bar:
            msg = "провал"
        elif (grade := (ans - success_bar) // uprise_bar) == 0:
            msg = "успех"
        else:
            msg = f"успех с {grade} повышени{grade_text.get(grade % 10 == 1)}"

        s = f"Кидаю; \n-> {sol[4:-1]}\n**Результат: {ans}, {msg}!**"
        res = RollResponse(
            command=f"{expression}; целевое число = {success_bar}",
            lines=sol[4:-1],
            result=f"Результат: {ans}, {msg}!",
        )
        await ctx.reply(res.to_str(), mention_author=False)
