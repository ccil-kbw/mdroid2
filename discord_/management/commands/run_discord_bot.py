import datetime
import os
from typing import Optional

import discord
from asgiref.sync import sync_to_async
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import tasks
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import asyncio

from discord_.models import MasjidData, get_masjid_data, save_guild_masjid_settings, get_masjid_settings_by_guild_id

from .helpers import _test_guild


def _token() -> str:
    token = os.getenv("MDROID2_TOKEN")
    if token is None:
        raise ValueError("MDROID2_TOKEN environment variable is required.")

    return token


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
        await save_guild_masjid_settings(
            masjid_id=masjids.value,
            guild_discord_id=interaction.guild_id,
            guild_discord_name=interaction.guild.name,
        )
        await interaction.response.send_message(
            f"Configuring {masjids.name} for the Server... Please wait..."
        )

    except discord.errors.Forbidden:
        await interaction.response.send_message(
            "I don't have permission to create a category! See documentation for more info."
        )
    except IntegrityError:
        await interaction.response.send_message(
            "This masjid is already configured for this server."
        )


@tree.command(
    name="masjid_data",
    description="Get Data about a Masjid!",
    guild=__test_guild,
)
@app_commands.choices(
    masjids=[
        Choice(name=m[0], value=str(m[1]))
        for m in MasjidData.objects.all().values_list("name", "id")
    ]
)
async def masjid_data(
        interaction: discord.interactions.Interaction, masjids: Choice[str]
):
    m_ = await sync_to_async(get_masjid_data, thread_sensitive=True)(masjids.value)
    embed = discord.Embed(
        title=m_.name,
        color=0x000,
        url=m_.iqama_source_location,
    )
    embed.add_field(name="Iqama Source", value=m_.iqama_source_location)
    embed.add_field(name="Website", value="Coming Soon!")
    embed.set_author(name="Masjid's Droid", url="https://github.com/seraftech/mdroid")
    embed.set_footer(
        text=f"Created at: {m_.created_at}\nLast Cached: {m_.last_cached}\nUUID: {m_.id}"
    )
    embed.set_image(
        url="https://seraf.dev/content/images/size/w960/2023/07/fares"
            "____Desert_with_mountains_in_the_background_Mosque_far_awa_"
            "9b993835-e270-422a-8c9c-f6a3221954a1-5824x3264-upscaled.png"
    )

    await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():
    await tree.sync(guild=__test_guild)
    print("Ready!")


@tasks.loop(time=datetime.time(8, 12, 0), count=1)
async def notify(channel: discord.TextChannel):
    masjid_notifications = await sync_to_async(get_masjid_settings_by_guild_id, thread_sensitive=True)(
        channel.guild.id
    )
    print(datetime.datetime.now())
    for masjid_notification in masjid_notifications:
        masjid = await sync_to_async(get_masjid_data, thread_sensitive=True)(
            masjid_notification.masjid_data_id
        )
        print(masjid.name, masjid.iqama_source_location)
        await channel.send(
            f"Hello! {channel.guild.name} is online! {masjid.name} is online!"
        )


@client.event
async def on_ready():
    if not notify.is_running():
        channel = await client.fetch_channel(1207112286515236975)
        notify.start(channel)


@tasks.loop(hours=24)
async def update_notification_times():
    # Update the notification_times list here
    pass


@update_notification_times.before_loop
async def before_update_notification_times():
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now + datetime.timedelta(days=1), datetime.time(0, 0))
    delta = midnight - now
    await asyncio.sleep(delta.seconds)


@task.loop(seconds=60)
async def send_notifications(channel: discord.TextChannel):
    now = datetime.datetime.utcnow().time()

    if any(now.replace(second=0, microsecond=0) == time for time in daily_iqama()):
        await channel.send("PRAYER TIME!")

class Command(BaseCommand):
    help = "Run the Discord Bot"

    def handle(self, *args, **options):
        client.run(_token())
