from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from blog.models import Link

class Command(BaseCommand):
    help = 'Change paid status for links older than 30 days'

    def handle(self, *args, **options):
        current_date = timezone.now()
        thirty_days_ago = current_date - timedelta(days=30)
        Link.objects.filter(paidAt__lte=thirty_days_ago).update(paid=False)
        self.stdout.write(self.style.SUCCESS('Successfully updated paid status'))
