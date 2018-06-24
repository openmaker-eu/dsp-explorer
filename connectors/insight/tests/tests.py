
from django.test import TestCase
from connectors.insight.connector import InsightConnectorV10 as Insight
from utils.Colorizer import Colorizer
from utils.testhelpers import User


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
        self.assertEqual(response.status_code, 200, '[INSIGHT-CONNECTOR ERROR] Response error ')

    def test2_recommend_profiles_response(self):
        resp = Insight.reccomended_user(self.crm_id)
        self.assertLess(resp.status_code, 205)

    def test2_recommend_profiles(self):
        resp = Insight.reccomended_user(self.crm_id)
        print(resp.json())
        self.assertLess(resp.status_code, 205)
        



