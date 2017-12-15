import os
import sys
import django

sys.path.append("/dspexplorer/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'dspexplorer.settings'
django.setup()

from dashboard.models import User, Profile, Location, Invitation
import json
from utils.GoogleHelper import GoogleHelper


def sanitize_place(user):
    try:
        if user.profile:
            user.profile.sanitize_place()
    except Exception as e:
        print 'sanitize place error'
        print e

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
        print 'Error 2'
        print e

def deobfuscate_invitation(user):
    try:
        Invitation.deobfuscate_email(user.email, user.first_name, user.last_name)
    except Exception as e:
        print 'Error Deobfuscation'
        print e

if __name__ == "__main__":
    users = User.objects.all()
    for user in users:
        sanitize_place(user)
        add_location_to_user(user)
        deobfuscate_invitation(user)

