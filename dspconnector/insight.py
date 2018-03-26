import requests
from django.conf import settings
from urllib import urlencode


class InsightConnectorV10(object):

    @classmethod
    def crawler_profiles(cls, qs=None):
        return cls.get('omn_crawler/get_om_user_profiles', qs)

    @classmethod
    def crawler_twitter_profiles(cls, qs=None):
        return cls.get('omn_crawler/twitter/get_profiles', qs)

    @classmethod
    def crawler_twitter_tweet(cls, qs=None):
        return cls.get('omn_crawler/twitter/get_tweets', qs)

    @classmethod
    def crawler_crm_users(cls, qs):
        return cls.get('omn_crawler/crm/get_users', qs)

    @classmethod
    def get(cls, endpoint, querydict={}):
        querydict = '?' + urlencode(querydict, False) if querydict and len(querydict) > 0 else ''
        url = settings.INSIGHT_API + 'api/v1.0/' + endpoint + querydict
        print url
        try:
            response = requests.get(url, timeout=8)
            if response and response.status_code < 205:
                response = response.json()
        except:
            response = None
        return response