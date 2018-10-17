import requests
import json
import urllib
from django.conf import settings
from urllib.parse import urlencode
from urllib.request import urlopen
from .Colorizer import Colorizer
import traceback
from utils.Logger import Logger

class GoogleHelper:

    @classmethod
    def get_city(cls, city):
        api_key = settings.GOOGLE_API_KEY
        city_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?' \
                   ''+urlencode({'input': city, 'key': api_key, 'language': 'en', 'types': '(cities)'})

        place = None
        place_detail = None

        try:
            response = requests.get(city_url)
            if response.status_code < 203:
                resp = response.json()
                place = resp['predictions'][0]

        except Exception as e:
            print(Colorizer.Red('[ERROR utils.GoogleHelper.get_city] Get from google place/autocomplete/ '))
            print(Logger.error(e))

        if place:
            place_id = place['place_id']
            detail_url = 'https://maps.googleapis.com/maps/api/place/details/json?' \
                         ''+urlencode({'placeid': place_id, 'key': api_key})
            try:
                response = requests.get(detail_url)
                if response.status_code < 203:
                    # place_detail = json.loads(response.content, object_pairs_hook=OrderedDict)
                    resp = response.json()
                    place_detail = resp['result']
            except Exception as e:
                print(Colorizer.Red('[ERROR utils.GoogleHelper.get_city] Get from google place/details/ '))
                print(Logger.error(e))

        if place and place_detail:
            try:
                post_code = [x for x in place_detail['address_components'] if "postal_code" in x["types"]]
                state = [
                    x for x in place_detail['address_components']
                    if "political" in x["types"]
                    and not ['country'] in x['types']
                ]
                country = [x for x in place_detail['address_components'] if "country" in x["types"]]

                post_code = post_code[0] if len(post_code) > 0 else []
                state = state.pop() if len(state) > 0 else []
                country = country[0] if len(country) > 0 else []

                return {
                    "city": place_detail['address_components'][0]['long_name'],
                    "state": state['short_name'] if 'short_name' in state else '',
                    "country": country['long_name'] if 'long_name' in country else '',
                    "country_short": country['short_name'] if 'short_name' in country else '',
                    "post_code": post_code['short_name'] if 'short_name' in post_code else '',
                    "lat": place_detail['geometry']['location']['lat'],
                    "long": place_detail['geometry']['location']['lng']
                }

            except Exception as e:
                print(Colorizer.Red('[ERROR utils.GoogleHelper.get_city] create places from google responses '))
                print(Logger.error(e))
                print(Colorizer.LightPurple('place'))
                print(Colorizer.LightPurple(place))
                print(Colorizer.Cyan('place_detail'))
                print(Colorizer.Cyan(place_detail))
                print(Colorizer.Yellow(exception_to_string(e)))
        else:
            return None


def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)
