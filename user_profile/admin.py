from django.contrib import admin
from .models import Linkpin,User
from django.contrib.auth.admin import UserAdmin

class LinkpinAdmin(admin.ModelAdmin):
    list_display = ['user', 'linkId', 'points', 'days', 'points_per_day', 'added', 'modified']
    search_fields = ['user__username', 'linkId']
    readonly_fields = ['added', 'modified']

admin.site.register(Linkpin, LinkpinAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'verified', 'added', 'modified', 'points', 'verification_id')
    list_filter = ('verified',)
    search_fields = ('username', 'email')
    readonly_fields = ('added', 'modified', 'verification_id')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Custom fields', {'fields': ('verified', 'points', 'added', 'modified', 'verification_id')}),
    )

admin.site.register(User, CustomUserAdmin)