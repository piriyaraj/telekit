from unicodedata import category
from django.contrib import admin
from django.db.models import Count
from blog.models import Category, Company, Country, Language, Link, Tag

# Register your models here.
admin.site.register(Link)
admin.site.register(Company)
# admin.site.register(Country)
# admin.site.register(Language)
admin.site.register(Tag)
# admin.site.register(Category)


@admin.register(Country)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count']
    def post_count(self, obj):
        return len(Link.objects.filter(country=obj))


@admin.register(Language)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count']

    def post_count(self, obj):
        return len(Link.objects.filter(language=obj))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count']

    def post_count(self, obj):
        return len(Link.objects.filter(category=obj))
