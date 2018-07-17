from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Twitter, TwitterProfile
from dashboard.models import Profile
from django.http import *
from django.urls import reverse
from django.contrib import messages
import requests
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs
import json
from utils.helpers import get_host


@login_required
def twitter_sign_in(request):
    # DOC https://dev.twitter.com/web/sign-in/implementing
    url = "https://api.twitter.com/oauth/request_token"
    twitter = Twitter.objects.first()
    oauth = OAuth1(twitter.app_id, client_secret=twitter.app_secret)
    response = requests.post(url=url, auth=oauth)
    credentials = parse_qs(response.text)
    print(credentials)
    oauth_callback_confirmed = credentials.get('oauth_callback_confirmed')[0]
    if not oauth_callback_confirmed:
        messages.warning(request, 'Error during Twitter login.')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    oauth_token = credentials.get('oauth_token')[0]
    redirect_url = "https://api.twitter.com/oauth/authenticate?oauth_token={}".format(oauth_token)
    return HttpResponseRedirect(redirect_url)


@login_required
def twitter_redirect(request):
    twitter = Twitter.objects.first()
    try:
        oauth_token, oauth_token_secret = _exchange_code_for_twitter_token(twitter.app_id,
                                                                           twitter.app_secret,
                                                                           request.GET.get('oauth_token'),
                                                                           request.GET.get('oauth_verifier'))
    except Exception as e:
        messages.error(request, 'Error during Twitter login.')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    if not oauth_token_secret or not oauth_token:
        messages.success(request, 'Error during Twitter login.')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    profile = Profile.objects.filter(user__email=request.user.email).first()
    twitter_profile = TwitterProfile.create(profile, oauth_token, oauth_token_secret)
    messages.success(request, 'Link with your Twitter profile completed.')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))


def _exchange_code_for_twitter_token(app_id=None, app_secret=None, resource_owner_key=None, resource_owner_secret=None):
    if not resource_owner_key or not resource_owner_secret:
        return None, None
    url = "https://api.twitter.com//oauth/access_token"
    try:
        oauth = OAuth1(app_id, app_secret, resource_owner_key=resource_owner_key,
                       resource_owner_secret=resource_owner_secret)
        response = requests.post(url=url, auth=oauth, data={"oauth_verifier": resource_owner_secret})
        credentials = parse_qs(response.text)
        print("###########")
        print(credentials)
        print("###########")
        oauth_token = credentials.get('oauth_token')[0]
        oauth_token_secret = credentials.get('oauth_token_secret')[0]
    except Exception as e:
        raise e
    return oauth_token, oauth_token_secret


def _twitter_get_data(user_id, app_id, app_secret, oauth_token, oauth_secret):
    import tweepy
    try:
        auth = tweepy.OAuthHandler(app_id, app_secret)
        auth.set_access_token(oauth_token, oauth_secret)
        api = tweepy.API(auth)
        user = api.me()
        user_object = user._json
        user_object['friends_list'] = [f.screen_name for f in api.friends()]
        MongoWrapper.update_user(user_id, {"twitter": user_object})
    except Exception as e:
        raise e


@login_required()
def deactivate_account(request, social):
    profile = Profile.objects.filter(user__email=request.user.email).first()
    if social == 'twitter':
        profile.twitter = False
        profile.save()
        TwitterProfile.objects.filter(profile=profile).delete()
    messages.success(request, 'You have unlinked your profile')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))

# Create your views here.
