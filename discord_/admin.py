from django.contrib import admin
from .models import IqamaSource, MasjidData, Guild, GuildMasjidSettings
from .serializers import IqamaSourceSerializer, MasjidDataSerializer, GuildSerializer, GuildMasjidSettingsSerializer


class IqamaSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    serializer_class = IqamaSourceSerializer


class MasjidDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'iqama_source', 'last_cached')
    search_fields = ('slug', 'name', 'iqama_source__name')


class GuildAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'discord_id')
    search_fields = ('name', 'discord_id')


class GuildMasjidSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'guild', 'masjid_data', 'channel_id', 'notifications')
    search_fields = ('guild__name', 'masjid_data__slug')


admin.site.register(IqamaSource, IqamaSourceAdmin)
admin.site.register(MasjidData, MasjidDataAdmin)
admin.site.register(Guild, GuildAdmin)
admin.site.register(GuildMasjidSettings, GuildMasjidSettingsAdmin)
