from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.files.storage import FileSystemStorage
from dashboard.models import Profile
from django.utils import timezone
from django.conf import settings
from utils.mailer import EmailHelper


def upload_to_and_rename(instance, filename):
    les = filter(lambda x: x[0] == instance.les, instance.les_choices)[0]
    from datetime import datetime as dt
    filename = les[1][0:3] + '_' + dt.now().strftime("%d_%m_%y_%M_%S") + filename
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

        p_user = Profile.objects.get(user__id=self.profile.user_id)
        applier_first_name = p_user.user.first_name
        applier_last_name = p_user.user.last_name
        latest_project_name_uploaded_by_current_user = Application.objects.filter(profile_id=self.profile.id).order_by('-id')[0].project_name
        latest_les_uploaded_by_current_user = Application.objects.filter(profile_id=self.profile.id).order_by('-id')[0].les

        EmailHelper.email(
            template_name='pss_upload_confirmation',
            title='DSPExplorer - Open Maker - Application done!',
            vars={
                'FIRST_NAME': applier_first_name,
                'LAST_NAME': applier_last_name
            },
            receiver_email=p_user.user.email
        )

        admins = settings.EMAIL_ADMIN_LIST

        for admin in admins:
            EmailHelper.email(
                template_name='pss_admin_upload_confirmation',
                title='New PSS application',
                vars={
                    'APPLIER_FIRST_NAME': applier_first_name,
                    'APPLIER_LAST_NAME': applier_last_name,
                    'APPLICATION_NAME': latest_project_name_uploaded_by_current_user,
                    'LES': self.retrieve_les_label(latest_les_uploaded_by_current_user)
                },
                receiver_email=admin
            )
