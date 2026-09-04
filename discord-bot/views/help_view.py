import discord


HELP_PAGES = {
    "overview": {
        "title": "🌱 Junimo Server Bot",
        "description": (
            "Bot monitoring untuk Stardew Valley Server "
            "yang berjalan di Raspberry Pi 5."
        ),
        "fields": [
            (
                "📖 Commands",
                (
                    "`/ping` — Check koneksi bot\n"
                    "`/status` — Informasi server\n"
                    "`/health` — Health monitoring\n"
                    "`/docker` — Status Docker\n"
                    "`/help` — Menu bantuan"
                ),
            ),
        ],
    },

    "monitoring": {
        "title": "🖥 Server Monitoring",
        "description": (
            "Command untuk memonitor kondisi Raspberry Pi."
        ),
        "fields": [
            (
                "🍓 /status",
                (
                    "Menampilkan host, OS, architecture, CPU, "
                    "RAM, storage, uptime dan Discord latency."
                ),
            ),
            (
                "🌱 /health",
                (
                    "Memeriksa CPU temperature, CPU usage, RAM, "
                    "storage, throttling, Docker dan NVMe SMART."
                ),
            ),
            (
                "🏓 /ping",
                "Memeriksa apakah Junimo Bot merespons.",
            ),
        ],
    },

    "docker": {
        "title": "🐳 Docker",
        "description": (
            "Monitoring Docker Engine pada Raspberry Pi."
        ),
        "fields": [
            (
                "🐳 /docker",
                (
                    "Menampilkan Docker version, architecture, "
                    "jumlah container serta status setiap container."
                ),
            ),
        ],
    },

    "stardew": {
        "title": "🎮 Stardew Valley",
        "description": (
            "Fitur pengelolaan Stardew Valley Dedicated Server "
            "akan ditambahkan pada tahap berikutnya."
        ),
        "fields": [
            (
                "🚧 Status",
                "Coming Soon",
            ),
        ],
    },
}


def build_help_embed(page_key="overview"):
    page = HELP_PAGES.get(
        page_key,
        HELP_PAGES["overview"],
    )

    embed = discord.Embed(
        title=page["title"],
        description=page["description"],
    )

    for name, value in page["fields"]:
        embed.add_field(
            name=name,
            value=value,
            inline=False,
        )

    embed.set_footer(
        text="Junimo Server Bot • Stardew Valley Server"
    )

    return embed


class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Overview",
                value="overview",
                emoji="🌱",
                description="Panduan utama Junimo Bot",
            ),
            discord.SelectOption(
                label="Server Monitoring",
                value="monitoring",
                emoji="🖥️",
                description="Status dan health Raspberry Pi",
            ),
            discord.SelectOption(
                label="Docker",
                value="docker",
                emoji="🐳",
                description="Monitoring Docker container",
            ),
            discord.SelectOption(
                label="Stardew Valley",
                value="stardew",
                emoji="🎮",
                description="Stardew Valley server commands",
            ),
        ]

        super().__init__(
            placeholder="Pilih kategori bantuan...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(
        self,
        interaction: discord.Interaction,
    ):
        page = self.values[0]

        await interaction.response.edit_message(
            embed=build_help_embed(page),
            view=self.view,
        )


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(HelpSelect())