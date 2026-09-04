import os
import platform
from datetime import datetime, timedelta

import discord
import psutil
from discord import app_commands
from dotenv import load_dotenv

import docker
import subprocess

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN tidak ditemukan di .env")

if not GUILD_ID:
    raise RuntimeError("DISCORD_GUILD_ID tidak ditemukan di .env")


GUILD = discord.Object(id=int(GUILD_ID))
intents = discord.Intents.default()


class JunimoBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        synced = await self.tree.sync(guild=GUILD)

        print(f"Synced {len(synced)} guild command(s)")
        for command in synced:
            print(f"- /{command.name}")


bot = JunimoBot()


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Connected to {len(bot.guilds)} server(s)")

    for guild in bot.guilds:
        print(f"- {guild.name} ({guild.id})")


def format_bytes(value):
    gb = value / (1024 ** 3)
    return f"{gb:.1f} GB"


def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    uptime = timedelta(seconds=int(uptime.total_seconds()))

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m"

def health_state(value, warning, critical):
    if value >= critical:
        return "🔴 Critical"
    elif value >= warning:
        return "⚠️ Warning"
    else:
        return "✅ Healthy"

def get_docker_client():
    try:
        client = docker.from_env()
        client.ping()
        return client
    except Exception:
        return None


@bot.tree.command(
    name="ping",
    description="Check apakah bot aktif",
    guild=GUILD
)
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"🏓 Pong! `{latency} ms`"
    )


@bot.tree.command(
    name="status",
    description="Tampilkan status server",
    guild=GUILD
)
async def status(interaction: discord.Interaction):

    cpu_usage = psutil.cpu_percent(interval=0.5)

    memory = psutil.virtual_memory()

    disk_path = "C:\\" if platform.system() == "Windows" else "/"
    disk = psutil.disk_usage(disk_path)

    uptime = get_uptime()

    embed = discord.Embed(
        title="🍓 Junimo Server Status",
        description="System monitoring",
        timestamp=datetime.now()
    )

    embed.add_field(
        name="🤖 Bot",
        value="🟢 Online",
        inline=True
    )

    embed.add_field(
        name="🏓 Discord Latency",
        value=f"`{round(bot.latency * 1000)} ms`",
        inline=True
    )

    embed.add_field(
        name="⏱ Uptime",
        value=f"`{uptime}`",
        inline=True
    )

    embed.add_field(
        name="🖥 Host",
        value=f"`{platform.node()}`",
        inline=True
    )

    embed.add_field(
        name="💻 OS",
        value=f"`{platform.system()}`",
        inline=True
    )

    embed.add_field(
        name="🏗 Architecture",
        value=f"`{platform.machine()}`",
        inline=True
    )

    embed.add_field(
        name="⚙️ CPU Usage",
        value=f"`{cpu_usage:.1f}%`",
        inline=True
    )

    embed.add_field(
        name="🧠 RAM",
        value=(
            f"`{format_bytes(memory.used)} / "
            f"{format_bytes(memory.total)}`\n"
            f"`{memory.percent:.1f}% used`"
        ),
        inline=True
    )

    embed.add_field(
        name="💾 Storage",
        value=(
            f"`{format_bytes(disk.used)} / "
            f"{format_bytes(disk.total)}`\n"
            f"`{disk.percent:.1f}% used`"
        ),
        inline=True
    )

    embed.set_footer(
        text="Junimo Server Bot • Stardew Valley Server"
    )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(
    name="health",
    description="Periksa kesehatan server",
    guild=GUILD
)
async def health(interaction: discord.Interaction):

    cpu_usage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()

    disk_path = "C:\\" if platform.system() == "Windows" else "/"
    disk = psutil.disk_usage(disk_path)

    latency = round(bot.latency * 1000)

    cpu_state = health_state(
        cpu_usage,
        warning=70,
        critical=90
    )

    ram_state = health_state(
        memory.percent,
        warning=75,
        critical=90
    )

    disk_state = health_state(
        disk.percent,
        warning=80,
        critical=90
    )

    latency_state = health_state(
        latency,
        warning=150,
        critical=300
    )

    states = [
        cpu_state,
        ram_state,
        disk_state,
        latency_state
    ]

    if any("Critical" in state for state in states):
        overall = "🔴 Critical"

    elif any("Warning" in state for state in states):
        overall = "⚠️ Warning"

    else:
        overall = "✅ Healthy"

    embed = discord.Embed(
        title="🌱 Junimo Server Health",
        description=f"Overall Status: **{overall}**",
        timestamp=datetime.now()
    )

    embed.add_field(
        name="⚙️ CPU",
        value=(
            f"`{cpu_usage:.1f}%`\n"
            f"{cpu_state}"
        ),
        inline=True
    )

    embed.add_field(
        name="🧠 RAM",
        value=(
            f"`{memory.percent:.1f}%`\n"
            f"{ram_state}"
        ),
        inline=True
    )

    embed.add_field(
        name="💾 Storage",
        value=(
            f"`{disk.percent:.1f}%`\n"
            f"{disk_state}"
        ),
        inline=True
    )

    embed.add_field(
        name="🏓 Discord",
        value=(
            f"`{latency} ms`\n"
            f"{latency_state}"
        ),
        inline=True
    )

    embed.add_field(
        name="⏱ Uptime",
        value=f"`{get_uptime()}`",
        inline=True
    )

    embed.add_field(
        name="🖥 Host",
        value=f"`{platform.node()}`",
        inline=True
    )

    embed.set_footer(
        text="Junimo Server Bot • Health Monitor"
    )

    await interaction.response.send_message(
        embed=embed
    )

@bot.tree.command(
    name="docker",
    description="Tampilkan status Docker dan Container",
    guild=GUILD
)
async def docker_status(interaction: discord.Interaction):

    client = get_docker_client()

    if client is None:
        embed = discord.Embed(
            title="🐳 Docker Status",
            description="🔴 Docker daemon tidak bisa di akses",
            timestamp= datetime.now()
        )

        embed.add_field(
            name="Status",
            value="`Unavailable`",
            inline=True
        )

        embed.add_field(
            name="Host",
            value=f"`{platform.mode()}`",
            inline=True
        )

        await interaction.response.send_message(embed=embed)
        return

    info = client.info()

    containers = client.containers.list(all=True)

    running = 0
    stopped = 0

    container_lines = []

    for container in containers:

        if container.status == "running":
            running += 1
            icon = "🟢"
        else:
            stopped += 1
            icon = "🔴"

        container_lines.append(
            f"{icon} `{container.name}` - `{container.status}`"
        )

    if not container_lines:
        container_text = "Tidak ada container"
    else:
        container_text = "\n".join(container_lines[:15])

    embed = discord.Embed(
        title="🐳 Docker Status",
        description="✅ Docker daemon aktif",
        timestamp=datetime.now()
    )

    embed.add_field(
        name="Docker Version",
        value=f"`{info.get('ServeVersion', 'Unknown')}`",
        inline=True
    )

    embed.add_field(
        name="Architecture",
        value=f"`{info.get('Architecture', 'Unknown')}`",
        inline=True
    )

    embed.add_field(
        name="Containers",
        value=(
            f"🟢 Running: `{running}`\n"
            f"🔴 Stopped: `{stopped}`"
        ),
        inline=True
    )

    embed.add_field(
        name="Container List",
        value=container_text,
        inline=False
    )

    embed.set_footer(
        text="Junimo Server Bot • Docker Monitor"
    )

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)