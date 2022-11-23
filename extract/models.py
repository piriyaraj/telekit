from email.policy import default
from django.db import models

# Create your models here.
class Notification(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)
    viewed=models.BooleanField(default=False)
    link=models.ForeignKey("blog.Link",on_delete=models.DO_NOTHING,blank=True, null=True,)

    def __str__(self):
        return f"{self.name}"