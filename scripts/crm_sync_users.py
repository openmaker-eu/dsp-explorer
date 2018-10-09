import os
import sys
import django

sys.path.append("/dspexplorer/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'dspexplorer.settings'
django.setup()

from .functions import sync_profiles, user_sync_template


def run(*args):
    user_sync_template(sync_profiles, args)

