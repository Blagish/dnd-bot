import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from help import MyHelpCommand
import loguru

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

        await bot.start(os.environ.get("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
