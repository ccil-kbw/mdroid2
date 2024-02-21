from django.core.management.base import BaseCommand
from discord_.models import MasjidData, IqamaTime

class Command(BaseCommand):
    help = "Update the Iqama cache"

    def handle(self, *args, **options):
        masjids = MasjidData.objects.all()
        for masjid in masjids:
            masjid.update_iqama_cache()
            print(f"Updated cache for {masjid.name}")
        print("Cache updated")
