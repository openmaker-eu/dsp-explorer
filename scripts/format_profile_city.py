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

def format_city(profile):
    try:
        if profile.place:
            place = json.loads(profile.place.replace('\'', '"'))
            if not all(k in place for k in ['city', 'state', 'country']):
                print(Colorizer.Purple('Triying to retrieve place from google'))
                profile.sanitize_place(force=True)
            if all(k in place for k in ['city', 'state', 'country']):
                profile.city = place['city']+', '+place['state']+', '+place['country']
                profile.save()

    except Exception as e:
        print(Colorizer.Red('###############################'))
        print(Colorizer.Red('Add location error'))
        print(Colorizer.Red(e))
        print(Colorizer.Red(profile.place))
        print(Colorizer.Red('###############################'))
    else:
        print(Colorizer.Green('LOCATION OK: '+profile.user.email))


def run():
    profiles = Profile.objects.all()
    for profile in profiles:
        format_city(profile)
