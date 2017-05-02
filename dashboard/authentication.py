from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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
    Profile.send_invitation(request, email, "%s %s" % (profile.user.first_name, profile.user.last_name))
    return JsonResponse({'status': 'ok', 'email': email, 'message': message}, status=200)


def reset_pwd(request, reset_token):
    pass
