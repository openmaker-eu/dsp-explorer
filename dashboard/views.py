from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.mailer import EmailHelper
from utils.hasher import HashHelper
from dspconnector.connector import DSPConnector, DSPConnectorException
from .models import Profile, Invitation, Feedback
from .exceptions import EmailAlreadyUsed, UserAlreadyInvited
from django.http import HttpResponseRedirect
from form import FeedbackForm
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, invitation_email_receiver


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
        themes = DSPConnector.get_themes()
        themes_list = [t.get('name', '') for t in themes.get('themes', []) if t.get('name', '') != theme_name]
    except DSPConnectorException as e:
        messages.error(request, e.message)
        themes_list = {}
    
    context = {'theme_name': theme_name,
               'themes': themes_list}
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
    if request.method == 'POST':
        try:
            address = request.POST['email']
            first_name = request.POST['first_name'].title()
            last_name = request.POST['last_name'].title()
        except KeyError:
            messages.error(request, 'Please all the fields are required!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        
        try:
            User.objects.get(email=address)
            messages.error(request, 'User is already a DSP member!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except User.DoesNotExist:
            pass
        
        try:
            Invitation.objects.get(receiver_email=HashHelper.md5_hash(address))
            messages.error(request, 'User is been already invited!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except Invitation.DoesNotExist:
            pass
        
        # email not present, filling invitation model
        try:
    
            Invitation.create(user=request.user,
                              sender_email=request.user.email,
                              sender_first_name=request.user.first_name,
                              sender_last_name=request.user.last_name,
                              receiver_first_name=first_name,
                              receiver_last_name=last_name,
                              receiver_email=address,
                              )

            subject = 'You are invited to join the OpenMaker community!'
            content = "{}{}{}".format(invitation_base_template_header,
                                      invitation_email_receiver.format(RECEIVER_FIRST_NAME=first_name,
                                                                       RECEIVER_LAST_NAME=last_name,
                                                                       SENDER_FIRST_NAME=request.user.first_name,
                                                                       SENDER_LAST_NAME=request.user.last_name,
                                                                       ONBOARDING_LINK=request.build_absolute_uri('/onboarding/')),
                                      invitation_base_template_footer)

            EmailHelper.send_email(
                message=content,
                subject=subject,
                receiver_email=address,
                receiver_name=''
            )
            messages.success(request, 'Invitation sent!')
        except EmailAlreadyUsed:
            messages.error(request, 'User is already a member!')
        except UserAlreadyInvited:
            messages.error(request, 'User has already received an invitation!')
        except Exception as e:
            print e.message
            messages.error(request, 'Please try again!')
    
    return render(request, 'dashboard/invite.html', {})


@login_required()
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                Feedback(user=request.user, title=request.POST['title'],
                         message_text=request.POST['message_text']).save()
                messages.success(request, 'Thanks for your feedback!')
            except KeyError:
                messages.warning(request, 'Error, please try again.')
        else:
            messages.error(request, 'Please all the fields are required!')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))