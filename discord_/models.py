import uuid

from asgiref.sync import sync_to_async
from django.db import models
import requests
from datetime import datetime

from django.utils import timezone

class IqamaSource(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class MasjidData(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    slug = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    iqama_source = models.ForeignKey(IqamaSource, on_delete=models.CASCADE)
    iqama_source_location = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_cached = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.slug

    def __repr__(self):
        return f"<MasjidData(id={self.id}, slug={self.slug}, name={self.name}, iqama_source={self.iqama_source}, last_cached={self.last_cached})>"

    def update_iqama_cache(self):
        import csv
        from io import StringIO
        resp = requests.get(self.iqama_source_location)
        iqama_data = csv.reader(resp.text.splitlines(), delimiter=",")
        headers = next(iqama_data)

        def build_time_stamp(date, time) -> datetime.time:
            try:
                return datetime.strptime(f"{date} {time}", "%m/%d/%Y %I:%M %p").time()
            except ValueError as e:
                print(f"ValueError parsing '{date} {time}'. Does not match format '%m/%d/%Y %I:%M %p'")

        for iqama_data_line in iqama_data:
            print(iqama_data_line)
            IqamaTime.objects.update_or_create(
                masjid_data=self,
                date=datetime.strptime(iqama_data_line[0], "%m/%d/%Y").date(),
                defaults={
                    "adhan_fajr": build_time_stamp(iqama_data_line[0], iqama_data_line[2]),
                    "iqama_fajr": build_time_stamp(iqama_data_line[0], iqama_data_line[3]),
                    "adhan_dhuhr": build_time_stamp(iqama_data_line[0], iqama_data_line[5]),
                    "iqama_dhuhr": build_time_stamp(iqama_data_line[0], iqama_data_line[6]),
                    "adhan_asr": build_time_stamp(iqama_data_line[0], iqama_data_line[7]),
                    "iqama_asr": build_time_stamp(iqama_data_line[0], iqama_data_line[8]),
                    "adhan_maghrib": build_time_stamp(iqama_data_line[0], iqama_data_line[9]),
                    "iqama_maghrib": build_time_stamp(iqama_data_line[0], iqama_data_line[10]),
                    "adhan_isha": build_time_stamp(iqama_data_line[0], iqama_data_line[11]),
                    "iqama_isha": build_time_stamp(iqama_data_line[0], iqama_data_line[12]),
                },
            )

        self.last_cached = timezone.now()
        self.save(
            update_fields=["last_cached"]
        )


class Guild(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30, unique=True)
    discord_id = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Guild(id={self.id}, name={self.name}, discord_id={self.discord_id})>"


class GuildMasjidSettings(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    masjid_data = models.ForeignKey(MasjidData, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=30)
    notifications = models.BooleanField()

    class Meta:
        unique_together = ["guild", "masjid_data"]

    def __str__(self):
        return f"{self.guild} - {self.masjid_data}"

    def __repr__(self):
        return f"<GuildMasjidSettings(id={self.id}, guild={self.guild}, masjid_data={self.masjid_data}, channel_id={self.channel_id}, notifications={self.notifications})>"


@sync_to_async
def save_guild_masjid_settings(
    masjid_id: str, guild_discord_id: str, guild_discord_name: str
) -> GuildMasjidSettings:
    guilds = Guild.objects.filter(discord_id=guild_discord_id)
    if guilds.exists():
        guild = guilds.first()
    else:
        guild = Guild.objects.create(
            name=guild_discord_name, discord_id=guild_discord_id
        )

    settings = GuildMasjidSettings.objects.create(
        guild=guild,
        masjid_data=MasjidData.objects.get(id=masjid_id),
        channel_id="",
        notifications=False,
    )

    return settings


class IqamaTime(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    masjid_data = models.ForeignKey(MasjidData, on_delete=models.CASCADE)
    date = models.DateField()
    adhan_fajr = models.TimeField()
    iqama_fajr = models.TimeField()
    adhan_dhuhr = models.TimeField()
    iqama_dhuhr = models.TimeField()
    adhan_asr = models.TimeField()
    iqama_asr = models.TimeField()
    adhan_maghrib = models.TimeField()
    iqama_maghrib = models.TimeField()
    adhan_isha = models.TimeField()
    iqama_isha = models.TimeField()

    class Meta:
        unique_together = ["masjid_data", "date"]


def get_masjid_data(masjid_id: str) -> MasjidData:
    return MasjidData.objects.get(id=masjid_id)


def get_masjid_settings_by_guild_id(guild_id: str) -> list[GuildMasjidSettings]:
    return list(GuildMasjidSettings.objects.filter(guild__discord_id=guild_id))