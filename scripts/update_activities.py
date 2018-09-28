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
from .functions import update_activities


def run():
    profiles = Profile.objects.all()
    for profile in profiles:
        try:
            update_activities(profile.user)
        except Exception as e:
            print(Colorizer.Red('####################################'))
            print(Colorizer.Red('Error updating activities'))
            print(Colorizer.Red(e))
            print(Colorizer.Red('####################################'))
        else:
            print(Colorizer.Green('Acitivite updated :' + profile.user.email))
