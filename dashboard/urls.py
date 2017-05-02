from django.conf.urls import url

from . import views, authentication

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', authentication.login_page, name='login'),
    url(r'^logout', authentication.logout_page, name='logout'),
    url(r'^dashboard/theme/(?P<theme_name>[\w\-]+)$', views.theme, name='theme'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^request_membership/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        authentication.request_membership, name='request_membership'),
    url(r'^reset_password/(?P<reset_token>[\w\-]+)$', authentication.reset_pwd, name='reset_pwd'),
    url(r'^recover', authentication.recover_pwd, name='recover_pwd'),
]
