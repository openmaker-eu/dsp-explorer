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
    users = User.objects.all()
    for profile in profiles:
        try:
            profile.user
        except User.DoesNotExist:
            print(Colorizer.Red('User doesnt exist for profile with ID : ' + str(profile.id)))
            profile.delete()
            print(Colorizer.Cyan('Removing profile'))
    for user in users:
        try:
            user.profile
        except Profile.DoesNotExist:
            print(Colorizer.Red('Profile doesnt exist for user ID: ' + str(user.id) + ', EMAIL: ' + user.email))
            user.delete()
            print(Colorizer.Cyan('Removing user with EMAIL: ' + user.email))
