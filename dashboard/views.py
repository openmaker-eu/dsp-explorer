from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dspconnector.connector import DSPConnector, DSPConnectorException
from .models import Profile


@login_required()
def dashboard(request):
    try:
        context = {"themes": DSPConnector.get_themes()}
    except DSPConnectorException as e:
        context = {"themes": []}
        messages.error(request, e.message)
    return render(request, 'dashboard/dashboard.html', context)


@login_required()
def theme(request, theme_name):
    try:
        feeds = DSPConnector.get_feeds(theme_name)
        influencers = DSPConnector.get_influencers(theme_name)
    except DSPConnectorException as e:
        messages.error(request, e.message)
        feeds = []
        influencers = []

    context = {"theme_name": theme_name,
               "feeds": feeds['feeds'],
               "influencers": influencers['influencers']}
    return render(request, 'dashboard/theme.html', context)


@login_required()
def profile(request):
    try:
        profile = Profile.objects.get(user__email=request.user.email)
    except:
        profile = {}
    context = {"profile": profile}
    return render(request, 'dashboard/profile.html', context)


@login_required()
def search_members(request):
    return render(request, 'dashboard/search_members.html', {})