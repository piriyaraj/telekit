from django.db import models
from django.utils import timezone

from user_profile.models import User
from datetime import timedelta

class Spin(models.Model):
    last_spin = models.DateTimeField(default=timezone.now() - timedelta(hours=2))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notified_data = models.DateTimeField(null=True, blank=True)
    today_spin_count = models.IntegerField(default=0)
    
    def can_spin_now(self):
        # Check if at least an hour has passed since the last spin
        elapsed_time = timezone.now() - self.last_spin
        return elapsed_time.total_seconds()

    def notify_user(self):
        # Check if more than 1 day has passed since the last spin
        elapsed_time = timezone.now() - self.last_spin
        if elapsed_time.total_seconds() >= 86400:
            self.notified_data = timezone.now()
            # Add logic to send notification to the user
            # For example, you might use Django signals or a task queue like Celery for asynchronous notification
