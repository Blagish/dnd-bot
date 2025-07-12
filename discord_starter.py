import asyncio
import discord
from discord.ext import commands
from help import MyHelpCommand
import loguru
from app.util.config import config

logger = loguru.logger

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    intents=intents,
    command_prefix=commands.when_mentioned_or(config.command_prefix),
    activity=discord.Activity(
        type=discord.ActivityType.listening, name=f"{config.command_prefix}help"
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

        await bot.start(config.discord_token)


if __name__ == "__main__":
    asyncio.run(main())
