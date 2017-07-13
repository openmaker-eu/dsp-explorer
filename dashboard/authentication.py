from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
import datetime as dt
from utils.mailer import EmailHelper
from .models import Profile, User

from crmconnector import capsule

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import logging
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime

from utils.emailtemplate import \
    invitation_base_template_header, \
    invitation_base_template_footer, \
    onboarding_email_template


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
                messages.info(request, 'Welcome %s' % user.first_name)
                return HttpResponseRedirect(reverse('dashboard:dashboard'))
            else:
                messages.error(request, 'User Invalid')
        else:
            messages.error(request, 'User not found')
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
            profile.reset_token = Profile.get_new_reset_token()
            profile.ask_reset_at = dt.datetime.now()
            profile.save()
            email_message = """
DSPExplorer - Open Maker
Hi {email}, to reset you password, click here:

http://{baseurl}/reset_password/{token}
            """.format(email=profile.user.email,
                       baseurl=get_current_site(request),
                       token=profile.reset_token)
            profile.send_email('DSPExplorer - Reset Password', email_message)
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
    if request.method == 'POST':
        try:
            email = request.POST['email']
            pasw = request.POST['password']
            pasw_confirm = request.POST['password_confirm']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            gender = request.POST['gender']
            birthdate_dt = datetime.strptime(request.POST['birthdate'], '%Y/%m/%d')
            city = request.POST['city']
            occupation = request.POST['occupation']
            tags = request.POST['tags']
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

        # Check image and get url
        try:
            file = request.FILES['profile_img']
            filename, file_extension = os.path.splitext(file.name)

            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if not (file_extension in allowed_extensions):
                raise ValueError
            imagename = str(datetime.now().microsecond) + '_' + str(file._size) + file_extension
            imagepath = default_storage.save('{CURRENT_SITE}/static/images/profile/{IMAGE}'.format(
                CURRENT_SITE=get_current_site(request),
                IMAGE=imagename
            ), ContentFile(file.read()))
        except ValueError:
            messages.error(request, 'Profile Image is not an image file')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        except:
            imagepath = '{CURRENT_SITE}/static/user_icon.png'.format(CURRENT_SITE=get_current_site(request))

        # Check if user exist
        try:
            User.objects.get(email=email)
            messages.error(request, 'User is already a DSP member!')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        except User.DoesNotExist:
            pass

        # profile create
        try:
            profile = Profile.create(email, first_name, last_name, imagepath, pasw, gender, birthdate_dt,
                                     city, occupation, tags, twitter_username)
        except Exception as exc:
            messages.error(request, 'Error creating user')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))

        confirmation_link = '{CURRENT_SITE}/onboarding/confirmation/{TOKEN}'.format(
            TOKEN=profile.reset_token,
            CURRENT_SITE=get_current_site(request)
        )

        # send e-mail
        subject = 'Onboarding... almost done!'
        content = "{}{}{}".format(invitation_base_template_header,
                                  onboarding_email_template.format(FIRST_NAME=first_name,
                                                                   LAST_NAME=last_name,
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

    return render(request, 'dashboard/onboarding.html', {})



def onboarding_confirmation(request, token):
    # Check for token
    try:
        profile = Profile.objects.get(reset_token=token)
    except Profile.DoesNotExist:
        messages.error(request, 'Token expired')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    #Check for user on Capsupe CRM
    user = capsule.CRMConnector.search_party_by_email(profile.user.email)
    if user:
        try:
            update_user = capsule.CRMConnector.update_party(user['id'], {'party': {
                'emailAddresses': [{'address': profile.user.email}],
                'type': 'person',
                'firstName': profile.user.first_name,
                'lastName': profile.user.last_name,
                'jobTitle': profile.occupation,
                'pictureURL': profile.picture_url
            }
            })
        except:
            messages.error(request, 'Some error occures, please try again!')
            logging.error('[VALIDATION_ERROR] Error during CRM Creation for user: %s' % profile.user.id)
            # TODO SEND ERROR EMAIL TO ADMIN
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
    else:
        try:
            capsule.CRMConnector.add_party({'party': {
                'emailAddresses': [{'address': profile.user.email}],
                'type': 'person',
                'firstName': profile.user.first_name,
                'lastName': profile.user.last_name,
                'jobTitle': profile.occupation,
                'pictureURL': profile.picture_url
            }
            })
        except:
            messages.error(request, 'Some error occures, please try again!')
            logging.error('[VALIDATION_ERROR] Error during CRM Creation for user: %s' % profile.user.id)
            # TODO SEND ERROR EMAIL TO ADMIN
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
    profile.user.is_active = True
    profile.user.save()
    profile.update_reset_token()
    messages.success(request, 'Your account is now active. Please login with your credentials!')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))
