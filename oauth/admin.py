from django.contrib import admin
from .models import Twitter, TwitterProfile

class TwitterAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'app_secret', 'redirect_url', 'created_at')


class TwitterProfileAdmin(admin.ModelAdmin):
    list_display = ('profile', 'access_token', 'secret_access_token', 'expires_in')

admin.site.register(Twitter, TwitterAdmin)
admin.site.register(TwitterProfile, TwitterProfileAdmin)
