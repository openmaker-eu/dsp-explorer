from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from .models import Profile, Feedback, Tag, Invitation, Challenge, Company, Interest
from django import forms
from froala_editor.widgets import FroalaEditor
from django.template import Template, Context
from django.db import models
from dashboard.serializer import ChallengeSerializer
from django_select2.forms import Select2MultipleWidget, Select2TagWidget, ModelSelect2TagWidget
from django.utils.encoding import force_text


# class OmTagWidget(ModelSelect2TagWidget):
#
#     model = Tag
#     queryset = Tag.objects.all()
#     search_fields = ('name', 'pk__startswith')
#
#     def create_value(self, value):
#         self.get_queryset().create(name=value)
#
#     def value_from_datadict(self, data, files, name):
#         values = super(OmTagWidget, self).value_from_datadict(data, files, name)
#         qs = self.queryset.filter(**{'pk__in': [l for l in values if isinstance(l, int)]})
#         names = [k.name for k in self.queryset.filter(**{'name__in': values})]
#         pks = set(force_text(getattr(o, 'pk')) for o in qs)
#         cleaned_values = []
#         for val in values:
#             if force_text(val) not in pks and force_text(val) not in names:
#                 val = self.queryset.create(name=val).pk
#             cleaned_values.append(val)
#         return cleaned_values


# class MyWidget(Select2TagWidget):
#
#     def value_from_datadict(self, data, files, name):
#         values = super(MyWidget, self).value_from_datadict(data, files, name)
#         return ",".join(values)
    # def optgroups(self, name, value, attrs=None):
    #     values = value[0].split(',') if value[0] else []
    #     selected = set(values)
    #     subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
    #     return [(None, subgroup, 0)]


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
         'source_of_inspiration', 'challenge',
    )
    exclude = ('location', 'social_links', 'reset_token', 'update_token_at', 'ask_reset_at', 'place')
    can_delete = False

    formfield_overrides = {
        models.ManyToManyField: {'widget': Select2MultipleWidget}
    }

    def challenge(self, obj):
        t = Template(self.template)
        return t.render(Context({'challenges': obj.get_interests(Challenge)}))
    challenge.allow_tags = True
    challenge.short_description = ''

    template = str(
        '<div class="module">'
        '<h2>Interested Challenges</h2></br>'
        '<table style="width:100%">'
        '   <tr style="font-weight:bold;"> '
        '       <td>Title</td>'
        '       <td>Details</td>'
        '   </tr>'
        '   {% for challenge in challenges %}'
        '       <tr>'
        '           <td>{{challenge.title}}</td>'
        '           <td>'
        '               <a href="/admin/dashboard/challenge/{{challenge.pk}}">'
        '                   <img src="/static/admin/img/icon-changelink.svg" alt="Change">'
        '               </a>'
        '           </td>'
        '       </tr>'
        '   {% endfor %}'
        '</table>'
        '   <style>.challenge label{display:none;}</style>'
        '</div>')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')
    readonly_fields = ('campany_challenges',)

    formfield_overrides = {
        models.TextField: {'widget': FroalaEditor},
        models.ManyToManyField: {'widget': Select2MultipleWidget}
    }

    def campany_challenges(self, obj):
        t = Template(self.template)
        print
        return t.render(Context({'challenges': ChallengeSerializer(obj.challenges, many=True).data}))
    campany_challenges.allow_tags = True
    campany_challenges.short_description = ''

    template = str(
        '<div class="module">'
        '<h2>Challenges</h2></br>'
        '<table style="width:100%">'
        '   <tr style="font-weight:bold;"> '
        '       <td>Title</td>'
        '       <td>Details</td>'
        '   </tr>'
        '   {% for challenge in challenges %}'
        '       <tr>'
        '           <td>{{challenge.title}}</td>'
        '           <td>'
        '               <a href="/admin/dashboard/challenge/{{challenge.id}}">'
        '                   <img src="/static/admin/img/icon-changelink.svg" alt="Change">'
        '               </a>'
        '           </td>'
        '       </tr>'
        '   {% endfor %}'
        '</table>'
        '   <style>.campany_challenges label, .field-campany_challenges label{display:none;} .readonly{margin-left:0!important;} </style>'
        '</div>')


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
    fk_name = 'profile'


class ChallengeAdmin(admin.ModelAdmin):

    readonly_fields = ('interested',)

    def interested(self, obj):
        t = Template(self.template)
        return t.render(Context({'interested': obj.interested()}))

    interested.allow_tags = True
    interested.short_description = ''

    fieldsets = (
        ('Base info', {
            'fields': ('company', 'title', 'description', 'picture', 'details', 'tags', 'les',),
        }),
        ('Email', {
            'fields': ('coordinator_email', 'notify_admin', 'notify_user',),
        }),
        ('Status', {
            'fields': ('start_date', 'end_date', 'published', 'closed', 'restricted_to'),
        }),
        ('Interested Profiles', {
            'fields': ('interested',),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': FroalaEditor},
        models.ManyToManyField: {'widget': Select2MultipleWidget}
    }

    template = str(
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
        '   <style>.field-interested label, .field-interested_challenges label{display:none;} .readonly{margin-left:0!important;}</style>'
        '</table>'
    )

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Company, CompanyAdmin)


# admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Invitation, InvitationAdmin)
