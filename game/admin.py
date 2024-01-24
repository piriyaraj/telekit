from django.contrib import admin
from .models import Spin

class SpinAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_spin', 'notified_data')
    search_fields = ('user__username',)  # Add any other fields you want to search

admin.site.register(Spin, SpinAdmin)
