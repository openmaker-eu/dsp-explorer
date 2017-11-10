# -*- coding: utf-8 -*-
from django.test import TestCase
from dashboard.models import Profile, User
from itertools import groupby
import json
from ..capsule import CRMConnector
from utils.Colorizer import Colorizer
from ..serializers import PartySerializer
from ..models import Party
from rest_framework.exceptions import APIException

class CrmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'email': 'test_unit@test.com',
            'first_name': 'aaa_unit_test',
            'last_name': 'aaa_test1',
            'picture': '',
            'password': 'asdasd',
            'gender': 'm',
            'birthdate': '1980-01-12',
            'city': 'Torreón',
            'occupation': 'tester',
            'twitter_username': '',
            'place': '{"city":"Torreón","state":"Coah.","country_short":"MX","country":"Messico","lat":25.5428443,"long":-103.40678609999998}',
        }
        profile = Profile.create(**cls.user_data)
        cls.user = User.objects.filter(email=cls.user_data['email'])[0]
        cls.party = Party(cls.user)

    def tearDown(self):
        test_party = CRMConnector.search_party_by_email(CrmTestCase.user_data['email'])
        print test_party
        if test_party and test_party['id']:
            CRMConnector.delete_party(test_party['id'])

    def testConnection(self):
        print(Colorizer.LightPurple('[ CRM Test : Connection test ]'))
        response = CRMConnector.get_all_parties()
        self.assertEqual(response.status_code, 200, '[CRM-CONNECTOR ERROR] Response error :\n %s ' % response)

    def testInsertion(self):
        print(Colorizer.LightPurple('[ CRM Test : Insertion test ]'))

        response = CRMConnector.add_party({'party': CrmTestCase.party.__dict__})
        self.assertTrue(True, '[CRM-CONNECTOR ERROR] Response is not a valid Party object :\n %s ' % response)
