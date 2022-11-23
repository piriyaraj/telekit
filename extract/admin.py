from unittest import result
from django.contrib import admin
from blog.models import Link

from extract.models import Notification
from django.utils.html import format_html
# Register your models here.
# admin.site.register(Notification)

@admin.register(Notification)
class NotiAdmin(admin.ModelAdmin):
    list_display = ("name",'date',"show_average","viewed")
    list_editable=['viewed']
    ordering = ("viewed", "date")
    list_filter = ["viewed"]
    def show_average(self, obj):
        result=Link.objects.get(id=obj.link.id)
        return format_html("<a href='/join/{}' target='_blank'>view</a></br>category: {}<br/>Name: {}</br>Description: {}", result.linkId,result.category,result.name,result.description)

    
    show_average.short_description = "Link"