# coding=utf-8
from django.test import TestCase
from models import User, Profile
import json

class AuthTestCase(TestCase):
    def setUp(self):
        Profile.create(
            email='testcase@top-ix.org',
            first_name='Résiérr',
            last_name='Test',
            picture='',
            password='q1w2e3r4',
            gender=1,
            birthdate=None,
            city=None,
            occupation=None,
            twitter_username=None,
            place=None
        )

    def test_profile_is_unicode_safe(self):
        profile = Profile.objects.filter(pk=1)[0]
        print 'profile'
        print profile.user

        # welcome = "Welcome onboard %{name}s!".format(name=profile.user.first_name.encode('utf-8')),
        welcome = "Welcome onboard {}!".format(profile.user.first_name.encode('utf-8'))
        print welcome

        self.assertEqual(json.dumps(welcome), json.dumps('Welcome onboard R\xc3\xa9si\xc3\xa9rr!'))
