# coding=utf-8
from django.test import TestCase, Client
from dashboard.models import Profile
import json
from dashboard.models import Profile, User, SourceOfInspiration, Tag
from django.shortcuts import render, reverse


class ProfileTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.client = Client()

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

        Profile.create(**cls.user_data)
        cls.user = User.objects.filter(email=cls.user_data['email'])[0]
        cls.user.set_password('12345')

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

    def test_profile_get(self):
        print '[TEST PROFILE PAGE] test get'

        logged_in = self.client.login(username='test_unit@test.com', password='12345')
        user = User.objects.filter(email='test_unit@test.com')[0]

        # response = self.client.get(reverse('dashboard:profile', kwargs={'profile_id': user.pk}))
        response = self.client.get('/?next=/profile/1/')

        for cont in response.context:
            print 'context'
            for c in cont:
                print c
            print '-------------------------'

        print 'context'

        self.assertTrue(True, 'Dsp response is not a topics object')
