from unicodedata import category
from django.contrib import admin

from blog.models import Category, Company, Country, Language, Link, Tag

# Register your models here.
admin.site.register(Link)
admin.site.register(Company)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Tag)
admin.site.register(Category)
