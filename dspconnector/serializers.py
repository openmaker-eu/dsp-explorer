from django.db import models
from rest_framework import serializers

class TopicsSerializer(serializers.Serializer):
    topic_name = serializers.CharField(max_length=50),
    description = serializers.CharField()
    topic_id = serializers.IntegerField()

class AudiencesSerializer(serializers.Serializer):
    lang = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True)
    time_zone = serializers.CharField(allow_null=True, allow_blank=True)
    profile_image_url = serializers.CharField()
    screen_name = serializers.CharField()
    location = serializers.CharField(allow_null=True, allow_blank=True)
    name = serializers.CharField()

class NewsSerializer(serializers.Serializer):
    domain = serializers.CharField()
    description = serializers.CharField()
    title = serializers.CharField()
    url = serializers.CharField()
    popularity = serializers.CharField()
    link_id = serializers.IntegerField()
    source = serializers.CharField()
    published_at = serializers.CharField(allow_null=True, allow_blank=True)
    im = serializers.CharField()
    keywords = serializers.ListField()
