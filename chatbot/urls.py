from django.conf.urls import url

from . import views, api

app_name = 'chatbot'

urlpatterns = [
    url(r'^$', views.chatbot, name='chatbot'),
    url(r'^v1.1/message/$', api.message_to_rasa_nlu, name='message_to_rasa_nlu'),
]
