from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture_url', 'reset_token')
    
admin.site.register(Profile, ProfileAdmin)
