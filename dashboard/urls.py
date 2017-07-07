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
    url(r'^dashboard/theme/(?P<theme_name>.*)$', views.theme, name='theme'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    
    # Profiles
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, name='user_detail'),
    
    # Search
    url(r'^search/members/$', views.search_members, name='search_members'),

    # Invite
    url(r'^invite/$', views.invite, name='invite'),

    # Onboarding
    url(r'^onboarding/$', views.onboarding, name='onboarding'),

    # Privacy
    url(r'^privacy/$', views.privacy, name='privacy'),

    # Feedback
    url(r'^feedback/$', views.feedback, name='feedback'),

    # FAQ page
    url(r'^support/$', views.support, name='support'),

    # Terms and Conditions
    url(r'terms/$', views.terms_conditions, name='terms_conditions'),

    # Confirmation
    url(r'^om_confirmation/(?P<sender_first_name>.+)/(?P<sender_last_name>.+)/(?P<sender_email>.+)/(?P<receiver_first_name>.+)/(?P<receiver_last_name>.+)/(?P<receiver_email>.+)/$', views.om_confirmation, name='om_confirmation'),

    # API v1.0
    # url(r'^api/v1.0/request_membership/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',api.request_membership, name='api_request_membership'),
    url(r'^api/v1.0/search/members/(?P<search_string>.*)/$', api.search_members, name='api_search_member'),
    url(r'^api/v1.0/search/last_members/$', api.get_last_members, name='api_get_last_members'),

    # API v1.1
    url(r'^api/v1.1/get_feeds/(?P<theme_name>.+)/(?P<date>.+)/(?P<cursor>.+)/$', api.get_feeds, name='api_get_feeds'),
    url(r'^api/v1.1/get_themes', api.get_themes, name='api_get_themes'),
    url(r'^api/v1.1/get_influencers/(?P<theme_name>.+)/$', api.get_influencers, name='api_get_influencers'),

    url(r'^api/v1.1/om_invitation/$', api.post_om_invitation, name='post_om_invitation'),
]

