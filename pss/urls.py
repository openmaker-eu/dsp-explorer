from django.conf.urls import url

from . import views

app_name = 'pss'

urlpatterns = [
    url(r'^$', views.application, name='application'),
    url(r'^result/$', views.application_result, name='application_result'),

    url(r'^application_pdf/$', views.application_pdf, {'application_id': None}, name='application_pdf'),
    url(r'^application_pdf/(?P<application_id>[0-9]+)/$', views.application_pdf, name='application_pdf')
]
