from django.contrib import admin
from .models import Profile, Feedback, Tag, Invitation


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_token')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'message_text', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'title')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'sender_email', 'sender_verified', 'created_at')
    search_fields = ('profile', 'sender_email')

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Invitation, InvitationAdmin)
