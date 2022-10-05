from pyexpat import model
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.text import slugify

from user_profile.models import User



class Country(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=False,unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    pass

class Category(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=False,unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    pass

class Language(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=False,unique=True)

    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    pass

class Tag(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=False,unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    pass

class Company(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=1000)
    profile=models.ImageField(upload_to='Company')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=False,unique=True)

    def __str__(self) -> str:
        return self.name    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    pass

linkTypes = (
    ("Group", "Group"),
    ("Channel", "Channel"),
    ("Bot", "Bot"),
    ("Stickers", "Stickers"),
)
# Create your models here.
class Link(models.Model):
    name=models.CharField(max_length=200)
    link=models.CharField(max_length=200)
    country=models.ForeignKey("Country", on_delete=models.DO_NOTHING)
    category=models.ForeignKey("Category", on_delete=models.DO_NOTHING)
    language=models.ForeignKey("Language", on_delete=models.DO_NOTHING)
    tag=models.ManyToManyField(Tag,related_name='tag_blogs',blank=True)
    added=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now_add=True)
    imgUrl=models.URLField(max_length=1000)
    noOfMembers=models.IntegerField()
    description=models.CharField(max_length=1000)
    company=models.ForeignKey("Company",on_delete=models.DO_NOTHING,blank=True, null=True,)
    type=models.CharField(choices=linkTypes,max_length=20)
    linkId=models.CharField(max_length=100)


