import discord

from views.help_view import HelpView, build_help_embed


def register(bot, guild):
    @bot.tree.command(
        name="help",
        description="Tampilkan panduan Junimo Bot",
        guild=guild,
    )
    async def help_command(
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            embed=build_help_embed("overview"),
            view=HelpView(),
            ephemeral=True,
        )