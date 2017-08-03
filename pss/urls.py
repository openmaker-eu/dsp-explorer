from django.conf.urls import url

from . import views

app_name = 'pss'

urlpatterns = [
    url(r'^$', views.application, name='application')
]
