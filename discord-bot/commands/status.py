from datetime import datetime

import discord

from services.system_service import get_system_snapshot
from utils.formatting import format_bytes


def register(bot, guild):
    @bot.tree.command(
        name="status",
        description="Tampilkan status server",
        guild=guild,
    )
    async def status(interaction: discord.Interaction):
        data = get_system_snapshot()

        memory = data["memory"]
        disk = data["disk"]

        embed = discord.Embed(
            title="🍓 Junimo Server Status",
            description="System monitoring",
            timestamp=datetime.now(),
        )

        embed.add_field(
            name="🤖 Bot",
            value="🟢 Online",
            inline=True,
        )

        embed.add_field(
            name="🏓 Discord Latency",
            value=f"`{round(bot.latency * 1000)} ms`",
            inline=True,
        )

        embed.add_field(
            name="⏱ Uptime",
            value=f"`{data['uptime']}`",
            inline=True,
        )

        embed.add_field(
            name="🖥 Host",
            value=f"`{data['host']}`",
            inline=True,
        )

        embed.add_field(
            name="💻 OS",
            value=f"`{data['os']}`",
            inline=True,
        )

        embed.add_field(
            name="🏗 Architecture",
            value=f"`{data['architecture']}`",
            inline=True,
        )

        embed.add_field(
            name="⚙️ CPU Usage",
            value=f"`{data['cpu_usage']:.1f}%`",
            inline=True,
        )

        embed.add_field(
            name="🧠 RAM",
            value=(
                f"`{format_bytes(memory.used)} / "
                f"{format_bytes(memory.total)}`\n"
                f"`{memory.percent:.1f}% used`"
            ),
            inline=True,
        )

        embed.add_field(
            name="💾 Storage",
            value=(
                f"`{format_bytes(disk.used)} / "
                f"{format_bytes(disk.total)}`\n"
                f"`{disk.percent:.1f}% used`"
            ),
            inline=True,
        )

        embed.set_footer(
            text="Junimo Server Bot • Stardew Valley Server"
        )

        await interaction.response.send_message(embed=embed)