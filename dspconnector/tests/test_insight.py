from django.test import SimpleTestCase
from dspconnector.insight import InsightConnectorV10


class ConnectorTestCase(SimpleTestCase):

    def setUp(self):
        self.connector = InsightConnectorV10

    def test_get_all_om_users_profiles(self):
        results = self.connector.crawler_profiles()
        self.assertIsNotNone(
            results['users'],
            '[INSIGHT-CONNECTOR ERROR] Response error'
        )

    def test_find_om_users_profiles(self):
        results = self.connector.crawler_profiles({filter: 'santoli'})
        print results

        self.assertIsNotNone(
            results['users'],
            '[INSIGHT-CONNECTOR ERROR] Response error'
        )




