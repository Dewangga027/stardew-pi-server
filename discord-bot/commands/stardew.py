from datetime import datetime

import discord

from services.stardew_service import get_stardew_status


def get_status_display(status):
    displays = {
        "running": "🟢 Online",
        "exited": "🔴 Stopped",
        "created": "🟡 Created",
        "restarting": "🟡 Restarting",
        "paused": "🟠 Paused",
        "dead": "🔴 Dead",
        "not_found": "⚪ Not Installed",
        "docker_unavailable": "🔴 Docker Unavailable",
    }

    return displays.get(
        status,
        f"⚪ {status.title()}"
    )


def register(bot, guild):
    @bot.tree.command(
        name="server",
        description="Tampilkan status Stardew Valley Server",
        guild=guild,
    )
    async def server(
        interaction: discord.Interaction,
    ):
        data = get_stardew_status()

        status_display = get_status_display(
            data["status"]
        )

        embed = discord.Embed(
            title="🎮 Stardew Valley Server",
            description=(
                f"Server Status: **{status_display}**"
            ),
            timestamp=datetime.now(),
        )

        embed.add_field(
            name="📦 Container",
            value=f"`{data['name']}`",
            inline=True,
        )

        embed.add_field(
            name="⚙️ Status",
            value=status_display,
            inline=True,
        )

        embed.add_field(
            name="⏱ Uptime",
            value=f"`{data['uptime']}`",
            inline=True,
        )

        embed.add_field(
            name="🐳 Image",
            value=f"`{data['image']}`",
            inline=False,
        )

        embed.add_field(
            name="🌐 Ports",
            value=f"```{data['ports']}```",
            inline=False,
        )

        if data["status"] == "not_found":
            embed.add_field(
                name="ℹ️ Information",
                value=(
                    "Stardew Valley Server belum dipasang.\n"
                    "Container `pi5junimo-server` "
                    "belum ditemukan."
                ),
                inline=False,
            )

        elif data["status"] == "docker_unavailable":
            embed.add_field(
                name="⚠️ Error",
                value=(
                    "Junimo tidak dapat terhubung "
                    "ke Docker daemon."
                ),
                inline=False,
            )

        embed.set_footer(
            text="Junimo Server Bot • Stardew Valley"
        )

        await interaction.response.send_message(
            embed=embed
        )