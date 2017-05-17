from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.mailer import EmailHelper
from dspconnector.connector import DSPConnector, DSPConnectorException
from .models import Profile
from django.http import HttpResponseRedirect


@login_required()
def dashboard(request):
    try:
        context = {'themes': DSPConnector.get_themes()}
    except DSPConnectorException as e:
        context = {'themes': []}
        messages.error(request, e.message)
    return render(request, 'dashboard/dashboard.html', context)


@login_required()
def theme(request, theme_name):
    try:
        feeds = DSPConnector.get_feeds(theme_name)
        influencers = DSPConnector.get_influencers(theme_name)
        themes = DSPConnector.get_themes()
        themes_list = [t.get('name', '') for t in themes.get('themes', []) if t.get('name', '') != theme_name]
    except DSPConnectorException as e:
        messages.error(request, e.message)
        feeds = []
        influencers = []
        themes_list = []

    context = {'theme_name': theme_name,
               'feeds': feeds.get('feeds', []),
               'themes': themes_list,
               'influencers': influencers.get('influencers', [])}
    return render(request, 'dashboard/theme.html', context)


@login_required()
def profile(request, profile_id=None):
    try:
        if profile_id:
            user_profile = Profile.get_by_id(profile_id)
        else:
            user_profile = Profile.get_by_email(request.user.email)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    context = {'profile': user_profile}
    return render(request, 'dashboard/profile.html', context)


@login_required()
def search_members(request):
    return render(request, 'dashboard/search_members.html', {})


@login_required()
def invite(request):
    subject = 'INVITATION on Driver Social Platform'
    content = 'Congratulation your friends ... invite you to join in!!'

    if request.method == 'POST':
        address = request.POST.get('email', '')
        try:
            Profile.get_by_email(address)
            messages.error(request, 'User already present!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except Profile.DoesNotExist:
            pass

        try:
            EmailHelper.send_email(
                message=content,
                subject=subject,
                receiver_email=address,
                receiver_name=''
            )
            messages.success(request, 'Invitation sent!')
        except:
            messages.error(request, 'Please try again!')
    return render(request, 'dashboard/invite.html', {})


def support(request):
    return render(request, 'dashboard/FAQpage.html', {})
