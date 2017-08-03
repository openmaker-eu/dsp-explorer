from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from dashboard.models import Profile
from datetime import datetime as dt

LES_CHOICE = (
    (0, 'Lama'),
    (1, 'Topix'),
    (2, 'NoIdea'),
)


class Application(models.Model):
    profile = models.ManyToManyField(Profile)
    les = models.IntegerField(default=0, choices=LES_CHOICE)
    project_name = models.TextField(_('Project Name'), max_length=500, null=False, blank=False)
    zip_location = models.FileField(_('Zip Location'), upload_to='application')
    created_at = models.DateTimeField(default=dt.now, null=True, blank=True)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ('created_at', )
