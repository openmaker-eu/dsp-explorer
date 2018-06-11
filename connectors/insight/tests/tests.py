
from django.test import TestCase
from connectors.insight.connector import InsightConnectorV10 as Insight
from utils.Colorizer import Colorizer


class InsightTestCase(TestCase):

    crm_id = '145489262'

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def test_1_connection(self):
        print(Colorizer.LightPurple('\n[ CRM Test : Connection test ]'))
        response = Insight.questions(crm_ids=[self.crm_id])
        print('response')
        print(response.json())
        self.assertEqual(response.status_code, 200, '[INSIGHT-CONNECTOR ERROR] Response error ')



