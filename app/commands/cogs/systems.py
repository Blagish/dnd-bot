from app.commands.base import BaseCog
from discord.ext import commands
from discord import app_commands, Message
from typing import Literal, Optional
from app.game_data import (
    DndRuSiteSearcher,
    DndEnSiteSearcher,
    get_info_pf2
)
from app.game_data.pf2_new.searcher import search_items
from app.game_data.pf2_new.classes.spells import Spell
from app.game_data.pf2_new.classes.feats import Feat
from app.util.gamedata_buttons import Buttons
from app.models.pf2Response import Pf2Response
from app.enums.PackType import PackType
import loguru

logger = loguru.logger

class Systems(BaseCog, name='Игровые системы'):
    async def fix_thing(self, ctx: commands.Context):
        if ctx.args:  # as non-slash command
            content = ctx.message.content
            line = content[content.find(" ") + 1 :]
            ctx.args[1] = line

    @commands.hybrid_command(
        name="dnd", aliases=["закл", "спелл", "dnd5", "spell", "днд", "днд5"]
    )
    @app_commands.describe(lang="Язык", spell="Название заклинания")
    async def spell_dnd5(
        self, ctx: commands.Context, spell: str, lang: Literal["ru", "en"]
    ):
        """Узнать о заклинании из D&D 5e. Как на русском, так и на английском"""
        match lang:
            case "ru":
                searcher = DndRuSiteSearcher()
            case "en":
                searcher = DndEnSiteSearcher()
                # if any(
                #     "а" <= c <= "я" for c in spell
                # ):  # если название спелла на русском
                #     spell = get_english_name(spell)
                #     if not spell:
                #         spell = "aaaaaaaaa"
                # return
            case _:
                await ctx.reply(embed=self.foreseen_error_message("Неизвестный язык"))
                return

        async with ctx.typing():
            try:
                message = searcher.get_spell(spell)
            except Exception as e:
                message = self.error_message(str(e))
        await ctx.reply(embed=message.embed, mention_author=False)

    @commands.hybrid_command(name="pf2", aliases=["pf", "пф2", "пф"])
    @app_commands.describe(thing="Заклинание/предмет/что угодно из PF2e")
    @commands.before_invoke(fix_thing)
    async def info_pf2(self, ctx: commands.Context, thing: str, trait: Optional[str]):
        """Узнать о любой вещи из Pathfinder 2e. На английском"""
        async with ctx.typing():
            response: Pf2Response = get_info_pf2(thing, trait=trait)
        buttons = None
        if response.choices is not None:
            print('adding choices')
            buttons = Buttons(choices=response.choices, func=get_info_pf2)
        try:
            await ctx.reply(response.message, embed=response.embed, view=buttons, mention_author=False)
        except Exception as e:
            print(e)

        if response.other_embeds:
            for embed in response.other_embeds:
                await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="pf2beta", aliases=["pfb", "пф2б", "пфб"])
    @app_commands.describe(name="[БЕТА] Заклинание/фит из PF2e, новая реализация.")
    @commands.before_invoke(fix_thing)
    async def info_pf2_beta(self, ctx: commands.Context, name: str, type: PackType): #, trait: Optional[str]):
        """[БЕТА] Узнать о заклинании из Pathfinder 2e. На английском. Тест новой реализации"""
        async with ctx.typing():
            logger.debug(f'looking for {name}')
            things = search_items(name, [type])
            logger.debug(f'found {things}')
            if things is None:
                response = Pf2Response(embed=Spell.get_embed_not_found())
            else:
                thing_name = things[0]['path']
                match type:
                    case PackType.spell:
                        thing_cls = Spell
                    case PackType.feat:
                        thing_cls = Feat
                thing = thing_cls.from_file(thing_name)
                if thing:
                    response = thing.to_embed()
                else:
                    response = Pf2Response(embed=Spell.get_embed_not_found())
        try:
            await ctx.reply(response.message, embed=response.embed, file=response.file, mention_author=False)
        except Exception as e:
            print(e)


    # async def send_fron_aon(self, message):
    #     pattern = r'(https?\:\/\/2e\.aonprd\.com\/\w+\.aspx\?ID=\d+)'
    #     if re.match(pattern, message.content):
    #         for i in message.embeds:
    #             title = i.title
    #             thing = title[:title.find('-')].strip()
    #             response: Pf2Response = get_info_pf2(thing)
    #             await message.reply(response.message, embed=response.embed, mention_author=False)
    #
    #
    # @commands.Cog.listener("on_message")
    # async def send_from_aon_listener1(self, message: Message):
    #     await self.send_fron_aon(message)
    #
    # @commands.Cog.listener("on_message_edit")
    # async def send_from_aon_listener2(self, before: Message, after: Message):
    #     await self.send_fron_aon(after)
