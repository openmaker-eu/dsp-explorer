# coding=utf-8
from django.test import TestCase, Client
from utils.mailer import EmailHelper
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, invitation_email_receiver


class MailTestCase(TestCase):
    def setUp(self):
        self.email = 'massimo.santoli@top-ix.org'

    def test_all(self):
        subject = 'You are invited to join the OpenMaker community!'
        content = "{0}{1}{2}".format(invitation_base_template_header,
                                     invitation_email_receiver.format(RECEIVER_FIRST_NAME='TEST',
                                                                      RECEIVER_LAST_NAME='TESTER',
                                                                      SENDER_FIRST_NAME='receiver',
                                                                      SENDER_LAST_NAME='recever',
                                                                      ONBOARDING_LINK='http://localhost/onboarding/'),
                                     invitation_base_template_footer)

        EmailHelper.send_email(
            message=content,
            subject=subject,
            receiver_email=self.email,
            receiver_name=''
        )