from django.conf.urls import url, include

from . import views, authentication, api, static, api14, questions

app_name = 'dashboard'

urlpatterns = [

    # Auth
    url(r'^test/$', views.test, name='test'),

    url(r'^$', authentication.login_page, name='homepage'),
    url(r'^logout/$', authentication.logout_page, name='logout'),
    url(r'^reset_password/(?P<reset_token>[\w\-]+)$', authentication.reset_pwd, name='reset_pwd'),
    url(r'^recover/$', authentication.recover_pwd, name='recover_pwd'),
    url(r'^manifesto/$', views.manifesto, name='manifesto'),

    ###################################### MDP ROUTES
    # Article list

    # url(r'^news_list/$', views.news_list, name='news_list'),
    # url(r'^news/(?P<entity_id>[0-9]+)/$', views.news_detail, name='news'),
    #
    # url(r'^articles_list/$', views.news_list, name='news_list'),
    # url(r'^article/(?P<entity_id>[0-9]+)/$', views.news_detail, name='news_detail'),
    #
    # url(r'^events_list/$', views.event_list, name='event_list'),
    # url(r'^events/(?P<entity_id>(\d+))/$', views.event_detail, name='event'),
    #
    # url(r'^projects_list/$', views.project_list, name='prj_list'),
    # url(r'^projects/(?P<entity_id>[0-9]+)$', views.project_detail, name='project_detail'),
    #
    # url(r'^challenges/(?P<entity_id>[0-9]+)$', views.challenge_detail, name='project'),
    #
    url(r'^profile/(?P<profile_id>[0-9]+)$', views.profile_detail, name='profile_detail'),
    url(r'^profile/$', views.profile_detail, name='profile_detail'),

    url(r'^entity/(?P<entity_name>\w+)/(?P<entity_id>[0-9]+)/(?P<entity_temp_id>[0-9]+)/$', views.entity_detail, name='entity_detail'),
    url(r'^entity/(?P<entity_name>\w+)/(?P<entity_id>[0-9]+)/$', views.entity_detail, name='entity_detail'),
    url(r'^entity/(?P<entity_name>\w+)/$', views.entity_list, name='entity_list'),


    ###################################### MDP ROUTES
    # Explore
    url(r'^dashboard/theme/(?P<topic_id>[0-9]+)/$', views.theme, name='theme'),
    url(r'^dashboard/theme/$', views.theme, {'topic_id': None}, name='theme'),
    url(r'^dashboard/events/(?P<topic_id>[0-9]+)/$', views.events, name='events'),
    url(r'^dashboard/events/$', views.events, {'topic_id': None}, name='events'),

    # Insight
    url(r'^insight/(?P<user_twitter_username>[0-9]+)/$', views.insight, name='insight'),
    url(r'^insight', views.insight, {'user_twitter_username': None}, name='insight'),

    # Dashboard
    url(r'^dashboard/(?P<topic_id>[0-9]+)/$', views.dashboard, name='dashboard'),
    url(r'^dashboard', views.dashboard, {'topic_id': None}, name='dashboard'),

    # Profiles
    url(r'^profile/project/$', views.project, name='project_create_update'),
    url(r'^profile/project/(?P<project_id>[0-9]+)/$', views.project, name='project'),
    url(r'^profile/project/(?P<project_id>[0-9]+)/(?P<action>[\w\-]+)/$', views.project, name='project'),

    # url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, {'action': None}, name='profile'),
    url(r'^profile/(?P<action>[\w\-]+)/$', views.profile, {'profile_id': None}, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/(?P<action>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/invitation/(?P<project_id>[0-9]+)/(?P<status>.+)/$', views.collaborator_invitation, name='profile'),

    url(r'^profile/$', views.profile, {'action': None}, name='profile'),

    # Search
    url(r'^search/members/$', views.community, name='community'),
    url(r'^search/members/(?P<search_string>[\w\- :]+)/$', views.community, name='community'),

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
    url(r'express_acceptance/$', static.express_acceptance, name='express_acceptance'),

    # Feedback
    url(r'^feedback/$', views.feedback, name='feedback'),

    url(r'^challenge/$', views.challenge, name='challenge'),
    url(r'^challenge/(?P<challenge_id>[0-9]+)/$', views.challenge, name='challenge'),


    # API v1.4
    ## MDP
    url(r'^api/v1.4/bookmark/(?P<entity>\w+)/(?P<entity_id>\w+)/$', api14.bookmark, name='bookmark'),
    url(r'^api/v1.4/bookmarks/(?P<entity>\w+)/$', api14.get_bookmark_by_entities, name='get_bookmark_by_entities'),
    url(r'^api/v1.4/bookmarks/$', api14.get_bookmarks, name='get_bookmark'),

    url(r'^api/v1.4/interest/chatbot/$', api14.chatbot_interests, name='chatbot_interests'),
    url(r'^api/v1.4/interest/(?P<entity>\w+)/(?P<user_id>\w+)/$', api14.interest, name='all_interest_of_user_in_entitiy'),
    url(r'^api/v1.4/interest/(?P<entity>\w+)/$', api14.interest, {'user_id': None}, name='all_interest_of_loggeduser_in_entitiy'),
    url(r'^api/v1.4/interest/$', api14.interest, {'entity': None, 'user_id': None}, name='all_interest_of_user'),

    url(r'^api/v1.4/user/interest/(?P<entity>\w+)/(?P<entity_id>\w+)/$', api14.my_interest, name='get_interested'),
    url(r'^api/v1.4/interested/(?P<entity>\w+)/(?P<entity_id>\w+)/$', api14.interested, name='get_interested'),
    url(r'^api/v1.4/interested/(?P<entity>\w+)/$', api14.interested, name='get_interested'),
    url(r'^api/v1.4/interests/$', api14.get_interests, name='get_bookmark'),

    # Auht
    url(r'^api/v1.4/login/$', api14.apilogin, name='user_login'),
    url(r'^api/v1.4/logout/$', api14.apilogout, name='user_logout'),
    url(r'^api/v1.4/signup/$', api14.signup, name='user_signup'),
    url(r'^api/v1.4/authorization/$', api14.authorization, name='get_user_authorization'),

    # Questions (Bot and wizard)
    url(r'^api/v1.4/questions/(?P<action>\w+)/$', questions.questions.as_view(), name='questions'),
    url(r'^api/v1.4/questions/$', questions.questions.as_view(), name='questions'),

    # Projects
    url(r'^api/v1.4/user/(?P<profile_id>\w+)/project/$', api14.user_projects, name='user_projects'),
    url(r'^api/v1.4/user/project/$', api14.user_projects, {'profile_id': None}, name='logged_user_projects'),

    # Entity - with user id (Tailored)
    url(r'^api/v1.4/user/(?P<user_id>\w+)/(?P<entity>\w+)/$', api14.entity.as_view(), name='user_entity'),

    # Entity
    url(r'^api/v1.4/(?P<entity>\w+)/(?P<entity_id>\w+)/$', api14.entity_details.as_view(), name='api_14_entity_detail'),
    url(r'^api/v1.4/(?P<entity>\w+)/$', api14.entity.as_view(), name='api_14_entity'),


    # API v1.3
    ## AUDIENCES
    url(r'^api/v1.3/audiences/(?P<topic_id>.+)/(?P<location>.+)/$', api.v13.get_audiences, name='api_13_get_audiences'),
    url(r'^api/v1.3/audiences/(?P<topic_id>.+)/$', api.v13.get_audiences, {'location': None}, name='api_13_get_audiences'),

    url(r'^api/v1.3/influencers/(?P<topic_id>.+)/(?P<location>.+)/$', api.v13.get_influencers, name='api_13_get_influencers'),
    url(r'^api/v1.3/influencers/(?P<topic_id>.+)/$', api.v13.get_influencers, {'location': None}, name='api_13_get_influencers'),

    url(r'^api/v1.3/events/(?P<topic_id>.+)/(?P<location>.+)/(?P<cursor>.+)/$', api.v13.get_events, name='api_13_get_events'),
    url(r'^api/v1.3/events/(?P<topic_id>.+)/(?P<cursor>.+)/$', api.v13.get_events, name='api_13_get_events'),

    url(r'^api/v1.3/hashtags/(?P<topic_id>.+)/(?P<date_string>.+)', api.v13.get_hashtags, name='api_13_hashtags'),

    url(r'^api/v1.3/news/(?P<topic_id>.+)/(?P<date_string>.+)/(?P<cursor>.+)/$', api.v13.get_news, name='api_13_news'),

    url(r'^api/v1.3/project/invitation/(?P<status>.+)/$', api.v13.project_invitation, name='api_13_project_invitation'),
    url(r'^api/v1.3/project/invitation/$', api.v13.project_invitation, name='api_13_project_invitation'),
    url(r'^api/v1.3/project/(?P<project_id>.+)/$', api.v13.project, name='api_13_project'),
    url(r'^api/v1.3/project/$', api.v13.project, {'project_id': None}, name='api_13_project'),
    url(r'^api/v1.3/profile/(?P<profile_id>[0-9]+)/projects/$', api.get_profile_projects, name='get_profile_projects'),

    url(r'^api/v1.3/challenge/$', api.get_challenge, {'challenge_id': None},  name='get_challenge'),
    url(r'^api/v1.3/challenge/(?P<challenge_id>[0-9]+)/$', api.get_challenge, name='get_challenge'),
    url(r'^api/v1.3/interest_ids/', api.get_interest_ids, name='get_interest_ids'),

    url(r'^api/v1.3/interest/ids/(?P<model_object>.*)/$', api.get_interest_object_ids, name='get_interest_object_ids'),
    url(r'^api/v1.3/interest/challenge/(?P<challenge_id>[0-9]+)/$', api.interest_challenge, name='interest_challenge'),
    url(r'^api/v1.3/interest/project/(?P<project_id>[0-9]+)/$', api.interest_project, name='interest_project'),
    url(r'^api/v1.3/profile/(?P<profile_id>[0-9]+)/challenge/$', api.get_profile_challenge, name='get_profile_challenge'),

    # API v1.2
    # NEWS (Ex Feeds)
    url(r'^api/v1.2/news/(?P<topic_ids>.+)/(?P<date_name>.+)/(?P<cursor>.+)/$', api.get_news, name='api_get_news'),
    # EVENTS
    url(r'^api/v1.2/events/(?P<topic_ids>.+)/(?P<cursor>.+)/$', api.get_events, name='api_get_events'),

    # TOPICS (Ex Themes)
    url(r'^api/v1.2/topics', api.get_topics, name='api_get_topics'),
    url(r'^api/v1.2/suggested_topic', api.get_suggested_topic, name='api_get_suggested_topic'),

    # AUDIENCES (EX Influencers)
    url(r'^api/v1.2/audiences/(?P<topic_id>.+)/', api.get_audiences, name='api_get_audiences'),

    # UPDATE CRM API
    url(r'^api/v1.2/update_field/(?P<to_be_updated>.+)/(?P<update_token>.+)/', api.update_field, name='api_update_field'),
    url(r'^api/v1.2/check_canvas/(?P<twitter_username>.+)/', api.check_canvas, name='api_check_canvas'),

    # API v1.1
    url(r'^api/v1.1/search/members/(?P<search_string>.*)/$', api.search_members, name='api_search_member'),
    url(r'^api/v1.1/search/members/', api.search_members, {'search_string': None},  name='api_search_member'),

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
    url(r'^api/v1.1/invitation/csv$', api.get_invitation_csv, name='get_invitation_csv'),

]

