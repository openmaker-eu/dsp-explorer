from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.files.storage import FileSystemStorage
from os.path import abspath, dirname
from dashboard.models import Profile
from django.utils import timezone
from django.conf import settings
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, pss_upload_confirmation, pss_admin_upload_confirmation

def upload_to_and_rename(instance, filename):
    from datetime import datetime as dt
    filename = dt.now().strftime("%d_%m_%y_%M_%S") + filename
    return filename


class Application(models.Model):

    les_choices = (
        (0, 'Spain'),
        (1, 'Italy'),
        (2, 'Slovakia'),
        (3, 'United Kingdom'),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    les = models.IntegerField(default=0, choices=les_choices)
    project_name = models.TextField(_('Project Name'), max_length=500, null=False, blank=False)

    zip_location = models.FileField(_('Zip Location'), upload_to=upload_to_and_rename, storage=FileSystemStorage(location=settings.UPLOAD_ROOT), max_length=500)

    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ('created_at', )

    def retrieve_les_label(self, code):

        for les in Application.les_choices:
            if code == les[0]: return les[1]
        return 'less found undefined'

    def send_email(self):

        user = User.objects.get(id=self.profile.user_id)
        applier_first_name = User.objects.get(id=self.profile.user_id).first_name
        applier_last_name = User.objects.get(id=self.profile.user_id).last_name
        latest_project_name_uploaded_by_current_user = Application.objects.filter(profile_id=self.profile.id).order_by('-id')[0].project_name
        latest_les_uploaded_by_current_user = Application.objects.filter(profile_id=self.profile.id).order_by('-id')[0].les

        # user_content_mail = "{}{}{}".format(invitation_base_template_header,
        #                                pss_upload_confirmation.format(
        #                                    FIRST_NAME=applier_first_name,
        #                                    LAST_NAME=applier_last_name),
        #                                invitation_base_template_footer)
        #
        # admin_content_mail = "{}".format(pss_admin_upload_confirmation.format(
        #     APPLIER_FIRST_NAME=applier_first_name,
        #     APPLIER_LAST_NAME=applier_last_name,
        #     APPLICATION_NAME=latest_project_name_uploaded_by_current_user,
        #     LES=self.retrieve_les_label(latest_les_uploaded_by_current_user)
        # ))


        user_content_mail = "{}{}{}".format(invitation_base_template_header,
                                            pss_upload_confirmation,
                                            invitation_base_template_footer)

        admin_content_mail = "{}".format(
            pss_admin_upload_confirmation.format(
                EMAIL=user.email,
                APPLICATION_NAME=latest_project_name_uploaded_by_current_user,
                LES=self.retrieve_les_label(latest_les_uploaded_by_current_user
            )
        ))

        self.profile._send_email('PSS Open Maker application done!', user_content_mail)
        self.profile._send_email('New PSS application', admin_content_mail, 'Admin', settings.EMAIL_ADMIN_1)
        self.profile._send_email('New PSS application', admin_content_mail, 'Admin', settings.EMAIL_ADMIN_2)

