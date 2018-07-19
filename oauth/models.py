from __future__ import unicode_literals
from dashboard.models import Profile
from django.db import models
import datetime

class Twitter(models.Model):
    app_id = models.CharField(max_length=200)
    app_secret = models.CharField(max_length=200)
    redirect_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.datetime.now)


class TwitterProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.CharField(max_length=200, default='-1')
    access_token = models.CharField(max_length=200)
    secret_access_token = models.CharField(max_length=200)
    token_type = models.CharField(default="Bearer", max_length=30)
    expires_in = models.CharField(max_length=30)

    def __str__(self):
        return "Twitter Profile of %s" % self.profile

    @classmethod
    def create(cls, profile, user_id, access_token, secret_access_token):

        if profile:
            profile.twitter = True
            profile.save()

        twitter_profile = cls(profile=profile)
        twitter_profile.user_id = user_id
        twitter_profile.access_token = access_token
        twitter_profile.secret_access_token = secret_access_token
        twitter_profile.save()
        return twitter_profile
