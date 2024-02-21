import time

import discord
import schedule
from django.core.management.base import BaseCommand

from discord_.models import GuildMasjidSettings

from .helpers import _test_guild


def something(url):
    print(url)


def daily_schedules():
    guild_settings = GuildMasjidSettings.objects.all()
    for guild_setting in guild_settings:
        schedule.every(10).seconds.do(
            something, url=guild_setting.masjid_data.iqama_source_location
        )


class Command(BaseCommand):
    help = "Run the Discord Bot"

    def handle(self, *args, **options):
        __test_guild = (
            _test_guild()
        )  # Instantiates in the dev and test environments. None otherwise
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        for c in client.get_all_channels():
            print(c.name, c.guild)

        schedule.every(10).seconds.do(something, url="mock")
        daily_schedules()
        while True:
            schedule.run_pending()
            time.sleep(1)
