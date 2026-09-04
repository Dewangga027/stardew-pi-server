from datetime import datetime

import discord

from services.docker_service import get_docker_health
from services.nvme_service import get_nvme_health, get_nvme_smart
from services.system_service import get_system_snapshot
from utils.health import health_state, overall_health


def register(bot, guild):
    @bot.tree.command(
        name="health",
        description="Periksa kesehatan server",
        guild=guild,
    )
    async def health(interaction: discord.Interaction):
        data = get_system_snapshot()

        memory = data["memory"]
        disk = data["disk"]
        cpu_usage = data["cpu_usage"]
        cpu_temp = data["cpu_temperature"]
        throttling = data["throttling"]

        latency = round(bot.latency * 1000)

        cpu_state = health_state(
            cpu_usage,
            warning=70,
            critical=90,
        )

        ram_state = health_state(
            memory.percent,
            warning=75,
            critical=90,
        )

        disk_state = health_state(
            disk.percent,
            warning=80,
            critical=90,
        )

        # Discord latency hanya informasi.
        # Tidak menentukan overall health host.
        latency_state = health_state(
            latency,
            warning=300,
            critical=1000,
        )

        if cpu_temp is None:
            temp_state = "⚪ Unknown"
            temp_text = "Unknown"
        else:
            temp_state = health_state(
                cpu_temp,
                warning=70,
                critical=85,
            )
            temp_text = f"{cpu_temp:.1f} °C"

        if throttling is None:
            throttling_state = "⚪ Unknown"
            throttling_text = "Unknown"

        elif throttling.lower() == "0x0":
            throttling_state = "✅ Healthy"
            throttling_text = throttling

        else:
            throttling_state = "⚠️ Warning"
            throttling_text = throttling

        docker_health = get_docker_health()
        docker_state = docker_health["state"]

        nvme_smart = get_nvme_smart()
        nvme_state = get_nvme_health(nvme_smart)

        host_states = [
            cpu_state,
            ram_state,
            disk_state,
            temp_state,
            throttling_state,
            docker_state,
            nvme_state,
        ]

        overall = overall_health(host_states)

        embed = discord.Embed(
            title="🌱 Junimo Server Health",
            description=f"Overall Status: **{overall}**",
            timestamp=datetime.now(),
        )

        embed.add_field(
            name="🌡 CPU Temperature",
            value=(
                f"`{temp_text}`\n"
                f"{temp_state}"
            ),
            inline=True,
        )

        embed.add_field(
            name="⚙️ CPU Usage",
            value=(
                f"`{cpu_usage:.1f}%`\n"
                f"{cpu_state}"
            ),
            inline=True,
        )

        embed.add_field(
            name="🧠 RAM",
            value=(
                f"`{memory.percent:.1f}%`\n"
                f"{ram_state}"
            ),
            inline=True,
        )

        embed.add_field(
            name="💾 Storage",
            value=(
                f"`{disk.percent:.1f}%`\n"
                f"{disk_state}"
            ),
            inline=True,
        )

        embed.add_field(
            name="⚡ Throttling",
            value=(
                f"`{throttling_text}`\n"
                f"{throttling_state}"
            ),
            inline=True,
        )

        embed.add_field(
            name="🐳 Docker",
            value=docker_state,
            inline=True,
        )

        embed.add_field(
            name="🏓 Discord",
            value=(
                f"`{latency} ms`\n"
                f"{latency_state}"
            ),
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

        if nvme_smart:
            nvme_temp = nvme_smart.get("temperature")
            nvme_used = nvme_smart.get("percentage_used")
            media_errors = nvme_smart.get("media_errors")

            nvme_temp_text = (
                f"{nvme_temp:.0f} °C"
                if nvme_temp is not None
                else "Unknown"
            )

            nvme_used_text = (
                f"{nvme_used:.0f}%"
                if nvme_used is not None
                else "Unknown"
            )

            media_text = (
                f"{media_errors:.0f}"
                if media_errors is not None
                else "Unknown"
            )

            nvme_value = (
                f"Temperature: `{nvme_temp_text}`\n"
                f"Percentage Used: `{nvme_used_text}`\n"
                f"Media Errors: `{media_text}`\n"
                f"{nvme_state}"
            )

        else:
            nvme_value = (
                "`SMART data unavailable`\n"
                f"{nvme_state}"
            )

        embed.add_field(
            name="💿 NVMe SMART",
            value=nvme_value,
            inline=False,
        )

        embed.set_footer(
            text="Junimo Server Bot • Health Monitor"
        )

        await interaction.response.send_message(
            embed=embed
        )