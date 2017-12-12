# -*- coding: utf-8 -*-
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
from opendataconnector.odconnector import OpenDataConnector

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

    def test1_api_response(self):
        print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should respond correctly')

        latlng = self.user.profile.location.lat+','+self.user.profile.location.lng
        response = OpenDataConnector.get_by_latlng(latlng)

        self.assertLessEqual(
            response.status_code,
            202,
            Colorizer.Red('Update Response Error: \n code: %s \n Info : %s' % (response.status_code, response))
        )

    def test2_get_alternate_city_names(self):
        print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should respond')

        latlng = self.user.profile.location.lat+','+self.user.profile.location.lng
        response = OpenDataConnector.get_city_alternate_name_by_latlng(latlng)

        self.assertIsNotNone(
            response,
            Colorizer.Red('City alternate names is not present on response')
        )
