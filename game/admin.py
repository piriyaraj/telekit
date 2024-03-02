from django.contrib import admin
from .models import Spin

class SpinAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_points', 'last_spin', 'today_spin_count', 'notified_data')
    search_fields = ('user__username',)  # Add any other fields you want to search

    def user_username(self, obj):
        return obj.user.username

    def user_points(self, obj):
        return obj.user.points

    user_username.short_description = 'User Username'
    user_points.short_description = 'User Points'

admin.site.register(Spin, SpinAdmin)

from django.contrib import admin
from .models import ReferralCount, ReferralVisit

@admin.register(ReferralCount)
class ReferralCountAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'added', 'modified')
    list_filter = ('added', 'modified')
    search_fields = ('user__username',)

@admin.register(ReferralVisit)
class ReferralVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip')
    search_fields = ('user__username',)
