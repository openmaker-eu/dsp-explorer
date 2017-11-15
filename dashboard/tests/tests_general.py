# coding=utf-8
from django.test import TestCase, Client
from dashboard.models import Profile
import json


class GeneralTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_profile_is_unicode_safe(self):
        print '[UTF-8 ENCODING TEST]'
        Profile.create(
            email='massimo.santoli@top-ix.org',
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
        profile = Profile.objects.filter(pk=1)[0]
        welcome = "Welcome onboard {}!".format(profile.user.first_name.encode('utf-8'))
        self.assertEqual(json.dumps(welcome), json.dumps('Welcome onboard R\xc3\xa9si\xc3\xa9rr!'))
