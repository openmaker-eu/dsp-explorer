from django.conf.urls import url

from . import views

app_name = 'oauth'

urlpatterns = [
    url(r'^twitter/', views.twitter_redirect, name='twitter_redirect'),
    url(r'^twitter_sign_in/', views.twitter_sign_in, name='twitter_sign_in'),
    url(r'^deactivate/(?P<social>[\w\-]+)$', views.deactivate_account, name='deactivate_account'),
]
