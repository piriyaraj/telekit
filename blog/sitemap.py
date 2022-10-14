from unittest import result
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Category,Country,Language,Link
from blog.models import Category,Country,Language,Link


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)

class countrySitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    def items(self):
        return Country.objects.all()


class categorySitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    def items(self):
        return Category.objects.all()


class languageSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    def items(self):
        return Language.objects.all()


class linkSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    def items(self):
        return Link.objects.all()
