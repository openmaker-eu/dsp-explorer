from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from dashboard.models import Challenge, Company, Project, ProjectContributor, EntityProxy, Bookmark, Interest, Tag
import json


class UserSerializer(serializers.ModelSerializer):

    profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    twitter_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'profile', 'twitter_name', 'location')

    def get_twitter_name(self, obj):
        return obj.profile.twitterauth.screen_name if hasattr(obj.profile, 'twitterauth') else None

    def get_location(self, obj):
        return obj.profile.place if hasattr(obj.profile, 'place') else None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


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
        return [x.get('name', '') for x in TagSerializer(obj.get_tags(), many=True).data]

    def get_interested(self, obj):
        return ProfileSerializer(obj.interested(), many=True).data

    def get_project_contributors(self, obj):
        contrib_rel = ProjectContributor.objects.filter(project=obj)
        return ProjectContributorSerializer(contrib_rel, many=True).data


class EntityProxySerializer(serializers.ModelSerializer):
    #interested = serializers.SerializerMethodField()

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
        if isinstance(obj, EntityProxy):
            return obj.get_real_object()[0]
        elif isinstance(obj, Project):
            return ProjectSerializer(obj).to_representation(obj)
        return super(BookmarkSerializer, self).to_representation(obj)


class InterestSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Interest
        fields = ('profile',)

    def to_representation(self, obj):
        """
        Because Interest is Polymorphic
        """
        if isinstance(obj, EntityProxy):
            return obj.get_real_object()[0]
            # return EntityProxySerializer(obj).to_representation(obj)
        elif isinstance(obj, Project):
            return ProjectSerializer(obj).to_representation(obj)
        return super(InterestSerializer, self).to_representation(obj)


class ExtChallengeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)
    tags = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    les = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)

    interested = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        # fields = '__all__'
        exclude = ("notify_admin", "notify_user")

    def get_tags(self, obj):
        return [x.name for x in obj.tags.all()]

    def get_company(self, obj):
        return obj.company.name

    def get_interested(self, obj):
        return [x.crm_id for x in obj.interested()]

    def get_les(self, obj):
        return obj.les_choices[obj.les][1]

    # def get_interested(self, obj):
    #     return ProfileSerializer(obj.interested(), many=True).data


class ExtProjectSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()

    interested = serializers.SerializerMethodField()

    class Meta:
        model = Project
        # fields = '__all__'
        exclude = ('project_contributors',)

    def get_tags(self, obj):
        return [x.name for x in obj.tags.all()]

    def get_profile(self, obj):
        return obj.profile.crm_id

    def get_interested(self, obj):
        return [x.crm_id for x in obj.interested()]

    def get_contributors(self, obj):
        contrib_rel = ProjectContributor.objects.filter(project=obj)
        return [x.crm_id for x in contrib_rel]
