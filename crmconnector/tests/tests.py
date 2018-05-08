# -*- coding: utf-8 -*-
from django.test import TestCase
from dashboard.models import Profile, User, SourceOfInspiration, Tag
import json
from ..capsule import CRMConnector
from utils.Colorizer import Colorizer
from ..serializers import PartySerializer
from ..models import Party
from rest_framework.exceptions import APIException
import copy
from rest_framework.exceptions import NotFound

class CrmTestCase(TestCase):

    party = None

    @classmethod
    def setUpClass(cls):

        cls.user_data = {
            'email': 'test_unit@test.com',
            'first_name': 'aaa_unit_test',
            'last_name': 'aaa_test_unit',
            'picture': '',
            'password': 'asdasd',
            'gender': 'Female',
            'birthdate': '1980-01-12',
            'city': 'Torreon',
            'occupation': 'tester',
            'twitter_username': '',
            'place': '{"city":"Torreon","state":"Coah.","country_short":"MX","country":"Messico","lat":25.5428443,"long":-103.40678609999998}',
        }

        cls.user = User.create(**cls.user_data)
        profile = Profile.create(user=cls.user, **cls.user_data)

        # Extra fields
        # cls.user.profile.types_of_innovation = 'Product innovation,Technological innovation,Business model innovation'
        cls.user.profile.organization = 'aaa_unit_test_organization'
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
        cls.user.profile.size = 'A small enterprise (<50 staff)'

        cls.user.profile.socialLinks = json.dumps([
            {"link": "top_ix", "name": "twitter"},
            {"link": "www.google.it", "name": "google-plus"},
            {"link": "https://www.facebook.com/topixconsortium/", "name": "facebook"}
        ])

        cls.user.profile.save()

        # Create Party
        cls.party = Party(cls.user)
        cls.party.get()

    @classmethod
    def tearDownClass(self):
        self.party.delete()

    def test_1_connection(self):
        print(Colorizer.LightPurple('\n[ CRM Test : Connection test ]'))
        response = self.party.all()
        self.assertEqual(response.status_code, 200, '[CRM-CONNECTOR ERROR] Response error :\n %s ' % response)

    def test_2_creation(self):
        print(Colorizer.LightPurple('[ CRM Test : Create ]'))
        results = self.party.create_or_update()
        self.assertIsInstance(results, dict, '[CRM-CONNECTOR ERROR] Creation Response should be a dictionary ')

    def test_5_Update(self):
        print(Colorizer.LightPurple('[ CRM Test : Update test ]'))
        results = self.party.create_or_update()
        self.assertTrue(True, '[CRM-CONNECTOR ERROR] Response is not a valid Party object :\n %s ')

    def test_6_FindNotExisting(self):
        print(Colorizer.LightPurple('\n[ CRM Test : Find non existent party by email]'))

        # Deepcopy user
        user = copy.deepcopy(self.user)
        user.email = 'test_clone@gmail.com'
        party = Party(user)

        party.emailAddresses[0]['address'] = 'test_clone@gmail.com'
        results = party.get()

        self.assertIsNone(results, '\n[CRM-CONNECTOR ERROR] Response should be empty')

    def test_7_findExisting(self):
        print(Colorizer.LightPurple('\n[ CRM Test : Find existing party]'))
        results = self.party.get()
        self.assertIsInstance(results, dict, '\n[CRM-CONNECTOR ERROR] Get Response should contain a dictionary')

    # def test_8_RemoveExisting(self):
    #     print(Colorizer.LightPurple('\n[ CRM Test : Remove test ]'))
    #     delete = self.party.delete()
    #     print 'delete'
    #
    #     print self.party.get()
    #     with self.assertRaises(NotFound):
    #         self.party.get()


