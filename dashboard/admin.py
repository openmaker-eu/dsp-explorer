from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from .models import Profile, Feedback, Tag, Invitation, Challenge, Company, Interest
from django import forms


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_token')


# class ChallengeAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     list_display_links = ('interested_profiles',)
#
#     def interested_profiles(self, obj):
#         return obj.get_interested()


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)


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


class InterestInline(GenericTabularInline):
    model = Interest
    can_delete = False
    # verbose_name_plural = 'Interests'
    fk_name = 'profile'


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    readonly_fields = ('interested',)
    # inlines = (InterestInline,)

    def interested(self, obj):
        html = '<filedset class="module"><h2>Interested Profiles </h2></br>'
        for profile in obj.get_interested():
            html += '<a href="/admin/dashboard/profile/'+str(profile.pk)+'/">' + profile.user.email + '</p>'
        return html+'</fieldset>'
    interested.allow_tags = True
    interested.short_description = ''



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Company, CompanyAdmin)
# admin.site.register(Feedback, FeedbackAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(Invitation, InvitationAdmin)
