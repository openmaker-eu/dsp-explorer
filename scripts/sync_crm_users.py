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
    errored = []
    profiles = Profile.objects.filter(user__email=args[0]) \
        if len(args) > 0 \
        else Profile.objects.all()
    for k, profile in enumerate(profiles):
        print(Colorizer.Cyan('UPDATING : ' + str(k) + ' of ' + str(len(profiles))))
        results = update_crm(profile.user)
        results and errored.append(results)

    print(Colorizer.Yellow(' '))
    print(Colorizer.Yellow('############### RESULTS ###############'))
    print('')
    print(Colorizer.Green(str(len(profiles)-len(errored)) + ' USERS WAS SUCCESFULLY UPDATED'))
    print(' ')
    print(Colorizer.Red(str(len(errored)) + ' USERS WITH ERRORS :'))
    for error in errored:
        print('    ')
        print('    '+Colorizer.Red(error['user'].email+' UUID: '+str(error['user'].id)))
        print('      | EXCEPTION: ')
        [print('      | '+line) for line in str(error['error']).split('\n')]
    print(Colorizer.Yellow(' '))
    print(Colorizer.Yellow('#######################################'))

