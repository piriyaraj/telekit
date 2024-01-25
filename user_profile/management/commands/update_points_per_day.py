# your_app/management/commands/update_points_per_day.py
from django.core.management.base import BaseCommand
from user_profile.models import Linkpin

class Command(BaseCommand):
    help = 'Update points per day for Linkpin instances'

    def handle(self, *args, **options):
        linkpins = Linkpin.objects.all()
        for linkpin in linkpins:
            linkpin.update_points_per_day()
        self.stdout.write(self.style.SUCCESS('Successfully updated points per day'))
