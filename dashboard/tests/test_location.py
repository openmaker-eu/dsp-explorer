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
from itertools import chain
import copy

class ProfileTestCase(TestCase):

    client = Client()
    user = None
    password = '12345678'

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

    # def test1_save_location_new(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should add location')
    #
    #     location = Location.create(**self.location)
    #     location = Location.objects.filter(lat=self.location['lat'], lng=self.location['lng'])
    #
    #     self.assertIsNotNone(location)
    #
    # def test2_save_existing_location(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should upadte existing location')
    #
    #     new_dict = copy.deepcopy(self.location)
    #     new_dict['city'] = 'Test_city'
    #
    #     Location.create(**self.location)
    #     Location.create(**new_dict)
    #     location = Location.objects.filter(lat=self.location['lat'], lng=self.location['lng'])
    #
    #     self.assertEqual(
    #         len(location), 1,
    #         'Save Location with same lat an lng and different name, should update existing location'
    #     )
    #
    # def test3_save_existing_location_same_coord_different_city(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should upadte existing location concatenating new city')
    #
    #     new_dict = copy.deepcopy(self.location)
    #     new_dict['city'] = 'Test_city'
    #
    #     Location.create(**self.location)
    #     location1 = Location.objects.filter(lat=self.location['lat'], lng=self.location['lng'])[0]
    #
    #     Location.create(**new_dict)
    #     location = Location.objects.filter(lat=self.location['lat'], lng=self.location['lng'])
    #
    #     self.assertEqual(
    #         location[0].city_alias,
    #         location1.city_alias+new_dict['city']+',',
    #         'Save Location with same lat an lng and different name, should update existing location adding new alias'
    #     )
    #
    # def test4_save_existing_location_same_coord_same_city(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should not update existing field')
    #
    #     Location.create(**self.location)
    #     location1 = Location.objects.filter(lat=self.location['lat'], lng=self.location['lng'])[0]
    #     Location.create(**self.location)
    #     location = Location.objects.filter(lat=self.location['lat'], lng=self.location['lng'])
    #
    #     self.assertEqual(
    #         location[0].city_alias,
    #         location1.city_alias,
    #         'Save Location with same lat an lng and same name should not update'
    #     )
    #
    def test5_add_location_to_profile(self):
        print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] add location')

        location = Location.create(**self.location)

        self.user.profile.location = location
        self.user.profile.save()

        user = User.objects.filter(email=self.user.email)[0]

        self.assertIsNotNone(user.profile.location)

    def test5_add_same_location_to_profile(self):
        print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] add location')

        location = Location.create(**self.location)

        self.user.profile.location = location
        self.user.profile.save()

        user = User.objects.filter(email=self.user.email)[0]

        self.assertIsNotNone(user.profile.location)

    def test7_save_existing_location_add_country(self):
        print Colorizer.LightPurple('\n[TEST PROFILE LOCATION] assert should add country aliases')

        Location.create(**self.location)

        location = Location.objects.filter(lat=self.location['lat'], lng=self.location['lng'])

        print location[0].country_alias

        self.assertEqual(
            len(location), 1,
            'Save Location with same lat an lng and different name, should update existing location'
        )
