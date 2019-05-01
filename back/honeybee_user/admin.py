from django.contrib import admin
from .models import HoneyBeeUser,PictureInfo

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

class PictureInfoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'pic_address',
        'owner',
    ]

admin.site.register(HoneyBeeUser,HoneyBeeUserAdmin)
admin.site.register(PictureInfo,PictureInfoAdmin)
