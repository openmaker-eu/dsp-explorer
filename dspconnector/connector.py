import requests
from django.conf import settings


class DSPConnectorException(Exception):

    response = None

    def __init__(self, resp):
        if resp:
            self.message = "Exception due to status code: %s" % resp.status_code
            self.response = resp
        else:
            self.message = "Connection error, please try again later."
            self.response = None


class DSPConnector(object):
    
    @staticmethod
    def get_themes():
        return DSPConnector._get(DSPConnector.generate_url(endpoint=settings.DSP_GET_THEMES))
    
    @staticmethod
    def get_feeds(theme_name):
        return DSPConnector._get(DSPConnector.generate_url(endpoint=settings.DSP_GET_FEEDS, parameter=theme_name))

    @staticmethod
    def get_influencers(theme_name):
        return DSPConnector._get(DSPConnector.generate_url(endpoint=settings.DSP_GET_INFLUENCERS, parameter=theme_name))
    
    @staticmethod
    def generate_url(endpoint, parameter=None):
        return settings.DSB_API_URL + endpoint + '/' + parameter if parameter else settings.DSB_API_URL + endpoint
    
    @staticmethod
    def _wrapper_request(response):
        if response and response.status_code < 205:
            return response.json()
        raise DSPConnectorException(response)
    
    @staticmethod
    def _get(url):
        try:
            response = requests.get(url)
        except:
            response = None
        return DSPConnector._wrapper_request(response=response)
