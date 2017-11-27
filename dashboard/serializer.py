from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from .models import Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    # gender = serializers.CharField()
    # role = serializers.CharField()
    # birthdate = serializers.DateField()
    # city = serializers.CharField()
    #
    # occupation = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # statement = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # organization = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # sector = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # size = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # technical_expertise = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # place = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='[{"name":"twitter","link":""},{"name":"google-plus","link":""},{"name":"facebook","link":""}]')


    class Meta:
        model = Profile
        fields = ('id', 'user', 'picture', 'occupation', 'tags', 'city')
