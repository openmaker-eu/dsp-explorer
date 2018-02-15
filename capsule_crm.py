import os
import sys
import django

sys.path.append("/dspexplorer/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'dspexplorer.settings'
django.setup()

from dashboard.models import User, Profile
import json
from crmconnector.models import Party
from utils.Colorizer import Colorizer
from crmconnector.capsule import CRMValidationException

def update_crm(user=None):
    errored = []
    partially_updated = []
    party = None

    users = user or User.objects.all()

    for user in users:
        try:
            print ('--------------------')
            print ('UPDATING USER : %s' % user)
            print ('--------------------')
            print (' ')
            party = Party(user)
            party.create_or_update()
            print Colorizer.Green('UPDATED %s' % user)
            print (' ')

        except Profile.DoesNotExist as e:
            print Colorizer.custom('[ERROR USER MALFORMED] : %s ' % e, 'white', 'purple')
            print (' ')

        except CRMValidationException as e:
            try:
                print Colorizer.Red('Try to exclude incompatible custom fields for user: %s' % user)
                party.safe_create_or_update()
                partially_updated.append(user.email)
                print Colorizer.Yellow('UPDATED partially: %s' % user)
                print (' ')

            except Exception as safe_exc:
                print Colorizer.Red('[ ERROR IN SAFE UPDATE ] : %s' % safe_exc)
                print json.dumps(party.as_dict(), indent=1)
                print (' ')

                print Colorizer.Red('ERROR UPDATING USER : %s' % user)
                print ('ERROR: %s' % e)
                print (' ')
                errored.append(user.email)

        except Exception as e:
            print Colorizer.Red('ERROR UPDATING USER : %s' % user)
            print ('ERROR: %s' % e)
            print (' ')

    return errored, partially_updated


def print_results(errored=None, partially_updated=None):
    # PRINT RESULTS
    print '-------------'
    print 'TOTAL RESULTS'
    print '-------------'

    if len(errored):
        print Colorizer.Red('%s errored users' % len(errored))
        # logger.error('ERROR updating users : %s' % errored)
        print errored

    if len(partially_updated):
        print Colorizer.Purple('%s partially updated users : ' % len(partially_updated))
        print(partially_updated)

    elif not len(errored) and not len(partially_updated):
        print Colorizer.Green('No errored users')
    print '-------------'


def get_test_user(user_email):
    user = User.objects.filter(email=user_email)
    return user if len(user) > 0 else User.objects.filter(email='massimo.santoli@top-ix.org')


def pair_crm_ids():
    users = User.objects.all()
    for u in users:
        try:
            party = Party(u)
            party_crm_id = party.get()['id']
            profile = Profile.get_by_email(u)
            profile.set_crm_id(party_crm_id)
        except Exception as e:
            print 'PAIR CRM IDs %s' % u
            print 'PAIR CRM IDs %s' % e

    sys.exit("Paring finished")


if __name__ == "__main__":
    pair_crm_ids() if len(sys.argv) > 1 and sys.argv[1] == 'pair_crm_ids' else None
    user = get_test_user(sys.argv[1]) if len(sys.argv) > 1 else None
    if len(user) > 0:
        errored, partially_updated = update_crm(user)
        print_results(errored, partially_updated)
    else:
        print Colorizer.Red('No user found')
