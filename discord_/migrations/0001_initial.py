# Generated by Django 5.0.2 on 2024-02-20 02:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Guild",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
                ("discord_id", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="IqamaSource",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="MasjidData",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("slug", models.CharField(max_length=30, unique=True)),
                ("name", models.CharField(blank=True, max_length=30, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "last_cached",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "iqama_source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="discord_.iqamasource",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GuildMasjidSettings",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("channel_id", models.CharField(max_length=30)),
                ("notifications", models.BooleanField()),
                (
                    "guild",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="discord_.guild"
                    ),
                ),
                (
                    "masjid_data",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="discord_.masjiddata",
                    ),
                ),
            ],
        ),
    ]
