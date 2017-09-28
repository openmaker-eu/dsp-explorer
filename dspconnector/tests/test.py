# coding=utf-8
from django.test import TestCase
from dspconnector.connector import DSPConnector, DSPConnectorV12
from dspconnector.serializers import TopicsSerializer, AudiencesSerializer, NewsSerializer
import json

class AuthTestCase(TestCase):
    def setUp(self):
        self.connector = DSPConnectorV12

    # ###### #
    # TOPICS #
    # ###### #
    def test_topics(self):
        print '\n[DSP-CONNECTOR TEST] Test for TOPICS API'
        results = self.connector.get_topics()

        self.assertIsNotNone(
            results and results['topics'],
            '[DSP-CONNECTOR ERROR] Response doesn\'t contain a topics field'
        )

    def test_topics_response_data(self):
        print '\n[DSP-CONNECTOR TEST] Test for TOPICS API: response data'
        results = self.connector.get_topics()['topics']
        serializer = TopicsSerializer(data=results, many=True)
        self.assertTrue(
            serializer.is_valid(),
            '[DSP-CONNECTOR ERROR] Response is not a Topics object :\n %s' % serializer.errors
        )

    # ######### #
    # AUDIENCES #
    # ######### #
    def test_audiences(self):
        print '\n[DSP-CONNECTOR TEST] Test for AUDIENCE API'
        results = self.connector.get_audiences(self.get_first_topic_id())
        self.assertIsNot(
            results and results['audiences'],
            False,
            '[DSP-CONNECTOR ERROR] Response doesn\'t contain an audience field'
        )

    def test_audiences_response_data(self):
        print '\n[DSP-CONNECTOR TEST] Test for AUDINCES API: response data'
        results = self.connector.get_audiences(self.get_first_topic_id())
        serializer = AudiencesSerializer(data=results['audiences'], many=True)
        self.assertTrue(
            serializer.is_valid(),
            '[DSP-CONNECTOR ERROR] Response is not an Audiences object :\n %s ' % serializer.errors
        )

    # #### #
    # NEWS #
    # #### #
    def test_news(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API'
        results = self.connector.get_news(self.get_first_topic_id())
        self.assertIsNot(
            len(results) > 0 and results['news'],
            False,
            '[DSP-CONNECTOR ERROR] Response doesn\'t contain a news filed'
        )

    def test_news_response_data(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API: response data'
        results = self.connector.get_news(self.get_first_topic_id())
        serializer = NewsSerializer(data=results['news'], many=True)
        self.assertTrue(
            serializer.is_valid(),
            '[DSP-CONNECTOR ERROR] Response is not an Audiences object :\n %s ' % serializer.errors
        )

    def test_news_search(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API FILTERED: providing "topic_id", "cursor" and "since" parameters'
        results = self.connector.search_news(self.get_first_topic_id(), {'cursor': '-1', 'since': '01-01-2017'})
        self.assertIsNot(
            len(results) > 0 and results['news'],
            False,
            '[DSP-CONNECTOR ERROR] Response doesn\'t contain a news field'
        )

    def test_news_search_multiple_topic_ids_list(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API FILTERED: multiple ids as list'
        topics = self.connector.get_topics()['topics']
        results = self.connector.search_news(
            [topics[0]['topic_id'], topics[0]['topic_id']],
            {'cursor': '-1', 'since': '01-01-2017'}
        )
        self.assertIsNot(
            len(results) > 0 and results['news'],
            False,
            '[DSP-CONNECTOR ERROR] Response doesn\'t contain a news field'
        )

    def test_news_search_multiple_topic_ids_string(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API FILTERED: multiple ids as string'
        topics = self.connector.get_topics()['topics']
        results = self.connector.search_news(
            ''+str(topics[0]['topic_id'])+','+str(topics[0]['topic_id']),
            {'cursor': '-1', 'since': '01-01-2017'}
        )
        self.assertIsNot(
            len(results) > 0 and results['news'],
            False,
            '[DSP-CONNECTOR ERROR] Response doesn\'t contain a news field'
        )

    def test_news_search_only_one_parameter(self):
        print '\n[DSP-CONNECTOR TEST] Test for NEWS API FILTERED: providing only topic_id'
        results = self.connector.search_news((self.get_first_topic_id(),))
        self.assertIsNot(
            len(results) > 0 and results['news'],
            False,
            '[DSP-CONNECTOR ERROR] NEWS api doesn\'t work providing only topic_id as parameter'
        )

    # #########
    # HELPERS
    # #########
    def get_first_topic_id(self):
        return self.connector.get_topics()['topics'][0]['topic_id'] or 1




