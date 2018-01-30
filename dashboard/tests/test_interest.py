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


class ProfileTestCase(TestCase):

    user = None
    password = '12345678'

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
        print Colorizer.LightPurple('\n[TEST CHALLENGE] should return only Challenge interests')

        Challenge.create('test challenge')
        challenge = Challenge.objects.get(title='test challenge')
        self.user.profile.add_interest(challenge)

        self.user.profile.add_interest(self.company)
        interests = self.user.profile.get_interests(Challenge)

        self.assertTrue(all(isinstance(x, Challenge) for x in interests), Colorizer.Red('No Company linked'))


