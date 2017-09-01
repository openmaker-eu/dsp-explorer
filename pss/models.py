from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from dashboard.models import Profile
from django.utils import timezone

LES_CHOICE = (
    (0, 'Bilbao'),
    (1, 'Italy'),
    (2, 'Bratislava'),
    (3, 'United Kingdom'),
)


def upload_to_and_rename(instance, filename):
    from datetime import datetime as dt
    import os
    filename = dt.now().strftime("%d_%m_%y_%M_%S") + filename
    return os.path.join('application', filename)


class Application(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    les = models.IntegerField(default=0, choices=LES_CHOICE)
    project_name = models.TextField(_('Project Name'), max_length=500, null=False, blank=False)
    zip_location = models.FileField(_('Zip Location'), upload_to=upload_to_and_rename)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ('created_at', )

    def send_email(self):
        # TODO Body Message and template for User and Admins
        self.profile.send_email('Invitation Sent!', 'Thanks for your submission!')
