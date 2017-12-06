import requests
from django.conf import settings
import json
from rest_framework.exceptions import NotFound
import urllib


class RestCountriesValidationException(Exception):
    pass


class RestCountriesConnector(object):
    @classmethod
    def __get_headers(cls):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    @classmethod
    def __handle_response(cls, results):
        if results and results.status_code < 203:
            return results
        else:
            return False

    @classmethod
    def __perform_get(cls, city_name):
        return requests.get(url='https://restcountries.eu/rest/v2/name/'+city_name, headers=cls.__get_headers())

    @classmethod
    def get_city_alias(cls, city_name):
        results = None
        response = cls.__perform_get(city_name)

        # if cls.__handle_response(response):
        try:
            response = json.loads(response.content)[0]
            en = response['name']
            aliases = response['translations']
            results = ','.join([aliases[x] for x in aliases])+','+','.join(response['altSpellings'])+','+en+','+response['nativeName']+','
        except:
            results = None

        return results

