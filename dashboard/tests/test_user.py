# coding=utf-8
from django.test import TestCase, Client
from utils import testhelpers
from dashboard.models import Profile, User
from utils.Colorizer import Colorizer


class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = testhelpers.create_test_user()
        cls.user = User.objects.get(email=user.email)

    def test1_create(self):
        print Colorizer.LightPurple('\n[TEST USER] should not create user if already exist')

        user = User.create(email=self.user.email)
        self.assertFalse(user, Colorizer.Red('Error during user creation'))

    def test2_create(self):
        print Colorizer.LightPurple('\n[TEST USER] should create user if not exist')

        user = User.create(email='arandomemail@gmail.com')
        self.assertTrue(user, Colorizer.Red('Error during user creation'))




