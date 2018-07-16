import requests
from django.conf import settings
import json
from rest_framework.exceptions import NotFound


class CRMValidationException(Exception):
    pass


class CRMConnector(object):
    
    @staticmethod
    def _wrapper_request(response):
        if response.status_code < 204:
            return response.json()
        if response.status_code == 204:
            # Handle no content response
            return None
        if response.status_code == 422:
            raise CRMValidationException('Status Code: {0}\nResponse: {1}'.format(response.status_code, response.content))

        raise NotFound('There are some connection problem, try again later')

    @staticmethod
    def _get_headers():
        headers = {
            'Authorization': 'Bearer {}'.format(settings.SECRET_TOKEN),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers
    
    @staticmethod
    def _perform_get(url):
        """
        Perform HTTP GET with Authorization Headers
        :url: Specify the destination URL
        :return: Requests Response Object
        """
        return requests.get(url=url, headers=CRMConnector._get_headers())
    
    @staticmethod
    def _perform_post(url, data):
        """
        Perform HTTP POST with Authorization Headers
        :url: Specify the destination URL
        :data: Content Body
        :return: Requests Response Object
        """
        return CRMConnector._wrapper_request(requests.post(url=url, data=data.encode("ascii", "ignore"), headers=CRMConnector._get_headers()))

    @staticmethod
    def _perform_put(url, data):
        """
        Perform HTTP PUT with Authorization Headers
        :url: Specify the destination URL
        :data: Content Body
        :return: Requests Response Object
        """
        return CRMConnector._wrapper_request(requests.put(url=url, data=data, headers=CRMConnector._get_headers()))

    @staticmethod
    def _perform_delete(url):
        """
        Perform DEL with Authorization Headers
        :url: Specify the destination URL
        :return: Requests Response Object
        """
        return CRMConnector._wrapper_request(requests.delete(url=url, headers=CRMConnector._get_headers()))
    
    @staticmethod
    def search_party_by_email(email):
        """
        Perform an API Search
        :param email: Email to search
        :return: API Response
        """
        search_url = settings.CAPSULE_BASE_URL_PARTIES+'/search?q={}&embed=fields,tags'.format(email)
        resp = CRMConnector._perform_get(search_url)
        try:
            party = resp.json().get('parties', [])
            return party[0]
        except IndexError:
            return None

    @staticmethod
    def search_party(field_name, field_value):
        """
        Perform an API Search
        :param email: Email to search
        :return: API Response
        """
        search_url = settings.CAPSULE_BASE_URL_PARTIES+'/search?q={}&embed=fields,tags'.format(email)
        resp = CRMConnector._perform_get(search_url)
        try:
            party = resp.json().get('parties', [])
            return party[0]
        except IndexError:
            return None

    @staticmethod
    def get_all_parties(paginated=False):
        pagination = '?page=1&perPage=10' if paginated else ''
        return CRMConnector._perform_get(settings.CAPSULE_BASE_URL_PARTIES + '/' + pagination)

    @staticmethod
    def add_party(party):
        party = json.dumps(party)
        return CRMConnector._perform_post(settings.CAPSULE_BASE_URL_PARTIES, party)

    @staticmethod
    def update_party(party_id, party):
        print(type(party))
        print(party)
        party = json.dumps(party)
        return CRMConnector._perform_post(settings.CAPSULE_BASE_URL_PARTIES + '/' + str(party_id), party)

    @staticmethod
    def delete_party(party_id):
        return CRMConnector._perform_delete(settings.CAPSULE_BASE_URL_PARTIES + '/' + str(party_id))

    @staticmethod
    def get_custom_field_definitions(entity_name):
        url = settings.CAPSULE_BASE_URL+'/'+entity_name+'/fields/definitions?perPage=100'
        resp = CRMConnector._wrapper_request(requests.get(url=url, headers=CRMConnector._get_headers()))
        try:
            return resp.get('definitions', [])
        except IndexError:
            return None
