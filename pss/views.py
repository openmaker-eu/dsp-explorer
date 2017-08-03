from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def application(request):
    if request.method == 'POST':
        pass
    return render(request, 'pss/application.html')
