from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', views.login_page, name='login'),
    url(r'^logout', views.logout_page, name='logout'),
    url(r'^dashboard/theme/(?P<theme_name>[\w\-]+)$', views.theme, name='theme'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^profile', views.profile, name='profile'),
]
