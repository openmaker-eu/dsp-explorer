# coding=utf-8
from django.test import TestCase, Client
from dashboard.models import Profile
import json

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_profile_is_unicode_safe(self):
        print '[UTF-8 ENCODING TEST]'
        Profile.create(
            email='testcase@top-ix.org',
            first_name='Résiérr',
            last_name='Test',
            picture='',
            password='q1w2e3r4',
            gender=1,
            birthdate=None,
            city=None,
            occupation=None,
            twitter_username=None,
            place=None
        )
        profile = Profile.objects.filter(pk=1)[0]
        welcome = "Welcome onboard {}!".format(profile.user.first_name.encode('utf-8'))
        self.assertEqual(json.dumps(welcome), json.dumps('Welcome onboard R\xc3\xa9si\xc3\xa9rr!'))

    def test_api_v12_topics(self):
        print '[test_api_v12_topics] test url'

        response = self.client .get('/api/v1.2/topics')
        results = self.get_results(response)

        self.assertIsNot(
            results and results['topics'],
            False,
            'Dsp response is not a topics object'
        )

    def test_api_v12_audiences(self):
        print '[test_api_v12_audiences]'
        try:
            topics = self.get_results(self.client.get('/api/v1.2/topics'))
        except:
            raise self.failureException('No topics found')

        response = self.client.get('/api/v1.2/audiences/{topic_id}/'.format(topic_id=topics['topics'][0]['topic_id']))
        results = self.get_results(response)

        self.assertIsNot(
            results and results['audiences'],
            False,
            'Response is not a audiences object'
        )

    def get_results(self, response):
        try:
            results = json.loads(response.content)
            return 'status' in results and (results['status'] == 'ok') and 'result' in results and results['result']
        except:
            return False
