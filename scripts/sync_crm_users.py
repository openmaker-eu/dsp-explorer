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
from .functions import update_crm


def run(*args):
    profiles = Profile.objects.filter(user__email=args[0]) \
        if len(args) > 0 \
        else Profile.objects.all()

    for profile in profiles:
        try:
            update_crm(profile.user)
            print(Colorizer.Green('SUCCESS CRM user update : ' + profile.user.email))
        except Exception as e:
            print(Colorizer.Red('#################################################'))
            print(Colorizer.Red('ERROR CRM Updating user : ' + profile.user.email))
            print(Colorizer.Red(e))
            print(Colorizer.Red('#################################################'))
