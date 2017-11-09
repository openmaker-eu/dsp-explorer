from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
@staff_member_required(login_url='dashboard:login')
def chatbot(request):
    return render(request, 'chatbot/chatbot.html')
