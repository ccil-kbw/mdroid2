# Generated by Django 5.0.2 on 2024-02-21 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("discord_", "0003_alter_guildmasjidsettings_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="masjiddata",
            name="iqama_source_location",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
