import os
import sys
import django
import requests
import time

sys.path.append("/dspexplorer/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'dspexplorer.settings'
django.setup()

from dashboard.models import User, Profile
import json
from crmconnector.models import Party
from utils.Colorizer import Colorizer
from crmconnector.capsule import CRMValidationException
from collections import OrderedDict
import urllib


def sanitize_place(city=None):
    from django.db.models import Q

    users = User.objects.filter(Q(profile__place=None)).distinct()

    for user in users:
        pass
        # try:
        #     if user.profile:
        #         city = user.profile.city
        #         print ' '
        #         print '----------------------------'
        #         print city
        #         print '############################'
        #         print get_city(city)
        #         print '----------------------------'
        #         print ' '
        # except:
        #     pass


def get_city(city=None):
    api_key = 'AIzaSyB7FZZonHwxfYY2gwDAgd587AMah0336Gw'
    city = city or 'turin'

    city_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?' \
               ''+urllib.urlencode({'input': city, 'key': api_key, 'language': 'en', 'types': '(cities)'})

    place = None
    place_detail = None

    try:
        response = requests.get(city_url)
        if response.status_code < 203:
            # place = json.loads(response.content, object_pairs_hook=OrderedDict)
            place = json.loads(response.content)
            place = place['predictions'][0]

    except Exception as e:
        print 'error'
        print e

    if place:
        place_id = place['place_id']
        detail_url = 'https://maps.googleapis.com/maps/api/place/details/json?' \
                     ''+urllib.urlencode({'placeid': place_id, 'key': api_key})

        try:
            response = requests.get(detail_url)
            if response.status_code < 203:
                # place_detail = json.loads(response.content, object_pairs_hook=OrderedDict)
                place_detail = json.loads(response.content)['result']

        except Exception as e:
            print 'error'
            print e

    if place and place_detail:
        try:
            post_code = filter(lambda x: "postal_code" in x["types"], place_detail['address_components'])
            state = filter(lambda x: "political" in x["types"] and not ['country'] in x['types'], place_detail['address_components'])
            country = filter(lambda x: "country" in x["types"], place_detail['address_components'])

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
            print 'error'
            print e

    else:
        print 'place'
        print not not place
        print 'place_detail'
        print not not place_detail
        return None


if __name__ == "__main__":
    city_name = sys.argv[1] if len(sys.argv) > 1 else None
    sanitize_place(city_name)

