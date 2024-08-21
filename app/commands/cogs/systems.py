from app.commands.base import BaseCog
from discord.ext import commands
from discord import app_commands, Message
from typing import Literal
from app.game_data import (
    get_spell_dnd_su,
    get_spell_wikidot,
    get_info_pf2,
    get_english_name,
)
from app.models.pf2Response import Pf2Response
import re
import loguru

logger = loguru.logger

class Systems(BaseCog, name='Игровые системы'):
    async def fix_thing(self, ctx: commands.Context):
        if ctx.args:  # as non-slash command
            content = ctx.message.content
            line = content[content.find(" ") + 1 :]
            ctx.args[1] = line

    @commands.command(
        name="dnd", aliases=["закл", "спелл", "dnd5", "spell", "днд", "днд5"]
    )
    @app_commands.describe(lang="Язык", spell="Название заклинания")
    async def spell_dnd5(
        self, ctx: commands.Context, lang: Literal["ru", "en"], spell: str
    ):
        """Узнать о заклинании из D&D 5e. Как на русском, так и на английском"""
        match lang:
            case "ru":
                get_from_spell_source = get_spell_dnd_su
            case "en":
                get_from_spell_source = get_spell_wikidot
                if any(
                    "а" <= c <= "я" for c in spell
                ):  # если название спелла на русском
                    spell = get_english_name(spell)
                    if not spell:
                        spell = "aaaaaaaaa"
                await ctx.reply(
                    embed=self.foreseen_error_message(
                        "Английский язык временно не поддерживается. Попробуйте позже"
                    )
                )
                return
            case _:
                await ctx.reply(embed=self.foreseen_error_message("Неизвестный язык"))
                return

        async with ctx.typing():
            try:
                message = get_from_spell_source(spell)
            except Exception as e:
                message = self.error_message(str(e))
        await ctx.reply(embed=message, mention_author=False)

    @commands.hybrid_command(name="pf2", aliases=["pf", "пф2", "пф"])
    @app_commands.describe(thing="Заклинание/предмет/что угодно из PF2e")
    @commands.before_invoke(fix_thing)
    async def info_pf2(self, ctx: commands.Context, thing: str):
        """Узнать о любой вещи из Pathfinder 2e. На английском"""
        async with ctx.typing():
            response: Pf2Response = get_info_pf2(thing)
        await ctx.reply(response.message, embed=response.embed, mention_author=False)

        if response.other_embeds:
            for embed in response.other_embeds:
                await ctx.reply(embed=embed, mention_author=False)

    async def send_fron_aon(self, message):
        pattern = r'(https?\:\/\/2e\.aonprd\.com\/\w+\.aspx\?ID=\d+)'
        if re.match(pattern, message.content):
            for i in message.embeds:
                title = i.title
                thing = title[:title.find('-')].strip()
                response: Pf2Response = get_info_pf2(thing)
                await message.reply(response.message, embed=response.embed, mention_author=False)


    @commands.Cog.listener("on_message")
    async def send_from_aon_listener1(self, message: Message):
        await self.send_fron_aon(message)

    @commands.Cog.listener("on_message_edit")
    async def send_from_aon_listener2(self, before: Message, after: Message):
        await self.send_fron_aon(after)
