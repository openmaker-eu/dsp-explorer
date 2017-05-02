from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
import datetime as dt
from crmconnector.capsule import CRMConnector
from .models import Profile
from .exceptions import EmailAlreadyUsed


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


def request_membership(request, email):
    party = CRMConnector.search_party_by_email(email)
    if not party:
        return JsonResponse({'status': 'error', 'message': 'User not Found'}, status=404)
    try:
        profile = Profile.create(email, party['firstName'], party['lastName'], party['pictureURL'])
    except EmailAlreadyUsed:
        return JsonResponse({'status': 'error', 'message': 'Email already present'}, status=409)
    message = 'Invitation sent!'
    subject_for_email = 'Welcome to DSP Explorer - Open Maker'
    message_for_email = 'Welcome! Click this link to create your account ' \
                        'http://{}/reset_password/{}'.format(get_current_site(request), profile.reset_token)
    profile.send_email(subject_for_email, message_for_email)
    return JsonResponse({'status': 'ok', 'email': email, 'message': message}, status=200)


def recover_pwd(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    if request.POST:
        username = request.POST['email']
        try:
            profile = Profile.objects.filter(user__email=username).get()
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
        except Profile.DoesNotExist:
            messages.error(request, 'User not Found.')
            return HttpResponseRedirect(reverse('dashboard:login'))
    return HttpResponseRedirect(reverse('dashboard:login'))


def reset_pwd(request, reset_token):
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
            return HttpResponseRedirect(reverse('dashboard:login', kwargs={'reset_token': reset_token}))
        if len(password) < 8:
            messages.warning(request, 'Attention, Please insert at least 8 characters!')
            return HttpResponseRedirect(reverse('dashboard:login', kwargs={'reset_token': reset_token}))
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
