from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from .models import Profile, Feedback, Tag, Invitation, Challenge, Company, Interest
from django import forms
from froala_editor.widgets import FroalaEditor
from django.template import Template, Context
from django.db import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('tags',)
    readonly_fields = (
        'user', 'picture', 'birthdate',
        'gender', 'city', 'occupation', 'twitter_username',
        'tags',
        'statement', 'organization',
        'types_of_innovation',  'size',
        'technical_expertise', 'technical_expertise_other',
        'sector', 'sector_other', 'role', 'role_other',  'socialLinks',
         'source_of_inspiration'

    )
    exclude = ('location', 'social_links', 'reset_token', 'update_token_at', 'ask_reset_at', 'place')
    can_delete = False

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


    list_display = ('title', 'company', 'challenge_picture', 'profile',  )
    readonly_fields = ('interested',)
    # inlines = (InterestInline,)

    def interested(self, obj):
        t = Template(self.template)
        return t.render(Context({'interested': obj.get_interested()}))

    interested.allow_tags = True
    interested.short_description = ''

    formfield_overrides = {
        models.TextField: {'widget': FroalaEditor},
    }

    template = str(
        '<div class="module">'
        '<h2>Interested Profiles</h2></br>'
        '<table style="width:100%">'
        '   <tr style="font-weight:bold;"> '
        '       <td>First Name</td>'
        '       <td>Last Name</td>'
        '       <td>Email</td>'
        '       <td>City</td>'
        '       <td>Details</td>'
        '   </tr>'
        '   {% for profile in interested %}'
        '       <tr>'
        '           <td>{{profile.user.first_name}}</td>'
        '           <td>{{profile.user.last_name}}</td>'
        '           <td>{{profile.user.email}}</td>'
        '           <td>{{profile.city}}</td>'
        '           <td>'
        '               <a href="/admin/dashboard/profile/{{profile.pk}}">'
        '                   <img src="/static/admin/img/icon-changelink.svg" alt="Change">'
        '               </a>'
        '           </td>'
        '       </tr>'
        '   {% endfor %}'
        '</table>'
        '</div>'
    )



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Company, CompanyAdmin)
# admin.site.register(Feedback, FeedbackAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(Invitation, InvitationAdmin)
