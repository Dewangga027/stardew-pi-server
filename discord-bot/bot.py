import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from commands import docker_cmd
from commands import health
from commands import help as help_command
from commands import ping
from commands import status


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")


if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN tidak ditemukan di .env"
    )

if not GUILD_ID:
    raise RuntimeError(
        "DISCORD_GUILD_ID tidak ditemukan di .env"
    )


GUILD = discord.Object(
    id=int(GUILD_ID)
)

intents = discord.Intents.default()


class JunimoBot(discord.Client):
    def __init__(self):
        super().__init__(
            intents=intents
        )

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        synced = await self.tree.sync(
            guild=GUILD
        )

        print(
            f"Synced {len(synced)} guild command(s)"
        )

        for command in synced:
            print(
                f"- /{command.name}"
            )


bot = JunimoBot()


ping.register(bot, GUILD)
status.register(bot, GUILD)
health.register(bot, GUILD)
docker_cmd.register(bot, GUILD)
help_command.register(bot, GUILD)


@bot.event
async def on_ready():
    print(
        f"Logged in as: {bot.user}"
    )

    print(
        f"Bot ID: {bot.user.id}"
    )

    print(
        f"Connected to {len(bot.guilds)} server(s)"
    )

    for guild in bot.guilds:
        print(
            f"- {guild.name} ({guild.id})"
        )


bot.run(TOKEN)