from unittest import result
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Category,Country,Language,Link
from blog.models import Category,Country,Language,Link


class countrySitemap(Sitemap):
    def items(self):
        return Country.objects.all()


class categorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()


class languageSitemap(Sitemap):
    def items(self):
        return Language.objects.all()


class linkSitemap(Sitemap):
    def items(self):
        return Link.objects.all()
