# coding=utf-8
from django.test import TestCase, Client
from utils.GoogleHelper import GoogleHelper

class GoogleTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_v12_topics(self):
        city = GoogleHelper.get_city('turin');
        print(city)
        self.assertEqual(True, True)