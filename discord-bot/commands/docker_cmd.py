import platform
from datetime import datetime

import discord

from services.docker_service import get_docker_snapshot


def register(bot, guild):
    @bot.tree.command(
        name="docker",
        description="Tampilkan status Docker dan Container",
        guild=guild,
    )
    async def docker_status(interaction: discord.Interaction):
        data = get_docker_snapshot()

        if data is None:
            embed = discord.Embed(
                title="🐳 Docker Status",
                description="🔴 Docker daemon tidak bisa diakses",
                timestamp=datetime.now(),
            )

            embed.add_field(
                name="Status",
                value="`Unavailable`",
                inline=True,
            )

            embed.add_field(
                name="Host",
                value=f"`{platform.node()}`",
                inline=True,
            )

            await interaction.response.send_message(embed=embed)
            return

        lines = data["containers"]

        if lines:
            container_text = "\n".join(lines[:15])
        else:
            container_text = "Tidak ada container"

        embed = discord.Embed(
            title="🐳 Docker Status",
            description="✅ Docker daemon aktif",
            timestamp=datetime.now(),
        )

        embed.add_field(
            name="Docker Version",
            value=f"`{data['version']}`",
            inline=True,
        )

        embed.add_field(
            name="Architecture",
            value=f"`{data['architecture']}`",
            inline=True,
        )

        embed.add_field(
            name="Containers",
            value=(
                f"🟢 Running: `{data['running']}`\n"
                f"🔴 Stopped: `{data['stopped']}`"
            ),
            inline=True,
        )

        embed.add_field(
            name="Container List",
            value=container_text,
            inline=False,
        )

        embed.set_footer(
            text="Junimo Server Bot • Docker Monitor"
        )

        await interaction.response.send_message(embed=embed)