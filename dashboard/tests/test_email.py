# coding=utf-8
from django.test import TestCase, Client
from utils.mailer import EmailHelper
import os

class MailTestCase(TestCase):
    def setUp(self):
        self.email_vars = {
            'EMAIL': 'massimo.santoli@top-ix.org',

            'FIRST_NAME': 'Résiérr',
            'SENDER_NAME': 'Résiérr',
            'RECEIVER_FIRST_NAME': 'Résiérr',
            'SENDER_FIRST_NAME': 'Résiérr',
            'APPLIER_FIRST_NAME': 'Résiérr',

            'LAST_NAME': 'Test',
            'RECEIVER_LAST_NAME': 'Test',
            'SENDER_LAST_NAME': 'Test',
            'APPLIER_LAST_NAME': 'Test',

            'ONBOARDING_LINK': 'http://localhost:8000',
            'CONFIRMATION_LINK': 'http://localhost:8000',
            'BASE_URL': 'http://localhost:8000',
            'TOKEN': 'token',
            'LES': 'ITALY',

            'APPLICATION_NAME': 'Testapp'

        }

    def test_email_all(self):
        print '[EMAIL TEST] : all'

        email_list = (
            'invitation_email_confirm',
            'pss_upload_confirmation',
            'invitation_email_receiver',
            'onboarding_email_template',
            'pss_upload_confirmation',
            'pss_admin_upload_confirmation',
            'authentication_reset_password'
        )

        for email_name in email_list:
            body = EmailHelper.email(
                template_name=email_name,
                title='Test Email',
                vars=self.email_vars,
                receiver_email='massimo.santoli@top-ix.org'
            )

        self.assertTrue(body, 'Mail error')