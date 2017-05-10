from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from dspconnector.connector import DSPConnector, DSPConnectorException
from .models import Profile
from django.http import HttpResponseRedirect


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
def profile(request, profile_id=None):
    try:
        if profile_id:
            user_profile = Profile.get_by_id(profile_id)
        else:
            user_profile = Profile.get_by_email(request.user.email)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    context = {"profile": user_profile}
    return render(request, 'dashboard/profile.html', context)


@login_required()
def search_members(request):
    return render(request, 'dashboard/search_members.html', {})


@login_required()
def invite(request):
    # static variables
    invitation_field = "INVITATION on Driver Social Platform"
    content_field = "Congratulation your friends ... invite you to join in!!"

    if request.method == 'POST':
        print 'into post'
        # show alert success sent top-right
        # send email to request.form['email']
        addressee = request.POST.get('email', '')
        # print addressee

        #trouble 
        send_mail(invitation_field, content_field, 'mauriziocontatto@gmail.com', [addressee], fail_silently=False)

        return render(request, 'dashboard/invite.html', {'message': "Mail Sent!"})

    else:
        print 'into get'
        return render(request, 'dashboard/invite.html', {})
