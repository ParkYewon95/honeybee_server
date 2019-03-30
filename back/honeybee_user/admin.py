from django.contrib import admin
from .models import HoneyBeeUser

class HoneyBeeUserAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'name',
        'email',
        'introduce',
        'profile_pic',
        'total_like',
        'total_down',
        'is_superuser',
        'is_admin',
        'is_staff',
    ]
    list_display = [
        'id',
        'name',
        'email',
        'unique_id',
    ]

admin.site.register(HoneyBeeUser,HoneyBeeUserAdmin)
