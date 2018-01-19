# coding=utf-8
from django.test import TestCase, Client
from utils import testhelpers
from dashboard.models import Profile
import json
from dashboard.models import Profile, User, SourceOfInspiration, Tag, Location
from django.shortcuts import render, reverse
from utils.Colorizer import Colorizer
import datetime
import pytz
from django.utils import timezone
import copy
from restcountriesconnector.rcconnector import RestCountriesConnector

class ConnectorTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = testhelpers.create_test_user()
        cls.user = User.objects.filter(email=user.email)[0]
        cls.location = {
            "city": "Torino",
            "state": "Piemonte",
            "country_short": "IT",
            "country": "Italia",
            "lat": '45.07031200000001',
            "lng": '7.686856499999976'
        }
        location = Location.create(**cls.location)
        cls.user.profile.location = location
        cls.user.profile.save()
        cls.user = User.objects.filter(email=user.email)[0]

    # def test1_api_response(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should respond correctly')
    #
    #     response = RestCountriesConnector.get_city_alias(self.location['country'])
    #
    #     self.assertIsNotNone(
    #         response, Colorizer.Red('Wrong response from Opencity Connector API')
    #     )

    def test1_add_country_aliases(self):
        print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should add country aliases if doesnt exist')

        # response = RestCountriesConnector.get_city_alias(self.location['country'])

        print 'country aliases'
        print self.user.profile.location.country_alias

        self.assertIsNotNone(
            None,
            Colorizer.Red('City alternate names is not present on response')
        )
