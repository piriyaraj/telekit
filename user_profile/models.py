from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": "The email must be unique"
        }
    )
    links = models.ManyToManyField("blog.Link")
    verified = models.BooleanField(default=False)
    added=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    points = models.IntegerField(default = 1000)
    verification_id = models.CharField(max_length=30,default='aaa')
    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Linkpin(models.Model):
    points = models.FloatField()
    days = models.FloatField()
    points_per_day = models.FloatField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    linkId = models.CharField(max_length=30,unique=True)

class Follow(models.Model):
    followed = models.ForeignKey(
        User,
        related_name='user_followers',
        on_delete=models.CASCADE
    )
    followed_by = models.ForeignKey(
        User,
        related_name='user_follows',
        on_delete=models.CASCADE
    )
    muted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.followed_by.username} started following {self.followed.username}"



