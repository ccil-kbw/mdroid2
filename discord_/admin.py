from django.contrib import admin

from .models import Guild, GuildMasjidSettings, IqamaSource, MasjidData, IqamaTime
from .serializers import (
    GuildMasjidSettingsSerializer,
    GuildSerializer,
    IqamaSourceSerializer,
    MasjidDataSerializer,
    IqamaTimeSerializer,
)


class IqamaSourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    serializer_class = IqamaSourceSerializer


class MasjidDataAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "name", "iqama_source", "last_cached")
    search_fields = ("slug", "name", "iqama_source__name")


class GuildAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "discord_id")
    search_fields = ("name", "discord_id")


class GuildMasjidSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "guild", "masjid_data", "channel_id", "notifications")
    search_fields = ("guild__name", "masjid_data__slug")


class IqamaTimeAdmin(admin.ModelAdmin):
    list_display = ("masjid_data", "date", "adhan_fajr", "iqama_fajr", "adhan_dhuhr", "iqama_dhuhr", "adhan_asr", "iqama_asr", "adhan_maghrib", "iqama_maghrib", "adhan_isha", "iqama_isha")
    search_fields = ("masjid_data__slug", "iqama_time", "iqama_date")
    ordering = ("date",)


admin.site.register(IqamaSource, IqamaSourceAdmin)
admin.site.register(MasjidData, MasjidDataAdmin)
admin.site.register(Guild, GuildAdmin)
admin.site.register(GuildMasjidSettings, GuildMasjidSettingsAdmin)
admin.site.register(IqamaTime, IqamaTimeAdmin)