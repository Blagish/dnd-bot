import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from help import MyHelpCommand
import loguru
from app.game_data.pf2_new.searcher import initialize_pf2_indexer

logger = loguru.logger

intents = discord.Intents.default()
intents.message_content = True


command_prefix = os.environ.get("COMMAND_PREFIX")
bot = commands.Bot(
    intents=intents,
    command_prefix=commands.when_mentioned_or(command_prefix),
    activity=discord.Activity(
        type=discord.ActivityType.listening, name=f"{command_prefix}help"
    ),
)
bot.remove_command("help")
bot.help_command = MyHelpCommand(
    sort_commands=False,
    commands_heading="(команды):",
    aliases_heading="Варианты:",
    no_category="Просто",
)


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    """Sync commands"""
    synced = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands globally")


async def main():
    async with bot:
        await bot.load_extension("app.commands")
        await bot.load_extension("app.tasks")
        
        # Инициализируем индексатор PF2e данных при запуске
        logger.info("Инициализация индексатора PF2e данных...")
        try:
            initialize_pf2_indexer()
            logger.info("Индексатор PF2e данных успешно инициализирован")
        except Exception as e:
            logger.error(f"Ошибка при инициализации индексатора PF2e данных: {e}")

        await bot.start(os.environ.get("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
