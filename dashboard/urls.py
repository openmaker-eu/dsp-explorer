from django.conf.urls import url

from . import views, authentication, api

app_name = 'dashboard'

urlpatterns = [
    # Auth
    url(r'^$', authentication.login_page, name='login'),
    url(r'^logout/$', authentication.logout_page, name='logout'),
    url(r'^reset_password/(?P<reset_token>[\w\-]+)$', authentication.reset_pwd, name='reset_pwd'),
    url(r'^recover/$', authentication.recover_pwd, name='recover_pwd'),
    
    # Explore
    url(r'^dashboard/theme/(?P<theme_name>[\w\-]+)$', views.theme, name='theme'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    
    # Profiles
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, name='user_detail'),
    
    # Search
    url(r'^search/members/$', views.search_members, name='search_members'),

    # Invite
    url(r'^invite/$', views.invite, name='invite'),

    # Privacy
    url(r'^privacy/$', views.privacy, name='privacy'),

    # FAQ page
    url(r'^support/$', views.support, name='support'),

    # Terms and Conditions
    url(r'terms/$', views.terms_conditions, name='terms_conditions'),

    # API v1.0
    url(r'^api/v1.0/request_membership/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        api.request_membership, name='api_request_membership'),
    url(r'^api/v1.0/search/members/(?P<search_string>.*)/$', api.search_members, name='api_search_member'),
    url(r'^api/v1.0/search/last_members/$', api.get_last_members, name='api_get_last_members'),

    # API v1.1
    url(r'^api/v1.1/get_feeds/(?P<theme_name>.+)/(?P<date>.+)/(?P<cursor>.+)/$', api.get_feeds, name='api_get_feeds'),
    url(r'^api/v1.1/get_themes', api.get_themes, name='api_get_themes')
]

