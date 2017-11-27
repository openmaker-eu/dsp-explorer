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
from itertools import chain

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

    def test6_save_data_response(self):
        print Colorizer.LightPurple('\n[TEST PROFILE PAGE] check update with valid data')
        response = self.post_profile(None)
        self.assertLessEqual(
            response.status_code,
            202,
            Colorizer.Red('Update Response Error: \n code: %s \n Info : %s' % (response.status_code, response))
        )

    def test7_save_data_errors(self):
        print Colorizer.LightPurple('\n[TEST PROFILE PAGE] check update with valid data')
        response = self.post_profile(None)
        update_errors = filter(lambda x: x.level >= 40, list(response.context['messages']))
        self.assertFalse(
            len(update_errors),
            Colorizer.Red('Update profile errors: %s' % '\n'.join(d.message for d in update_errors))
        )

    @classmethod
    def login(cls):
        return cls.client.login(username=cls.user.username, password=cls.password)

    @classmethod
    def get_profile_page(cls):
        cls.login()
        return cls.client.get('/profile/%s/' % cls.user.profile.pk, follow=True)

    @classmethod
    def post_profile(cls, data):
        cls.login()
        # @TODO: this not send vaid data
        data = dict(chain(cls.user.__dict__.iteritems(), cls.user.profile.__dict__.iteritems()))
        data['birthdate'] = '1983/05/14'
        return cls.client.post('/profile/%s/' % cls.user.profile.pk, data, follow=True)


