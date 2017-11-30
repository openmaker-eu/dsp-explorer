from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from .models import Profile, Invitation, User
from utils.hasher import HashHelper
from utils.mailer import EmailHelper
from .serializer import ProfileSerializer
from dspconnector.connector import DSPConnector, DSPConnectorException, DSPConnectorV12, DSPConnectorV13
from utils.api import not_authorized, not_found, error, bad_request, success
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, \
    invitation_email_confirm
import json
from datetime import date, timedelta
import random, logging
from crmconnector.models import Party
from json_tricks.np import dump, dumps, load, loads, strip_comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.Colorizer import Colorizer

logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.views import View
import math

def search_members(request, search_string):

    members_per_page = 20

    # Switch between Search and last_n_users
    if search_string and search_string.strip() != '':
        results = Profile.search_members(search_string, request.GET.get('restrict_to', None))
    else:
        results = Profile.objects.all()

    count = results.count()

    # Pagination
    page = request.GET.get('page', 1)
    max_page = int(math.ceil(float(count)/float(members_per_page))) or 1

    paginator = Paginator(results, members_per_page)
    paginated_results = paginator.page(page)

    # Serialize
    serializer = ProfileSerializer(instance=paginated_results, many=True)

    # Response
    return JsonResponse({
        'status': 'ok',
        'search_string': search_string,
        'result': serializer.data,
        'page': page,
        'max_page': max_page,
        'results_count': count
    }, status=200)


def get_last_members(request):
    last_twenty = Profile.get_last_n_members(21)
    serializer = ProfileSerializer(instance=last_twenty, many=True)
    return JsonResponse({
        'status': 'ok',
        'result': serializer.data
    }, status=200)


def get_feeds(request, theme_name, date='yesterday', cursor=-1):
    try:
        feeds = DSPConnector.get_feeds(theme_name, date, cursor)
    except DSPConnectorException:
        feeds = {}
    return JsonResponse(
        {
            'status': 'ok',
            'result': feeds
        }, status=200)


def get_themes(request):
    try:
        themes = DSPConnector.get_themes()
    except DSPConnectorException:
        themes = {}
    return JsonResponse({'status': 'ok',
                         'result': themes}, status=200)


def get_influencers(request, theme_name):
    try:
        influencers = DSPConnector.get_influencers(theme_name)
    except DSPConnectorException:
        influencers = {}
    return JsonResponse({'status': 'ok',
                         'result': influencers}, status=200)


def get_hot_tags(request, tag_number=4):
    return JsonResponse({
        'status': 'ok',
        'result': [{'hashtag': t[0], 'count': t[1]} for t in Profile.get_hot_tags(tag_number)]
    }, status=200)


def get_sector(request):
    return JsonResponse(
        {'status': 'ok',
         'sectors': [
             {'name': t[0], 'size': t[1]} for t in Profile.get_sectors()]
         }, status=200)


def get_places(request):

    return JsonResponse({'status': 'ok',
                         'places': Profile.get_places()}, status=200)


def get_user_stats(request):
    n_profiles = len(Profile.objects.all())

    n_male = len(Profile.objects.filter(gender='male'))
    n_female = len(Profile.objects.filter(gender='female'))
    n_other = n_profiles - n_male - n_female

    return JsonResponse({'status': 'ok',
                         'n_profiles': n_profiles,
                         'gender_info': {'n_male': n_male, 'n_female': n_female, 'other': n_other,
                                         'n_male_%': float(n_male)*100/n_profiles,
                                         'n_female_%': float(n_female) * 100 / n_profiles,
                                         'n_other_%': float(n_other) * 100 / n_profiles},
                         }, status=200)


@csrf_exempt
def post_om_invitation(request):
    if request.method != 'POST':
        return not_authorized()
    try:
        sender_first_name = request.POST['sender_first_name'].title()
        sender_last_name = request.POST['sender_last_name'].title()
        sender_email = request.POST['sender_email'].lower()
        receiver_first_name = request.POST['receiver_first_name'].title()
        receiver_last_name = request.POST['receiver_last_name'].title()
        receiver_email = request.POST['receiver_email'].lower()
        if sender_first_name == '' or sender_last_name == '' or sender_email == '' or receiver_first_name == '' \
                or receiver_last_name == '' or receiver_email == '':
            return bad_request("Please fill al the fields")
        
        if sender_email == receiver_email:
            return bad_request("Sender and receiver must be different")
    
    except KeyError:
        return bad_request("Please fill al the fields")
    
    # sender already a DSP user?
    try:
        User.objects.get(email=sender_email)
        return HttpResponseRedirect('http://openmaker.eu/error_sender/')
    except User.DoesNotExist:
        pass
    
    # receiver already a DSP user?
    try:
        User.objects.get(email=receiver_email)
        return HttpResponseRedirect('http://openmaker.eu/error_receiver/')
    except User.DoesNotExist:
        pass
    
    # receiver already invited?
    try:
        Invitation.objects.get(receiver_email=HashHelper.md5_hash(receiver_email))
        return HttpResponseRedirect('http://openmaker.eu/error_invitation/')
    except Invitation.DoesNotExist:
        pass
    
    Invitation.create(user=None,
                      sender_email=sender_email,
                      sender_first_name=sender_first_name,
                      sender_last_name=sender_last_name,
                      receiver_first_name=receiver_first_name,
                      receiver_last_name=receiver_last_name,
                      receiver_email=receiver_email,
                      sender_verified=False
                      )
    
    activation_link = 'http://{}/om_confirmation/{}/{}/{}/{}/{}/{}'.format(
        get_current_site(request),
        sender_first_name.encode('utf-8').encode('base64'),
        sender_last_name.encode('utf-8').encode('base64'),
        sender_email.encode('base64'),
        receiver_first_name.encode('utf-8').encode('base64'),
        receiver_last_name.encode('utf-8').encode('base64'),
        receiver_email.encode('base64'))
    
    subject = 'OpenMaker Nomination.. almost done!'
    content = "{}{}{}".format(invitation_base_template_header,
                              invitation_email_confirm.format(SENDER_NAME=sender_first_name,
                                                              CONFIRMATION_LINK=activation_link),
                              invitation_base_template_footer)
    EmailHelper.send_email(
        message=content,
        subject=subject,
        receiver_email=sender_email,
        receiver_name=''
    )
    return HttpResponseRedirect('http://openmaker.eu/pending_invitation/')


def get_om_events(request):
    from django.conf import settings
    from eventbrite import Eventbrite
    eventbrite = Eventbrite(settings.ITA_API_KEY)
    try:
        ita_events = eventbrite.get('/users/me/owned_events')
        return JsonResponse({
            'status': 'ok',
            'results': {
                'italy': ita_events
            }}, status=200)
    except Exception as e:
        print e.message
        return JsonResponse({
            'status': 'error',
            'results': {}},
            status=500)

###########
# API V 1.3
###########

class v13:
    @staticmethod
    def __wrap_response(*args, **kwargs):
        try:
            results = args[0](args[1:])
        except DSPConnectorException:
            return JsonResponse({
                'status': 'error',
                'result': {}
            }, status=400)
        return JsonResponse({
            'status': 'ok',
            'result': results
        }, status=200)

    @staticmethod
    def get_influencers(request, topic_id=1, location=None):

        print location

        if not location:
            place = json.loads(request.user.profile.place)
            location = place['country_short']
        try:
            results = DSPConnectorV13.get_influencers(topic_id, location)
        except DSPConnectorException:
            results = {}
        return JsonResponse({
            'status': 'ok',
            'result': results
        }, status=200)

    @staticmethod
    def get_audiences(request, topic_id=1, location=None):
        results = {}
        if not location:
            place = json.loads(request.user.profile.place)
            location = place['country_short']
        try:
            results = DSPConnectorV13.get_audiences(topic_id, location)
        except DSPConnectorException:
            results = {}
        return JsonResponse({
            'status': 'ok',
            'result': results
        }, status=200)

    @staticmethod
    def get_events(request, topic_id, location='', cursor=0):
        try:
            events = DSPConnectorV13.get_events(topic_id, location, cursor)
        except DSPConnectorException:
            events = {}

        return JsonResponse({
            'status': 'ok',
            'result': events
        }, status=200)


    @staticmethod
    def get_hashtags(request, topic_id=1, date_string='yesterday'):
        try:
            results = DSPConnectorV13.get_hashtags(topic_id, date_string)['hashtags']
        except DSPConnectorException:
            results = {}
        return JsonResponse({
            'status': 'ok',
            'result': results
        }, status=200)

    @staticmethod
    def get_news(request, topic_id=1, date_string='yesterday', cursor=0):

        item_per_page = 20
        news = []
        next_cursor = 0
        resp = {}

        try:
            results = DSPConnectorV13.get_news(topic_id, date_string, cursor*item_per_page)
            news = results['news']
            next_cursor = results['next_cursor']/item_per_page
            resp = {'news': news, 'next_cursor': next_cursor, 'max_page': None}
        except DSPConnectorException:
            pass
        return JsonResponse({
            'status': 'ok',
            'result': resp,
            'test': results
        }, status=200)

    # @staticmethod
    # def get_themes(request):
    #     return v13.__wrap_response(v13.get_themes)


###########
# API V 1.2
###########

def get_topics(request):
    try:
        topics = DSPConnectorV12.get_topics()
    except DSPConnectorException:
        topics = {}
    return JsonResponse({
        'status': 'ok',
        'result': topics
    }, status=200)


def get_suggested_topic(request):
    try:
        topics = DSPConnectorV12.get_topics()['topics']
        random_topic = topics[random.randint(0, len(topics) - 1)]
    except DSPConnectorException:
        random_topic = {}
    return JsonResponse({
        'status': 'ok',
        'result': random_topic
    }, status=200)


def get_news(request, topic_ids, date_name='yesterday', cursor=-1):
    date_dict = {
        'yesterday': date.today() - timedelta(1),
        'week': date.today() - timedelta(7),
        'month': date.today() - timedelta(30)
    }
    try:
        since = date_dict[date_name].strftime('%d-%m-%Y')
        news = DSPConnectorV12.search_news(topic_ids, {'since': since, 'cursor': cursor})
    except DSPConnectorException:
        news = {}

    return JsonResponse({
        'status': 'ok',
        'result': news
    }, status=200)


def get_events(request, topic_ids, cursor=-1):
    try:
        events = DSPConnectorV12.get_events(topic_ids, cursor)
    except DSPConnectorException:
        events = {}

    return JsonResponse({
        'status': 'ok',
        'result': events
    }, status=200)


def get_audiences(request, topic_id):
    try:
        audiences = DSPConnectorV12.get_audiences(topic_id)
    except DSPConnectorException:
        audiences = {}
    return JsonResponse({
        'status': 'ok',
        'result': audiences
    }, status=200)


def update_field(request, to_be_updated, update_token):
    import threading

    if not update_token == settings.UPDATE_TOKEN:
        return not_authorized()

    if to_be_updated == 'crm':
        users = User.objects.all()
        thr = threading.Thread(target=create_or_update_party, kwargs=dict(users=users))
        thr.start()

    if to_be_updated == 'default_img':
        # update default images
        users = User.objects.all()
        thr = threading.Thread(target=update_default_profile_image, kwargs=dict(users=users))
        thr.start()

    return JsonResponse({'status': 'ok', 'updating': to_be_updated}, status=200)


def update_default_profile_image(users):
    print 'update_default_profile_image'
    errored = []
    sanititized = []
    for user in users:
        try:
            if user.profile.picture == 'images/profile/default_user_icon.png':
                print ('--------------------')
                print ('UPDATING USER : %s' % user)
                print ('--------------------')
                print (' ')
                if user.profile.gender == 'male': user.profile.picture = 'images/profile/male.svg'
                if user.profile.gender == 'female': user.profile.picture = 'images/profile/female.svg'
                if user.profile.gender == 'other': user.profile.picture = 'images/profile/other.svg'
                sanititized.append(user.email)
                user.profile.save()
        except Profile.DoesNotExist as e:
            errored.append(user.email)
            print Colorizer.custom('[ERROR USER MALFORMED] : %s ' % e, 'white', 'purple')
            print (' ')
    # PRINT RESULTS
    print '-------------'
    print 'TOTAL RESULTS'
    print '-------------'

    if len(errored):
        print Colorizer.Red('%s errored users' % len(errored))
        print errored

    if len(sanititized):
        print Colorizer.Purple('%s updated users : ' % len(sanititized))
        print(sanititized)

    elif not len(errored) and not len(sanititized):
        print Colorizer.Green('no updates or errors')
    print '-------------'


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
