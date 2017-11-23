
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dspexplorer.settings")

from dspexplorer.wsgi import application



from django.conf import settings
from dashboard import models
from utils.api import *
import json
from crmconnector.models import Party
from utils.Colorizer import Colorizer


def update_crm(request, crmtoken):
    import threading
    if not crmtoken == settings.CRM_UPDATE_TOKEN:
        return not_authorized

    # users = User.objects.all()
    users = User.objects.filter(email='massimo.santoli@top-ix.org')

    thr = threading.Thread(target=create_or_update_party, kwargs=dict(users=users))
    thr.start()

    return JsonResponse({'status': 'ok'}, status=200)

def create_or_update_party(users):
    errored = []
    sanititized = []
    party = None
    for user in users:
        try:
            print ('--------------------')
            print ('UPDATING USER : %s' % user)
            print ('--------------------')
            print (' ')
            # logger.debug('UPDATING %s' % user)
            party = Party(user)
            party.create_or_update()
            # logger.debug('UPDATED')
            print Colorizer.Green('UPDATED %s' % user)
            print (' ')

        except Profile.DoesNotExist as e:
            print Colorizer.custom('[ERROR USER MALFORMED] : %s ' % e, 'white', 'purple')
            print (' ')

        except Exception as e:
            try:
                print Colorizer.Red('Try to exclude incompatible custom fields for user: %s' % user)
                party.safe_create_or_update()
                sanititized.append(user.email)
                print Colorizer.Yellow('UPDATED partially: %s' % user)
                print (' ')

            except Exception as safe_exc:
                print Colorizer.Red('[ ERROR IN SAFE UPDATE ] : %s' % safe_exc)
                print json.dumps(party.as_dict(), indent=1)
                print (' ')

                # logger.error('ERROR %s' % e)
                # logger.error('USER %s' % user)
                # logger.error('USER data : %s' % dumps(party.__dict__) if party else 'no data')

                print Colorizer.Red('ERROR UPDATING USER : %s' % user)
                print ('ERROR: %s' % e)
                print (' ')
                errored.append(user.email)

    # PRINT RESULTS
    print '-------------'
    print 'TOTAL RESULTS'
    print '-------------'

    if len(errored):
        print Colorizer.Red('%s errored users' % len(errored))
        # logger.error('ERROR updating users : %s' % errored)
        print errored

    if len(sanititized):
        print Colorizer.Purple('%s partially updated users : ' % len(sanititized))
        print(sanititized)

    elif not len(errored) and not len(sanititized):
        print Colorizer.Green('No errored users')
    print '-------------'
