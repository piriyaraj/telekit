from unicodedata import category
from django.contrib import admin
from django.db.models import Count
from blog.models import Category, Company, Country, Language, Link, Tag

# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link','pointsperday', 'country', 'category', 'language', 'noOfMembers', 'published')
    list_filter = ('country', 'category', 'language', 'published')
    search_fields = ('name', 'link', 'description')
    readonly_fields = ('added', 'modified')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'link','pointsperday', 'country', 'category', 'language','mail')
        }),
        ('Additional Information', {
            'fields': ('tag', 'noOfMembers', 'description', 'company', 'type', 'linkId', 'imgUrl', 'image_file')
        }),
        ('Status', {
            'fields': ('published',)
        }),
        ('Timestamps', {
            'fields': ('added', 'modified'),
            'classes': ('collapse',),
        }),
    )

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
