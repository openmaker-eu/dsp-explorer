# coding=utf-8
from django.test import TestCase, Client
from utils.mailer import EmailHelper
import os

class MailTestCase(TestCase):
    def setUp(self):
        self.profile = {
            'email': 'massimo.santoli@top-ix.org',
            'first_name': 'Résiérr',
            'last_name': 'Test',
            'picture': '',
            'password': 'q1w2e3r4',
            'gender': 1,
            'birthdate': None,
            'city': None,
            'occupation': None,
            'twitter_username': None,
            'place': None
        }

    def test_email_all(self):
        print '[EMAIL TEST] : all'
        #
        # render = EmailHelper.render_email('pss_upload_confirmation', {
        #     'FIRST_NAME': 'Résiérr',
        #     'LAST_NAME': 'Test',
        # })
        #
        # print 'render'
        # print render

        body = EmailHelper.email(
            template_name='pss_upload_confirmation',
            title='Test Email',
            vars={
                'FIRST_NAME': 'Résiérr',
                'LAST_NAME': 'Test',
            },
            receiver_email='massimo.santoli@top-ix.org'
        )

        self.assertTrue(body, 'Mail error')