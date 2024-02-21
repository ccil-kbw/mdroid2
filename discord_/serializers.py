from rest_framework import serializers

from .models import Guild, GuildMasjidSettings, IqamaSource, MasjidData, IqamaTime


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


class IqamaTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IqamaTime
        fields = "__all__"
