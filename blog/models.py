from django.urls import reverse
from django.core.files import File
from pyexpat import model
from tempfile import NamedTemporaryFile
from unicodedata import category
from unittest.util import _MAX_LENGTH
from urllib.request import urlopen
from django.db import models
from django.utils.text import slugify

from user_profile.models import User



class Country(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=False,unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name    

    def get_absolute_url(self):
        return reverse("country", args=[self.slug])
        # return f'/{self.slug}/'

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

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])
        # return f'/{self.slug}/'

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

    def get_absolute_url(self):
        return reverse("language", args=[self.slug])
        # return f'/{self.slug}/'

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

    def get_absolute_url(self):
        # return reverse("post/", args=[self.slug])
        print(self.slug)
        return f'/{self.slug}/'

    def __str__(self) -> str:
        return self.title

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
    image_file = models.ImageField(upload_to='images')
    published=models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("links", args=[self.linkId])
        # return f'/{self.linkId}/'

    def save(self, *args, **kwargs):
        if self.imgUrl and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.imgUrl).read())
            img_temp.flush()
            self.image_file.save(f"image_{self.linkId}", File(img_temp))
        try:
            super(Link, self).save(*args, **kwargs)
        except:pass
 

    def delete(self, using=None, keep_parents=False):
        # assuming that you use same storage for all files in this model:
        storage = self.image_file.storage
        print("delete called")
        if storage.exists(self.image_file.name):
            storage.delete(self.image_file.name)

        super().delete() 

