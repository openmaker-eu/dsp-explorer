# coding=utf-8
from django.test import TestCase, Client
from utils import testhelpers
from dashboard.models import Profile
import json
from dashboard.models import Profile, User, SourceOfInspiration, Tag, Challenge, Interest, Company
from django.shortcuts import render, reverse
from utils.Colorizer import Colorizer
import datetime
import pytz
from django.utils import timezone


class InterestTestCase(TestCase):

    user = None

    @classmethod
    def setUpTestData(cls):
        user = testhelpers.create_test_user()
        cls.user = User.objects.get(email=user.email)
        company = Company(name='Top-IX').save()
        cls.company = Company.objects.get(name='Top-IX')

    def test1_create_challenge(self):
        print Colorizer.LightPurple('\n[TEST CHALLENGE] should create an interest(challenge)')
        Challenge.create('test challenge')
        self.assertTrue(Challenge.objects.get(title='test challenge'), Colorizer.Red('Create Challenge Error'))

    def test2_profile_interest_in_challenge(self):
        print Colorizer.LightPurple('\n[TEST CHALLENGE] should link an interest(Challenge)')

        Challenge.create('test challenge')
        challenge = Challenge.objects.get(title='test challenge')

        self.user.profile.add_interest(challenge)
        interests = self.user.profile.get_interests()

        self.assertGreater(len(interests), 0, Colorizer.Red('No Challenge linked'))

    def test3_profile_interest_in_company(self):
        print Colorizer.LightPurple('\n[TEST CHALLENGE] should link an interest(Company)')

        self.user.profile.add_interest(self.company)
        interests = self.user.profile.get_interests()

        self.assertGreater(len(interests), 0, Colorizer.Red('No Company linked'))

    def test4_profile_filter_interest_challenge(self):
        print Colorizer.LightPurple('\n[TEST CHALLENGE] should return only interests that are Challenges')

        Challenge.create('test challenge')
        challenge = Challenge.objects.get(title='test challenge')
        self.user.profile.add_interest(challenge)

        self.user.profile.add_interest(self.company)
        interests = self.user.profile.get_interests(Challenge)

        self.assertTrue(all(isinstance(x, Challenge) for x in interests), Colorizer.Red('Filter interest does not return a list of challenge'))

    def test5_get_interested_from_challenge(self):
        print Colorizer.LightPurple('\n[TEST CHALLENGE] should return a list of profile interested in a challenge')

        Challenge.create('test challenge')
        challenge = Challenge.objects.get(title='test challenge')
        self.user.profile.add_interest(challenge)

        profiles = challenge.interested()

        self.assertTrue(all(isinstance(x, Profile) for x in profiles), Colorizer.Red('Challenge related interest are not a porofile list'))

    def test6_delete_interest_from_profile(self):
        print Colorizer.LightPurple('\n[TEST CHALLENGE] should should delete interest(challenge) from profile')

        Challenge.create('test challenge')
        challenge = Challenge.objects.get(title='test challenge')
        self.user.profile.add_interest(challenge)

        self.user.profile.delete_interest(Challenge, challenge.id)
        challenges = self.user.profile.get_interests(Challenge)

        self.assertEqual(len(challenges), 0, Colorizer.Red('User interest(challenge) is not deleted'))




