from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def logout_page(request):
    logout(request)
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/dashboard")
    username = password = ''
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/dashboard')
    return render(request, 'dashboard/login.html', {})


@login_required()
def dashboard(request):
    # context = {"user": request.user}
    return render(request, 'dashboard/dashboard.html')
