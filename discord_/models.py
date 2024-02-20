from django.db import models


class IqamaSource(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class MasjidData(models.Model):
    id = models.UUIDField(primary_key=True)
    slug = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    iqama_source = models.ForeignKey(IqamaSource, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_cached = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.slug

    def __repr__(self):
        return f"<MasjidData(id={self.id}, slug={self.slug}, name={self.name}, iqama_source={self.iqama_source}, last_cached={self.last_cached})>"


class Guild(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    discord_id = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Guild(id={self.id}, name={self.name}, discord_id={self.discord_id})>"


class GuildMasjidSettings(models.Model):
    id = models.UUIDField(primary_key=True)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    masjid_data = models.ForeignKey(MasjidData, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=30)
    notifications = models.BooleanField()

    def __str__(self):
        return f"{self.guild} - {self.masjid_data}"

    def __repr__(self):
        return f"<GuildMasjidSettings(id={self.id}, guild={self.guild}, masjid_data={self.masjid_data}, channel_id={self.channel_id}, notifications={self.notifications})>"
