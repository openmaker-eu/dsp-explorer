# coding=utf-8
from django.test import TestCase, Client
from dashboard.models import Profile
import json


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()

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
