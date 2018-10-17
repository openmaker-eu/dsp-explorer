import os
import sys
import django

sys.path.append("/dspexplorer/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'dspexplorer.settings'
django.setup()

from dashboard.models import User, Profile, Location, Invitation
import json
from utils.GoogleHelper import GoogleHelper
from utils.Colorizer import Colorizer


def add_place_to_profile(profile):
    try:
        profile.sanitize_place(force=True)
    except Exception as e:
        print(Colorizer.Red('###############################'))
        print(Colorizer.Red('sanitize place error'))
        print(Colorizer.Red(e))
        print(Colorizer.Red('###############################'))
    else:
        print(Colorizer.Green('PLACE OK: '+profile.user.email))


def add_location_to_user(user):
    try:
        if user.profile.place:
            place = json.loads(user.profile.place)

            location = Location.create(
                lat=repr(place['lat']),
                lng=repr(place['long']),
                city=place['city'],
                state=place['state'],
                country=place['country'],
                country_short=place['country_short'],
                post_code=place['post_code'] if 'post_code' in place else '',
                city_alias=place['city']+','
            )
            user.profile.location = location
            user.profile.save()

    except Exception as e:
        print(Colorizer.Red('###############################'))
        print(Colorizer.Red('Add location error'))
        print(Colorizer.Red(e))
        print(Colorizer.Red('###############################'))
    else:
        print(Colorizer.Green('LOCATION OK: '+user.email))


def run():
    users = User.objects.all()
    for user in users:
        add_place_to_profile(profile)
        add_location_to_user(user)




        {"city":"Arezzo","state":"Toscana","country_short":"IT","country":"Italia","post_code":"52100","lat":43.46328390000001,"long":11.879633600000034}
