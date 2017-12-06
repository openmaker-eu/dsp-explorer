import requests
from django.conf import settings
import json
from rest_framework.exceptions import NotFound
import urllib

dataset = 'geonames-all-cities-with-a-population-1000@public'
# api_key = settings.OPENDATA_KEY

class OPENDATAValidationException(Exception):
    pass


class OpenDataConnector(object):

    @classmethod
    def __get_headers(cls):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    @classmethod
    def __handle_response(cls, results):
        print results
        if results and results.status_code < 203:
            return results
        else:
            return False

    @classmethod
    def __get_url(cls, params):
        return 'https://data.opendatasoft.com/api/records/1.0/search/?' \
               ''+urllib.urlencode(params)

    @classmethod
    def __perform_get(cls, url):
        return requests.get(url=url, headers=cls.__get_headers())

    @classmethod
    def get_by_latlng(cls, latlng):
        url = cls.__get_url({'dataset': dataset, 'facet': 'country', 'geofilter.distance': latlng+',1000'})+'&facet=timezone'
        return cls.__perform_get(url)

    @classmethod
    def get_city_alternate_name_by_latlng(cls, latlng):
        results = None
        response = cls.get_by_latlng(latlng)

        # if cls.__handle_response(response):
        try:
            results = json.loads(response.content)['records'][0]['fields']['alternate_names']
        except:
            results = None

        return results
