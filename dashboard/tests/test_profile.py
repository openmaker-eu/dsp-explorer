# coding=utf-8
from django.test import TestCase, Client
from utils import testhelpers
from dashboard.models import Profile
import json
from dashboard.models import Profile, User, SourceOfInspiration, Tag
from django.shortcuts import render, reverse
from utils.Colorizer import Colorizer
import datetime
import pytz
from django.utils import timezone


class ProfileTestCase(TestCase):

    client = Client()
    user = None
    password = '12345678'

    @classmethod
    def setUpTestData(cls):
        user = testhelpers.create_test_user()
        cls.user = User.objects.filter(email=user.email)[0]

    def test1_login(self):
        print Colorizer.LightPurple('\n[TEST PROFILE PAGE] test login')
        self.assertTrue(self.client.login(username=self.user.username, password=self.password), Colorizer.Red('Error during login'))

    def test2_response(self):
        print Colorizer.LightPurple('\n[TEST PROFILE PAGE] test response success')
        response = self.get_profile_page()
        self.assertLessEqual(
            response.status_code,
            202,
            Colorizer.Red('Response Error: \n code: %s \n Info : %s' % (response.status_code, response))
        )

    def test3_is_profile_page(self):
        print Colorizer.LightPurple('\n[TEST PROFILE PAGE] assert response is a profile page')
        response = self.get_profile_page()
        self.assertEqual(
            response.request['PATH_INFO'],
            '/profile/%s/' % self.user.profile.pk,
            Colorizer.Red('Response is not the profile page but : %s' % response.request['PATH_INFO'])
        )

    def test4_data_is_user_object(self):
        print Colorizer.LightPurple('\n[TEST PROFILE PAGE] assert response user is an user object')
        response = self.get_profile_page()
        self.assertTrue(isinstance(response.context['user'], User), 'Response User data is not an User instance')

    def test5_data_is_the_test_user(self):
        print Colorizer.LightPurple('\n[TEST PROFILE PAGE] assert response user is the test user')
        response = self.get_profile_page()
        # @TODO : now tests only by equality of the string method output of the 2 objects. Need to test also user data
        self.assertEqual(response.context['user'], self.user, 'Response User data is not an User instance')

    @classmethod
    def login(cls):
        return cls.client.login(username=cls.user.username, password=cls.password)

    @classmethod
    def get_profile_page(cls):
        cls.login()
        return cls.client.get('/profile/%s/' % cls.user.profile.pk, follow=True)
