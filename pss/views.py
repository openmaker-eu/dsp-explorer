from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import *
from django.contrib import messages
from django.urls import reverse
from .models import Application
from dashboard.models import Profile
import logging


@login_required
def application(request):
    if request.method == 'POST':
        try:
            project_name = request.POST['project_name'].strip().title()
            les_choice = int(request.POST.getlist('les_choice')[0])
            zip_location = request.FILES['zip_location']
            if not project_name or not zip_location:
                raise KeyError
        except (ValueError, KeyError, IndexError):
            logging.info('ERROR - Please fill all the fields')
            messages.error(request, 'Please fill all the fields')
            return HttpResponseRedirect(reverse('pss:application'))
        app = Application(project_name=project_name,
                          les=les_choice,
                          zip_location=zip_location,
                          profile=Profile.objects.get(user=request.user))
        app.save()
        messages.success(request, 'Thanks for your submission!')
        app.send_email()
    return render(request, 'pss/application.html')
