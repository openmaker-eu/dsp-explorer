# coding=utf-8
from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
import datetime as dt
from utils.mailer import EmailHelper
from .models import Profile, User, Invitation, Tag
from crmconnector import capsule
import pytz
import logging
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime
from utils.hasher import HashHelper
from utils.generic import *
import json
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, \
    invitation_email_confirmed, invitation_email_receiver, onboarding_email_template, authentication_reset_password
import re
from django.utils.encoding import force_unicode

from crmconnector.models import Party
from rest_framework.exceptions import NotFound

logger = logging.getLogger(__name__)
from dashboard.exceptions import EmailAlreadyUsed, UserAlreadyInvited, SelfInvitation, InvitationAlreadyExist, InvitationDoesNotExist



def logout_page(request):
    logout(request)
    messages.success(request, 'Bye Bye!')
    return HttpResponseRedirect(reverse('dashboard:login'))


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.info(request, 'Welcome %s' % user.first_name.encode('utf-8'))
                return HttpResponseRedirect(reverse('dashboard:dashboard'))
            else:
                messages.error(request, 'User Invalid')
        else:
            messages.error(request, 'Username or password are wrong!')
    return render(request, 'dashboard/login.html', {})


def recover_pwd(request):
    """
    Method used to ask for a reset password
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    if request.POST:
        username = request.POST['email']
        try:
            profile = Profile.get_by_email(username)

            # Check if user is active
            if not profile.user.is_active:
                messages.error(request, 'Your user is not yet active, '
                               'please complete the activation process before requesting a new password')
                return HttpResponseRedirect(reverse('dashboard:login'))

            profile.reset_token = Profile.get_new_reset_token()
            profile.ask_reset_at = dt.datetime.now()
            profile.save()

            # send e-mail
            email_body = authentication_reset_password.format(
                FIRST_NAME=profile.user.first_name.encode('utf-8'),
                LAST_NAME=profile.user.last_name.encode('utf-8'),
                BASE_URL=get_current_site(request),
                TOKEN=profile.reset_token
            )
            email_content = "{0}{1}{2}".format(
                invitation_base_template_header,
                email_body,
                invitation_base_template_footer
            )
            EmailHelper.send_email(
                message=email_content,
                subject='DSPExplorer - Reset Password',
                receiver_email=profile.user.email
            )

            messages.success(request, 'You will receive an email with a link to reset your password!')
            return HttpResponseRedirect(reverse('dashboard:login'))
        except Profile.DoesNotExist:
            messages.error(request, 'User not Found.')
            return HttpResponseRedirect(reverse('dashboard:login'))
    return render(request, 'dashboard/recover_pwd.html', {})


def reset_pwd(request, reset_token):
    """
    Method used to reset the password
    :param request:
    :param reset_token:
    :return:
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    try:
        profile = Profile.objects.filter(reset_token=reset_token).get()
    except Profile.DoesNotExist:
        messages.error(request, 'User Not Found!')
        return HttpResponseRedirect(reverse('dashboard:login'))
    seven_days_ago = timezone.now() - dt.timedelta(days=7)
    if profile.ask_reset_at < seven_days_ago:
        messages.error(request, 'Token Expired, Please try asking to reset your password.')
        return HttpResponseRedirect(reverse('dashboard:login'))
    
    if request.POST:
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        if password != repeat_password:
            messages.warning(request, 'Attention, Password must be equals!')
            return HttpResponseRedirect(reverse('dashboard:reset_pwd', kwargs={'reset_token': reset_token}))
        if len(password) < 8:
            messages.warning(request, 'Attention, Please insert at least 8 characters!')
            return HttpResponseRedirect(reverse('dashboard:reset_pwd', kwargs={'reset_token': reset_token}))

        # Check if user is active
        if not profile.user.is_active:
            messages.error(request, 'Your user is not yet active, '
                           'please complete the activation process before requesting a new password')
            return HttpResponseRedirect(reverse('dashboard:login'))

        profile.user.set_password(password)
        profile.user.is_active = True
        profile.user.save()
        profile.ask_reset_at = None
        profile.reset_token = None
        profile.update_token_at = dt.datetime.now()
        profile.save()
        messages.success(request, 'Password reset completed!')
        return HttpResponseRedirect(reverse('dashboard:login'))
    return render(request, 'dashboard/reset_pwd.html', {"profile": profile, "reset_token": reset_token})


def onboarding(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    if request.method == 'POST':
        try:
            email = request.POST['email'].lower()
            pasw = request.POST['password']
            pasw_confirm = request.POST['password_confirm']
            first_name = request.POST['first_name'].title()
            last_name = request.POST['last_name'].title()
            gender = request.POST['gender']
            birthdate_dt = datetime.strptime(request.POST['birthdate'], '%Y/%m/%d')
            birthdate_dt = pytz.utc.localize(birthdate_dt)
            city = request.POST['city']
            occupation = request.POST['occupation']
            tags = request.POST['tags']

            place = request.POST.get('place', None) if request.POST.get('place', None) != '{}' else None

            if tags == '' or tags == None or tags == 'undefined':
                raise KeyError

            twitter_username = request.POST.get('twitter', '')
        except ValueError:
            messages.error(request, 'Incorrect birthdate format: it must be YYYY/MM/DD')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        except KeyError:
            messages.error(request, 'Please fill the required fields!')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))

        # check password
        if pasw != pasw_confirm:
            messages.error(request, 'Password and confirm password must be the same')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))

        # check birthdate
        if birthdate_dt > pytz.utc.localize(datetime(dt.datetime.now().year - 13, *birthdate_dt.timetuple()[1:-2])):
            messages.error(request, 'You must be older than thirteen')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))

        # Check image and get url
        if gender == 'male': imagefile = 'images/profile/male.svg'
        if gender == 'female': imagefile = 'images/profile/female.svg'
        if gender == 'other': imagefile = 'images/profile/other.svg'


        # Check if user exist
        try:
            User.objects.get(email=email)
            messages.error(request, 'User is already a DSP member!')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        except User.DoesNotExist:
            pass

        # profile create
        try:
            profile = Profile.create(email, first_name, last_name, imagefile, pasw, gender, birthdate_dt,
                                     city, occupation, twitter_username, place)
        except Exception as exc:
            logging.error('[PROFILE_CREATION_ERROR] Error during local profile creation for user email: {USER} , EXCEPTION {EXC}'.format(USER=email, EXC=exc))
            messages.error(request, 'Error creating user')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))

        # Add tags to profile
        # @TODO : handle tag Creation exception
        for tag in map(lambda x: re.sub(r'\W', '', x.lower().capitalize(), flags=re.UNICODE), tags.split(",")):
            tagInstance = Tag.objects.filter(name=tag).first() or Tag.create(name=tag)
            profile.tags.add(tagInstance)
        profile.save()

        # Add twitter username to social links
        social_links = json.loads(profile.socialLinks)
        social_links[0]['link'] = twitter_username
        profile.socialLinks = json.dumps(social_links)
        profile.save()

        # send e-mail
        confirmation_link = request.build_absolute_uri('/onboarding/confirmation/{TOKEN}'.format(TOKEN=profile.reset_token))

        subject = 'Onboarding... almost done!'
        content = "{0}{1}{2}".format(
            invitation_base_template_header,
            onboarding_email_template.format(
                FIRST_NAME=first_name.encode('utf-8'),
                LAST_NAME=last_name.encode('utf-8'),
                CONFIRMATION_LINK=confirmation_link,
            ),
            invitation_base_template_footer)

        EmailHelper.send_email(
            message=content,
            subject=subject,
            receiver_email=email
        )

        messages.success(request, 'Confirmation mail sent!')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    return render(request, 'dashboard/onboarding.html', {'tags': json.dumps(map(lambda x: x.name, Tag.objects.all()))})


def onboarding_confirmation(request, token):
    # Check for token
    try:
        profile = Profile.objects.get(reset_token=token)
    except Profile.DoesNotExist:
        messages.error(request, 'Token expired')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    # update on crm
    try:
        party = Party(profile.user)
        party.create_or_update()
    except NotFound as e:
        messages.error(request, 'There was some connection problem, please try again')
        logger.debug('CRM CREATION USER CONNECTION ERROR %s' % e)
        return HttpResponseRedirect(reverse('dashboard:profile'))
    except Exception as e:
        logger.debug('CRM CREATION USER ERROR %s' % e)
        return HttpResponseRedirect(reverse('dashboard:profile'))


    profile.user.is_active = True
    profile.user.save()
    profile.update_reset_token()
    login(request, profile.user)
    # Modal creation after first login
    body = '' \
           '<div class="row">' \
           '<div class="col-md-12 text-center margin-top-30 margin-bottom-30">' \
           '<p class="margin-bottom-30">Start discover the community and build great projects!</br>Remember to <strong>nominate</strong> your friends!</p>' \
           '<div class="col-md-6 text-center">' \
           '<a href="{EXPLORE_LINK}" class="btn login-button">Start exploring</a>' \
           '</div>' \
           '<div class="col-md-6 text-center">' \
           '<a href="{INVITE_LINK}" class="btn login-button">Invite a friend</a>' \
           '</div>' \
           '</div></div>'.format(EXPLORE_LINK=reverse('dashboard:dashboard'), INVITE_LINK=reverse('dashboard:invite'))

    modal_options = {
        "title": "Welcome onboard %s!" % force_unicode(profile.user.first_name),
        "body": escape_html(body),
        "footer": False
    }
    messages.info(request, json.dumps(modal_options), extra_tags='modal')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))


def om_confirmation(
        request,
        sender_first_name,
        sender_last_name,
        sender_email,
        receiver_first_name,
        receiver_last_name,
        receiver_email
):

    # sender
    sender_first_name = sender_first_name.decode('base64')
    sender_last_name = sender_last_name.decode('base64')
    sender_email = sender_email.decode('base64')

    # receiver
    receiver_first_name = receiver_first_name.decode('base64')
    receiver_last_name = receiver_last_name.decode('base64')
    receiver_email = receiver_email.decode('base64')

    try:
        Invitation.confirm_sender(sender_email=sender_email, receiver_email=receiver_email)
    except SelfInvitation as e:
        messages.error(request, 'You can\'t invite youself!')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    except EmailAlreadyUsed as e:
        messages.error(request, 'User is already a DSP member!')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    except UserAlreadyInvited as e:
        messages.error(request, 'You have already invite this user!')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    # Emails
    try:
        # Invitation email already sent
        Invitation.objects.get(receiver_email=HashHelper.md5_hash(receiver_email))
    except Invitation.DoesNotExist:
        # Send email for the first time
        EmailHelper.email(
            template_name='invitation_email_receiver',
            title='You are invited to join the OpenMaker community!',
            vars={
                'RECEIVER_FIRST_NAME': receiver_first_name.encode('utf-8'),
                'RECEIVER_LAST_NAME': receiver_last_name.encode('utf-8'),
                'SENDER_FIRST_NAME': sender_first_name.encode('utf-8'),
                'SENDER_LAST_NAME': sender_last_name.encode('utf-8'),
                'ONBOARDING_LINK': request.build_absolute_uri('/onboarding/')
            },
            receiver_email=receiver_email
        )

    EmailHelper.email(
        template_name='invitation_email_confirmed',
        title='OpenMaker Nomination done!',
        vars={'ONBOARDING_LINK': request.build_absolute_uri('/onboarding/')},
        receiver_email=sender_email
    )

    return HttpResponseRedirect('http://openmaker.eu/confirmed/')

    # try:
    #     # Check if invited user exist, if exist raise error?
    #     User.objects.get(email=receiver_email)
    #     messages.error(request, 'User is already a DSP member!')
    #     return HttpResponseRedirect(reverse('dashboard:dashboard'))
    # except User.DoesNotExist:
    #     pass
    #
    # try:
    #     # Check invitaion exist if does not exist raise error
    #     invitation = Invitation.objects.get(
    #         sender_email=HashHelper.md5_hash(sender_email),
    #         receiver_email=HashHelper.md5_hash(receiver_email)
    #     )
    #
    #     # Check if invitation is already send, if exist raise error
    #     if invitation.sender_verified:
    #         messages.error(request, 'Invitation already sent!')
    #     else:
    #         # invitation flow start
    #         invitation.sender_verified = True
    #         invitation.save()
    #
    #         # sending invitation mail
    #         subject = 'OpenMaker Nomination done!'
    #         content = "{0}{1}{2}".format(
    #             invitation_base_template_header,
    #             invitation_email_confirmed.format(
    #                 ONBOARDING_LINK=request.build_absolute_uri('/onboarding/')
    #             ),
    #             invitation_base_template_footer
    #         )
    #
    #         EmailHelper.send_email(
    #             message=content,
    #             subject=subject,
    #             receiver_email=sender_email,
    #             receiver_name=''
    #         )
    #
    #         subject = 'You are invited to join the OpenMaker community!'
    #         content = "{0}{1}{2}".format(
    #             invitation_base_template_header,
    #             invitation_email_receiver.format(
    #                 RECEIVER_FIRST_NAME=receiver_first_name.encode('utf-8'),
    #                 RECEIVER_LAST_NAME=receiver_last_name.encode('utf-8'),
    #                 SENDER_FIRST_NAME=sender_first_name.encode('utf-8'),
    #                 SENDER_LAST_NAME=sender_last_name.encode('utf-8'),
    #                 ONBOARDING_LINK=request.build_absolute_uri('/onboarding/')),
    #             invitation_base_template_footer
    #         )
    #
    #         EmailHelper.send_email(
    #             message=content,
    #             subject=subject,
    #             receiver_email=receiver_email,
    #             receiver_name=''
    #         )
    #         messages.success(request, 'Invitation complete!')
    #
    # except Invitation.DoesNotExist:
    #     messages.error(request, 'Invitation does not exist')
    return HttpResponseRedirect('http://openmaker.eu/confirmed/')


def csrf_failure(request, reason=''):
    messages.warning(request, 'Some error occurs!')
    return HttpResponseRedirect(reverse('dashboard:login'))
