import logging
import smtplib
import time
from email.header import Header
from email.message import Message

from django.conf import settings


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
        # TODO ASYNC CALL!
        receivers = [receiver_email]
        formatted_message = Message()
        formatted_message['Subject'] = Header("%s - %s" % (subject, time.strftime("%d/%m/%Y %H:%M:%S")), 'utf-8')
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
