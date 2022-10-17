from unittest import result
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Category,Country,Language,Link
from blog.models import Category,Country,Language,Link

def printHtml(obj):
    for i in list(obj):
        tag = "<a href='link' title='descri'>title</a>"
        tag=tag.replace("title",i.name).replace("link","/category/"+i.slug).replace('descri',i.name+" telegram invite links")
        print(tag)

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
