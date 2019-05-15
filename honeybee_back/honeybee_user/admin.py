from django.contrib import admin
from .models import HoneyBeeUser,PictureInfo

class HoneyBeeUserAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'unique_id',
    ]

admin.site.register(HoneyBeeUser,HoneyBeeUserAdmin)
admin.site.register(PictureInfo)
# Register your models here.
