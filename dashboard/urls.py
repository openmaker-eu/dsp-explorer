from django.conf.urls import url

from . import views, authentication, api, static

app_name = 'dashboard'

urlpatterns = [
    # Auth
    url(r'^$', authentication.login_page, name='login'),
    url(r'^logout/$', authentication.logout_page, name='logout'),
    url(r'^reset_password/(?P<reset_token>[\w\-]+)$', authentication.reset_pwd, name='reset_pwd'),
    url(r'^recover/$', authentication.recover_pwd, name='recover_pwd'),

    # Explore
    url(r'^dashboard/theme/(?P<topic_id>[0-9]+)/$', views.theme, name='theme'),
    url(r'^dashboard/theme/$', views.theme, {'topic_id': None}, name='theme'),
    url(r'^dashboard', views.dashboard, name='dashboard'),

    # Profiles
    url(r'^profile/$', views.profile, {'action': None}, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, {'action': None}, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/(?P<action>[\w\-]+)/$', views.profile, name='profile'),

    # Search
    url(r'^search/members/$', views.search_members, name='search_members'),
    url(r'^search/members/(?P<search_string>[\w\-]+)/$', views.search_members, name='search_members'),

    # Invite
    url(r'^invite/$', views.invite, name='invite'),

    # Onboarding
    url(r'^onboarding/$', authentication.onboarding, name='onboarding'),
    url(r'^onboarding/confirmation/(?P<token>.+)/$', authentication.onboarding_confirmation, name='onboarding_confirmation'),
    url(r'^om_confirmation/(?P<sender_first_name>.+)/(?P<sender_last_name>.+)/(?P<sender_email>.+)/(?P<receiver_first_name>.+)/(?P<receiver_last_name>.+)/(?P<receiver_email>.+)/$', authentication.om_confirmation, name='om_confirmation'),

    # static
    url(r'^privacy/$', static.privacy, name='privacy'),
    url(r'^support/$', static.support, name='support'),
    url(r'terms/$', static.terms_conditions, name='terms_conditions'),

    # Feedback
    url(r'^feedback/$', views.feedback, name='feedback'),

    # API v1.2

        # NEWS (Ex Feeds)
        # url(r'^api/v1.2/news/(?P<topic_ids>.+)/$', api.get_news, {'date_name': 'yesterday', 'cursor': -1}, name='api_get_news'),
        # url(r'^api/v1.2/news/(?P<topic_ids>.+)/(?P<date_name>.+)/$', api.get_news, {'cursor': -1}, name='api_get_news'),
        url(r'^api/v1.2/news/(?P<topic_ids>.+)/(?P<date_name>.+)/(?P<cursor>.+)/$', api.get_news, name='api_get_news'),

        # TOPICS (Ex Themes)
        url(r'^api/v1.2/topics', api.get_topics, name='api_get_topics'),
        url(r'^api/v1.2/suggested_topic', api.get_suggested_topic, name='api_get_suggested_topic'),

        # AUDIENCES (EX Influencers)
        url(r'^api/v1.2/audiences/(?P<topic_id>.+)/', api.get_audiences, name='api_get_audiences'),


    # API v1.1
    url(r'^api/v1.1/search/members/(?P<search_string>.*)/$', api.search_members, name='api_search_member'),
    url(r'^api/v1.1/search/last_members/$', api.get_last_members, name='api_get_last_members'),
    url(r'^api/v1.1/get_feeds/(?P<theme_name>.+)/(?P<date>.+)/(?P<cursor>.+)/$', api.get_feeds, name='api_get_feeds'),
    url(r'^api/v1.1/get_themes', api.get_themes, name='api_get_themes'),
    url(r'^api/v1.1/get_influencers/(?P<theme_name>.+)/$', api.get_influencers, name='api_get_influencers'),
    url(r'^api/v1.1/om_invitation/$', api.post_om_invitation, name='post_om_invitation'),
    url(r'^api/v1.1/get_hot_tags/$', api.get_hot_tags, name='get_hot_tags'),
    url(r'^api/v1.1/get_hot_tags/(?P<tag_number>\d+)/$', api.get_hot_tags, name='get_hot_tags'),
    url(r'^api/v1.1/get_user_stats/$', api.get_user_stats, name='get_user_stats'),
    url(r'^api/v1.1/get_sectors/$', api.get_sector, name='get_sector'),
    url(r'^api/v1.1/get_places/$', api.get_places, name='get_places'),
    url(r'^api/v1.1/get_om_events/$', api.get_om_events, name='get_om_events'),
]
