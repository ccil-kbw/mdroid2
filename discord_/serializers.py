from .models import IqamaSource, MasjidData, Guild, GuildMasjidSettings
from rest_framework import serializers


class IqamaSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IqamaSource
        fields = "__all__"


class MasjidDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasjidData
        fields = "__all__"


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = "__all__"


class GuildMasjidSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuildMasjidSettings
        fields = "__all__"
