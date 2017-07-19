from django.contrib import admin
from .models import Profile, Feedback


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_token')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'message_text', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'title')

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Profile, ProfileAdmin)
