# coding=utf-8
import logging
import smtplib
import time
from email.header import Header
from email.message import Message

from django.conf import settings
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, \
    invitation_email_confirmed, invitation_email_receiver, onboarding_email_template
import os

from django.template import loader, Context, Template
from django.template.loader import render_to_string



class EmailHelper(object):
    """
    Email Helper Class
    Usage Example
        EmailHelper.send_email(message="Hello Friend",
                           subject="TESTING EMAIL",
                           receiver_name="top-ix User",
                           receiver_email="test1@top-ix.org")
    """
    
    @staticmethod
    def _format_email(name, email):
        return "{} <{}>".format(name, email)
    
    @staticmethod
    def send_email(message, subject, sender_name='DSPExplorer - Open Maker',
                   receiver_name=None, sender_email='noreply@openmaker.eu',
                   receiver_email=None):
        print "send_email"
        receivers = [receiver_email]
        formatted_message = Message()
        formatted_message['Content-Type'] = 'text/html'
        formatted_message['Subject'] = Header("%s" % (subject))
        formatted_message['From'] = EmailHelper._format_email(sender_name, sender_email)
        formatted_message['To'] = EmailHelper._format_email(receiver_name, receiver_email)
        formatted_message.set_payload("""{}""".format(message))
        
        try:
            smtp_obj = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.ehlo()
            smtp_obj.login(settings.SMTP_USERNAME, settings.SMTP_KEY)
            smtp_obj.sendmail(sender_email, receivers, str(formatted_message))
            logging.info("Email sent to %s" % receiver_email)
        except smtplib.SMTPException as error:
            logging.error("Error: unable to send email to %s because:\n%s" % (receiver_email, error.message))

    @staticmethod
    def send_test_email(sendTo):
        """
        :info: example email sender for testing purpose
        :param sendTo:
        :return: void
        """
        content = "{}{}{}".format(invitation_base_template_header,
                                  invitation_email_receiver.format(RECEIVER_FIRST_NAME='Name',
                                                                   RECEIVER_LAST_NAME='Last',
                                                                   SENDER_FIRST_NAME='Send name',
                                                                   SENDER_LAST_NAME='Send last',
                                                                   ONBOARDING_LINK='www.example.ix'),
                                  invitation_base_template_footer)

        EmailHelper.send_email(
            message=content,
            subject='Test email',
            receiver_email=sendTo,
            receiver_name='Tester'
        )

    @staticmethod
    def render_email(template_name, vars={}):
        base_template_path = os.path.join(settings.BASE_DIR, 'templates/email/base.html')
        body_template_path = os.path.join(settings.BASE_DIR, 'templates/email/'+template_name+'.html')

        base_template = open(base_template_path).read()\
            .replace('{', '{{')\
            .replace('}', '}}')\
            .replace('***BODY***', '{0}')
        body_template = open(body_template_path).read().replace('\n', '')

        email_template = Template(
            base_template.format(body_template)
        )

        return email_template.render(Context(vars))

    @staticmethod
    def email(template_name, receiver_email, title, vars={}):
        try:
            EmailHelper.send_email(
                subject=title,
                message=EmailHelper.render_email(template_name, vars).encode('utf-8'),
                receiver_email=receiver_email
            )
            return True
        except Exception as exc:
            print exc
            return exc