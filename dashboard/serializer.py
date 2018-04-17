from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from dashboard.models import Challenge, Company, Project, ProjectContributor, EntityProxy, Bookmark
from .models import Tag
import json


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

    class Meta:
        model = Profile
        fields = ('id', 'user', 'picture', 'occupation', 'tags', 'city')


class CompanySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class ChallengeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    profile = ProfileSerializer(read_only=True)

    interested = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = '__all__'

    def get_interested(self,obj):
        return ProfileSerializer(obj.interested(), many=True).data


class ProjectContributorSerializer(serializers.ModelSerializer):
    contributor = ProfileSerializer(read_only=True)

    class Meta:
        model = ProjectContributor
        fields = ('contributor', 'status')


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    profile = ProfileSerializer(read_only=True)
    project_contributors = serializers.SerializerMethodField()
    tags_string = serializers.SerializerMethodField()

    interested = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_tags_string(self, obj):
        return obj.get_tags()

    def get_interested(self, obj):
        return ProfileSerializer(obj.interested(), many=True).data

    def get_project_contributors(self, obj):
        contrib_rel = ProjectContributor.objects.filter(project=obj)
        return ProjectContributorSerializer(contrib_rel, many=True).data


class EntityProxySerializer(serializers.ModelSerializer):
    interested = serializers.SerializerMethodField()

    class Meta:
        model = EntityProxy
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ('profile',)

    def to_representation(self, obj):
        """
        Because Bookmark is Polymorphic
        """
        print "TO REPDDSSSSS    "
        if isinstance(obj, EntityProxy):
            return EntityProxySerializer(obj).to_representation(obj)
        elif isinstance(obj, Project):
            return ProjectSerializer(obj).to_representation(obj)
        return super(BookmarkSerializer, self).to_representation(obj)