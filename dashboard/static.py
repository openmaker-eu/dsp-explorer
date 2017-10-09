from django.shortcuts import render


def privacy(request):
    return render(request, 'dashboard/privacy.html', {})


def support(request):
    return render(request, 'dashboard/support.html', {})


def terms_conditions(request):
    return render(request, 'dashboard/terms_conditions.html', {})


def express_acceptance(request):
    return render(request, 'dashboard/express_acceptance.html', {})
