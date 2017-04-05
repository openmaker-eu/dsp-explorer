from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dspconnector.connector import DSPConnector, DSPConnectorException


def logout_page(request):
    logout(request)
    messages.success(request, 'Bye Bye!')
    return redirect('/')


def login_page(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect("/dashboard")
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.info(request, 'Welcome %s' % user.first_name)
                return redirect('/dashboard')
            else:
                messages.error(request, 'User Invalid')
        else:
            messages.error(request, 'User not found')
    return render(request, 'dashboard/login.html', {})


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
    pagesize = 20
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    try:
        feeds = DSPConnector.get_feeds(theme_name)
        influencers = DSPConnector.get_influencers(theme_name)
    except DSPConnectorException as e:
        messages.error(request, e.message)
        feeds = []
        influencers = []

    paginator = Paginator(feeds, pagesize)
    try:
        feeds_to_show = paginator.page(page)
    except PageNotAnInteger:
        feeds_to_show = paginator.page(1)
    except EmptyPage:
        feeds_to_show = paginator.page(paginator.num_pages)
        
    context = {"theme_name": theme_name,
               "feeds": feeds_to_show,
               "influencers": influencers}
    return render(request, 'dashboard/theme.html', context)

@login_required()
def profile(request):
    context = {}
    return render(request, 'dashboard/profile.html', context)
