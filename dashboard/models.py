from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime as dt
import uuid
from .exceptions import EmailAlreadyUsed
from utils.mailer import EmailHelper
from django.contrib.sites.shortcuts import get_current_site


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # CRM Data
    picture_url = models.TextField(_('picture URL'), max_length=500, null=True, blank=True)
    
    # Reset Password
    reset_token = models.TextField(max_length=200, null=True, blank=True)
    update_token_at = models.DateTimeField(default=None, null=True, blank=True)
    ask_reset_at = models.DateTimeField(default=dt.now, null=True, blank=True)
    
    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
    
    class Meta:
        ordering = ('user',)
    
    @classmethod
    def create(cls, email, first_name, last_name, picture_url):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email,
                                            email=email,
                                            password=User.objects.make_random_password(),
                                            first_name=first_name,
                                            last_name=last_name)
            user.is_active = False
            user.save()

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = cls(user=user)
            profile.picture_url = picture_url
            profile.reset_token = str(uuid.uuid4())
            profile.save()
        if not user.is_active:
            return profile
        raise EmailAlreadyUsed

    @classmethod
    def send_invitation(cls, request, email, full_name):
        try:
            profile = Profile.objects.get(user__email=email)
        except Profile.DoesNotExist:
            return None
        message = 'Welcome! Click this link to create your account ' \
                  'http://{}/reset_password/{}'.format(get_current_site(request), profile.reset_token)
        EmailHelper.send_email(message=message, subject='Welcome to DSP Explorer - Open Maker',
                               receiver_name=full_name, receiver_email=email)
