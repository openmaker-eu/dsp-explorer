import requests
from django.conf import settings


class CRMConnector(object):
    
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
        return requests.post(url=url, data=data, headers=CRMConnector._get_headers())

    @staticmethod
    def _perform_put(url, data):
        """
        Perform HTTP PUT with Authorization Headers
        :url: Specify the destination URL
        :data: Content Body
        :return: Requests Response Object
        """
        return requests.put(url=url, data=data, headers=CRMConnector._get_headers())

    @staticmethod
    def _perform_delete(url):
        """
        Perform DEL with Authorization Headers
        :url: Specify the destination URL
        :return: Requests Response Object
        """
        return requests.delete(url=url, headers=CRMConnector._get_headers())
    
    @staticmethod
    def search_party_by_email(email):
        """
        Perform an API Search
        :param email: Email to search
        :return: API Response
        """
        search_url = 'https://api.capsulecrm.com/api/v2/parties/search?q={}'.format(email)
        resp = CRMConnector._perform_get(search_url)
        try:
            party = resp.json().get('parties', [])
            return party[0]
        except IndexError:
            return None

    # def create user
