from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .models import Profile, Invitation, User
from utils.hasher import HashHelper
from utils.mailer import EmailHelper
from .serializer import ProfileSerializer
from dspconnector.connector import DSPConnector, DSPConnectorException
from utils.api import *
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, \
    invitation_email_confirm
import json

def search_members(request, search_string):
    result = Profile.search_members(search_string)
    serializer = ProfileSerializer(instance=result, many=True)
    return JsonResponse({'status': 'ok',
                         'search_string': search_string,
                         'result': serializer.data}, status=200)


def get_last_members(request):
    last_twenty = Profile.get_last_n_members(21)
    serializer = ProfileSerializer(instance=last_twenty, many=True)
    return JsonResponse({'status': 'ok',
                         'result': serializer.data}, status=200)


def get_feeds(request, theme_name, date='yesterday', cursor=-1):
    try:
        feeds = DSPConnector.get_feeds(theme_name, date, cursor)
    except DSPConnectorException:
        feeds = {}
    return JsonResponse({'status': 'ok',
                         'result': feeds}, status=200)


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
    return JsonResponse({'status': 'ok',
                         'tags': [
                             {'name': t[0], 'size': t[1]} for t in Profile.get_hot_tags(tag_number)]}, status=200)


def get_sector(request):
    return JsonResponse({'status': 'ok',
                         'sectors': [
                             {'name': t[0], 'size': t[1]} for t in Profile.get_sectors()]}, status=200)
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

