import os
import discord
from discord import app_commands
from discord.app_commands import Choice
from typing import List, Literal, Optional
from discord_.models import MasjidData
from django.core.management.base import BaseCommand


def _token() -> str:
    token = os.getenv("MDROID2_TOKEN")
    if token is None:
        raise ValueError("MDROID2_TOKEN environment variable is required.")

    return token


def _test_guild() -> Optional[discord.Object]:
    test_guild_id = os.getenv("MDROID2_TEST_GUILD_ID", None)
    if test_guild_id:
        print(f"Using test guild: {test_guild_id}")

    return discord.Object(id=test_guild_id) if test_guild_id else None


__test_guild = (
    _test_guild()
)  # Instantiates in the dev and test environments. None otherwise
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(
    name="hey",
    description="Hey there!",
    guild=__test_guild,
)
async def hey(interaction):
    await interaction.response.send_message("Bye!")


# noinspection PyUnresolvedReferences
@tree.command(
    name="add_masjid",
    description="Add a masjid!",
    guild=__test_guild,
)
@app_commands.choices(
    masjids=[
        Choice(name=m[0], value=str(m[1]))
        for m in MasjidData.objects.all().values_list("name", "id")
    ]
)
async def add_masjid(
    interaction: discord.interactions.Interaction, masjids: Choice[str]
):
    try:
        await interaction.response.send_message(
            f"Configuring {masjids.name} for the Server... Please wait..."
        )

        await interaction.response.send_message(
            f"{interaction.user.name} added {masjids.name} to the Server. "
            f"Notifications will be sent to the default channel!"
        )
    except discord.errors.Forbidden:
        await interaction.response.send_message(
            "I don't have permission to create a category! See documentation for more info."
        )


@client.event
async def on_ready():
    await tree.sync(guild=__test_guild)
    print("Ready!")


class Command(BaseCommand):
    help = "Run the Discord Bot"

    def handle(self, *args, **options):
        client.run(_token())
