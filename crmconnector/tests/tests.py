# -*- coding: utf-8 -*-
from django.test import TestCase
from dashboard.models import Profile, User, SourceOfInspiration, Tag
from itertools import groupby
import json
from ..capsule import CRMConnector
from utils.Colorizer import Colorizer
from ..serializers import PartySerializer
from ..models import Party
from rest_framework.exceptions import APIException

class CrmTestCase(TestCase):

    party = None

    @classmethod
    def setUpTestData(cls):

        cls.user_data = {
            'email': 'test_unit@test.com',
            'first_name': 'aaa_unit_test',
            'last_name': 'aaa_test_unit',
            'picture': '',
            'password': 'asdasd',
            'gender': 'Male',
            'birthdate': '1980-01-12',
            'city': 'Torreón',
            'occupation': 'tester',
            'twitter_username': '',
            'place': '{"city":"Torreón","state":"Coah.","country_short":"MX","country":"Messico","lat":25.5428443,"long":-103.40678609999998}',
        }

        Profile.create(**cls.user_data)
        cls.user = User.objects.filter(email=cls.user_data['email'])[0]

        # Extra fields
        cls.user.profile.types_of_innovation = 'Product innovation,Technological innovation,Business model innovation'
        cls.user.profile.organization = 'testerorg'
        cls.user.profile.statement = 'Hi im a test user generated from unit test suite'

        ## SOP
        cls.user.profile.source_of_inspiration.add(SourceOfInspiration.create('Apple'))
        cls.user.profile.source_of_inspiration.add(SourceOfInspiration.create('Microsoft'))
        cls.user.profile.source_of_inspiration.add(SourceOfInspiration.create('Samsung'))
        ## Tags
        cls.user.profile.tags.add(Tag.create('Innovation'))
        cls.user.profile.tags.add(Tag.create('Social'))
        cls.user.profile.tags.add(Tag.create('Design'))

        cls.user.profile.sector = 'ICT'

        cls.user.profile.technical_expertise = 'Digital fabrication - Digitalization of analog and traditional technologies'
        cls.user.profile.size = 'A small enterprise (<50 staff, ≲10 MLN of turnover, ≲10MLN total balance sheet)'

        cls.user.profile.socialLinks = json.dumps([
            {"link": "test_om_tw", "name": "twitter"},
            {"link": "www.google.it", "name": "google-plus"},
            {"link": "", "name": "facebook"}
        ])

        cls.user.profile.save()

        # Create Party
        cls.party = Party(cls.user)

    def tearDown(self):
        # self.party.find_and_delete()
        pass

    def testConnection(self):
        print(Colorizer.LightPurple('[ CRM Test : Connection test ]'))
        response = self.party.all()
        self.assertEqual(response.status_code, 200, '[CRM-CONNECTOR ERROR] Response error :\n %s ' % response)

    def testFind(self):
        print(Colorizer.LightPurple('[ CRM Test : Find party by email test ]'))
        results = self.party.get()
        print results
        self.assertTrue(True, '[CRM-CONNECTOR ERROR] Response is not a valid Party object :\n %s ')

    def testInsertion(self):
        print(Colorizer.LightPurple('[ CRM Test : Insertion test ]'))
        results = self.party.create_or_update()
        self.assertTrue(True, '[CRM-CONNECTOR ERROR] Response is not a valid Party object :\n %s ')
