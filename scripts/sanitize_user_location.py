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
from .functions import add_location_to_user, sanitize_place

# if __name__ == "__main__":
#     users = User.objects.all()
#     for user in users:
#         sanitize_place(user)
#         add_location_to_user(user)

def run():
    users = User.objects.all()
    for user in users:
        sanitize_place(user)
        add_location_to_user(user)
