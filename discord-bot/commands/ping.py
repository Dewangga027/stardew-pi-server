import discord
from discord import app_commands


def register(bot, guild):
    @bot.tree.command(
        name="ping",
        description="Check apakah bot aktif",
        guild=guild,
    )
    async def ping(interaction: discord.Interaction):
        latency = round(bot.latency * 1000)

        await interaction.response.send_message(
            f"🏓 Pong! `{latency} ms`"
        )