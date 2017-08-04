from django.conf.urls import url

from . import views

app_name = 'pss'

urlpatterns = [
    url(r'^$', views.application, name='application'),
    url(r'^result/$', views.application_result, name='application_result')
]
