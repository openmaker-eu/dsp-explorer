# coding=utf-8
from django.test import TestCase
from connector import DSPConnector,DSPConnectorV12
import json

class AuthTestCase(TestCase):
    def setUp(self):
        self.connector = DSPConnectorV12
        pass

    def test_topics(self):
        print '\n[DSP-CONNECTOR TEST] Test for TOPICS API'
        results = self.connector.get_topics()
        self.assertIsNotNone(
            results and results['topics'],
            'Dsp response is not a topics object'
        )

    def test_audiences(self):
        print '\n[DSP-CONNECTOR TEST] Test for AUDIENCE API'
        results = self.connector.get_audiences(self.get_first_topic_id())
        self.assertIsNot(
            results and results['audiences'],
            False,
            'Dsp response is not an Audience object'
        )

    def test_news(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API'
        results = self.connector.get_news((self.get_first_topic_id(),))
        self.assertIsNot(
            len(results) > 0 and results['news'],
            False,
            'Dsp response is not a News object'
        )

    def test_news_search(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API FILTERED'
        results = self.connector.search_news((self.get_first_topic_id(),))
        self.assertIsNot(
            len(results) > 0 and results['news'],
            False,
            'Dsp response is not a News object'
        )

    def get_first_topic_id(self):
        return self.connector.get_topics()['topics'][0]['topic_id'] or 1



