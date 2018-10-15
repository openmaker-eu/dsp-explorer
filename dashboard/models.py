# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django_mysql.models import JSONField
from django.utils import timezone
from datetime import datetime as dt, datetime
from utils.hasher import HashHelper
import uuid
from .exceptions import EmailAlreadyUsed, UserAlreadyInvited, SelfInvitation, InvitationAlreadyExist, InvitationDoesNotExist
from opendataconnector.odconnector import OpenDataConnector
from restcountriesconnector.rcconnector import RestCountriesConnector
import json, re
from utils.GoogleHelper import GoogleHelper
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
from utils.mailer import EmailHelper
from dspconnector.connector import DSPConnectorV13
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
import os
from collections import Counter
from connectors.insight.connector import InsightConnectorV10 as Insight

class ModelHelper:

    @staticmethod
    def get_by_name(model_name):
        try:
            ct_model = ContentType.objects.get(model=model_name)
            return ct_model.model_class()
        except Exception as e:
            print(model_name)
            print('error findig class')
            print(e)


    @staticmethod
    def get_serializer(model):
        ct_model = None
        model_name = None

        try:
            # GET ContentType instance
            if isinstance(model, str):
                ct_model = ContentType.objects.get(model=model)
                model_name = model
            elif issubclass(model, models.Model):
                ct_model = ContentType.objects.get_for_model(model)
                model_name = model._meta.object_name

            # GET Application
            app_label = ct_model.app_label
            app = __import__(app_label)

            # Try to get serializer class
            return getattr(app.serializer, model_name+'Serializer')
        except Exception as e:
            print('try get serializer error')
            print(e)
            return False

    @classmethod
    def filter_instance_list_by_class(cls, list_to_filter, filter_class=None, filter_type=None):
        if filter_type:
            return [x for x in list_to_filter if isinstance(x, filter_class) if x.type == filter_type if hasattr(x, 'type')]
        if filter_class is not None:
            return [x for x in list_to_filter if isinstance(x, filter_class)]
        return list_to_filter

    @staticmethod
    def find_this_entity(entity, entity_id):
        local_entity = None
        if entity == 'news' or entity == 'events':
            with transaction.atomic():
                try:
                    local_entity = EntityProxy.objects.select_for_update().get(type=entity, externalId=entity_id)
                except EntityProxy.DoesNotExist:
                    print("CREATE THE ENTITY [TYPE]:{} --- [ID]:{}".format(entity, entity_id))
                    local_entity = EntityProxy()
                    local_entity.externalId = entity_id
                    local_entity.type = entity
                    local_entity.save()

        elif entity == 'projects':
            local_entity = Project.objects.get(pk=entity_id)
        elif entity == 'profile':
            local_entity = Profile.objects.get(pk=entity_id)
        else:
            try:
                local_entity = Challenge.objects.get(pk=entity_id)
            except Challenge.DoesNotExist as e:
                raise ObjectDoesNotExist
            except Exception as e:
                raise ObjectDoesNotExist
        return local_entity


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False)
    type = models.CharField(max_length=50, null=True, default=None)

    @classmethod
    def create(cls, name, type=None):
        tag = Tag(name=name, type=type)
        tag.save()
        return tag

    @classmethod
    def create_or_update(cls, tag, tag_type=None):
        return Tag.objects.filter(name=tag, type=tag_type).first() or Tag.create(name=tag, type=tag_type) if isinstance(tag, str) else None

    def __str__(self):
        return self.name


class Country(models.Model):
    code = models.CharField(max_length=20, null=True, blank=True, default=None)
    alias = models.TextField(null=True, blank=True, default=None)

    @classmethod
    def create(cls, code, alias):
        existing = Country.objects.filter(code=code)

        if len(existing):
            return existing

        new_country = cls(code=code, alias=alias)
        new_country.save()
        return new_country

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return self.code

class Location(models.Model):

    lat = models.CharField(null=True, blank=True, max_length=20)
    lng = models.CharField(null=True, blank=True, max_length=20)

    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    country_short = models.CharField(max_length=200, null=True, blank=True)
    post_code = models.CharField(max_length=200, null=True, blank=True)
    city_alias = models.TextField(null=True, blank=True, default=None)
    country_alias = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, default=None)

    @classmethod
    def create(cls, lat, lng, city, state=None, country=None, country_short=None, post_code=None, city_alias=None):
        existing_location = Location.objects.filter(lat=lat, lng=lng)
        new_location = None

        # Model does not esxist
        if not len(existing_location):
            new_location = cls(
                lat=lat,
                lng=lng,
                city=city,
                state=state,
                country=country,
                country_short=country_short,
                post_code=post_code,
                city_alias=city+','
            )
            latlng = cls.get_latlng(lat, lng)
            aliases = OpenDataConnector.get_city_alternate_name_by_latlng(latlng)

            if aliases:
                new_location.city_alias = aliases+','
            new_location.save()

        else:
            existing_location = existing_location[0]
            # Model Exist, update
            if existing_location and not city+',' in existing_location.city_alias:
                existing_location.city_alias += city+','
                existing_location.save()

        results = new_location or existing_location
        cls.add_country_alias(results)

        return results

    @classmethod
    def add_country_alias(cls, location):
        if not location.country_alias:
            existing_country = Country.objects.filter(code=location.country_short)
            if len(existing_country):
                location.country_alias = existing_country[0]
                location.save()
                return location

            country_aliases = RestCountriesConnector.get_city_alias(location.country)
            if country_aliases:
                country_alias = Country.create(location.country_short, country_aliases)
                location.country_alias = country_alias
                location.save()

    @classmethod
    def get_latlng(cls, lat=None, lng=None):
        lat = lat or cls.lat
        lng = lng or cls.lng
        return lat+','+lng

    class Meta:
        ordering = ('lat', 'lng', 'city')

    def __str__(self):
        return self.city+', '+self.state+' '+self.country+' '+self.country_short


class SourceOfInspiration(models.Model):
    name = models.TextField(_('Name'), max_length=200, null=False, blank=False)

    @classmethod
    def create(cls, name):
        source = SourceOfInspiration(name=name)
        source.save()
        return source

    def __str__(self):
        return self.name


class User(User):

    class Meta:
        proxy = True

    @classmethod
    def create(cls, *args, **kwargs):

        print(kwargs)
        if User.objects.filter(email=kwargs.get('email', False)).first():
            return False
        try:
            print('1')
            user = User.objects.create_user(
                username=kwargs.get('email', False),
                email=kwargs.get('email', False),
                password=kwargs.get('password', False),
                first_name=kwargs.get('first_name', False),
                last_name=kwargs.get('last_name', False)
            )
            user.is_active = False
            user.save()
            return user

        except Exception as e:
            print('User creation Error')
            print(e)
            return False


# class interest_mixin(models.Model):
#     '''
#     addnin
#     '''
#     class Meta:
#         abstract = True
#
#     interest = GenericRelation('Interest')
#
#     def interested(self, filter_class=None):
#         interests = self.interest.all().order_by('-created_at')
#         interested = map(lambda x: x.profile, interests) if len(interests) > 0 else []
#         return ModelHelper.filter_instance_list_by_class(interested, filter_class)


def default_place():
    return {}

class Profile(models.Model):
    crm_id = models.PositiveIntegerField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(_('Picture'), upload_to='images/profile', null=True, blank=True)
    gender = models.TextField(_('Gender'), max_length=500, null=True, blank=True)
    city = models.TextField(_('City'), max_length=500, null=True, blank=True)
    occupation = models.TextField(_('Occupation'), max_length=500, null=True, blank=True)
    birthdate = models.DateTimeField(_('Birth Date'), blank=True, null=True)

    twitter_username = models.TextField(_('Twitter Username'), max_length=100, blank=True, null=True)
    twitter = models.BooleanField(default=False)

    place = models.TextField(default=None, null=True)

    statement = models.TextField(_('Statement'), blank=True, null=True)
    role = models.TextField(_('Role'), max_length=200, null=True, blank=True, default='')
    organization = models.TextField(_('Organization'), max_length=200, null=True, blank=True, default='')
    sector = models.TextField(_('Sector'), max_length=200, null=True, blank=True, default='')
    types_of_innovation = models.TextField(_('Types of Innovation'), max_length=200, null=True, blank=True, default='')
    size = models.TextField(_('Size'), max_length=200, null=True, blank=True, default='')

    technical_expertise = models.TextField(_('Technical Expertise'), max_length=200, null=True, blank=True, default='')

    technical_expertise_other = models.TextField(_('Technical Expertise other'), max_length=200, null=True, blank=True, default='')
    role_other = models.TextField(_('Role other'), max_length=200, null=True, blank=True, default='')
    sector_other = models.TextField(_('Sector other'), max_length=200, null=True, blank=True, default='')

    tags = models.ManyToManyField(Tag, related_name='profile_tags')
    source_of_inspiration = models.ManyToManyField(SourceOfInspiration, related_name='profile_sourceofinspiration')

    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, default=None)
    interest = GenericRelation('Interest')

    # domain = models.TextField(blank=True)
    # area = models.TextField(blank=True)
    # technology = models.TextField(blank=True)
    # skills = models.TextField(blank=True)

    def activity(self, tag_type, tags=None):
        '''

        :param tag_type:
        :param tags:
        :return:
            if tags are not provided return the tags
            if tags are provided create/update the relation
        '''

        # Get tags
        if tags is None:
            relat = Tag.objects.filter(profile_tags=self.pk, type=tag_type).values()
            return relat
        # Create if not exist and then relate/unrelate to this profile
        else:
            return self.tags_create_or_update(tags=tags, clear=True, tag_type=tag_type)


    socialLinks = models.TextField(
        _('Social Links'),
        max_length=200,
        null=True,
        blank=True,
        default='[{"name":"twitter","link":""},{"name":"google-plus","link":""},{"name":"facebook","link":""}]'
    )

    def reccomended(self):
        try:
            res = Insight.reccomended_user(self.crm_id)
            users_ids = res.json()['users'][0]['recommended_users']
            profiles = Profile.objects.filter(crm_id__in=users_ids)
            return profiles
        except:
            pass

    def best_matches(self):
        all_matches = [y.pk for x in self.tags.all() for y in x.profile_tags.all() if y.pk!=self.pk]
        best_matches = [x[0] for x in Counter(all_matches).most_common(5)]
        return Profile.objects.filter(pk__in=best_matches)


    def interested(self, filter_class=None):
        interests = self.interest.all().order_by('-created_at')
        interested = [x.profile for x in interests] if len(interests) > 0 else []
        return ModelHelper.filter_instance_list_by_class(interested, filter_class)

    def interests(self, filter_class=object):
        return [x.get() for x in self.profile_interest.all() if isinstance(x.get(), filter_class)]

    @classmethod
    def create(cls, **kwargs):
        user = kwargs.get('user', None)
        tags = kwargs.get('tags', None)

        profile = cls(user=user)

        profile.picture = kwargs.get('picture', None)
        profile.gender = kwargs.get('gender', None)
        profile.birthdate = kwargs.get('birthdate', None)
        profile.city = kwargs.get('city', None)
        profile.occupation = kwargs.get('occupation', None)
        profile.place = kwargs.get('place', None)

        profile.reset_token = Profile.get_new_reset_token()
        profile.save()

        tags and profile.tags_create_or_update(tags)

        # Set activities as tags
        profile.activity('area', kwargs.get('area', None))
        profile.activity('technology', kwargs.get('technology', None))
        profile.activity('skills', kwargs.get('skills', None))
        profile.activity('domain', kwargs.get('domain', None))
        profile.save()

        try:
            # Create user on CRM
            party = cls.create_or_update_to_crm(profile.user)
            # Try to set crm_id to profile model
            profile.crm_id = party.get_crm_id() if party else None
            profile.save()
            # Notify insight about the new user
            profile.crm_id is not None and Insight.notify_user_creation(profile.crm_id)
        except Exception as e:
            print('[ERROR : dashboard.models.profile.create]')
            print(e)
        return profile

    @classmethod
    def create_or_update_to_crm(cls, user):
        from crmconnector.models import Party
        user = user or cls
        try:
            party = Party(user)
            party.create_or_update()
            return party
        except Exception as e:
            print('#####################################')
            print('Error creating/updating user to CRM')
            print(e)
            print('#####################################')
            return False

    def tags_create_or_update(self, tags, clear=False, tag_type=None):
        if not tags:
            return False
        #tags = [x.lower().capitalize() for x in tags.split(",")] if isinstance(tags, str) else tags
        tags = [x for x in tags.split(",")] if isinstance(tags, str) else tags
        print([x for x in Tag.objects.filter(profile_tags=self.pk, type=tag_type)])

        clear and [self.tags.remove(x) for x in Tag.objects.filter(profile_tags=self.pk, type=tag_type)]

        for tag in tags:
            tagInstance = Tag.create_or_update(tag, tag_type)
            tagInstance and self.tags.add(tagInstance)
        tags and self.save()

    def picture_set_or_update(self, picture):
        if picture:
            filename, file_extension = os.path.splitext(picture.name)
            if not file_extension in ['.jpg', '.jpeg', '.png']:
                raise ValueError('nonvalid')
            if picture.size > 1048576: ## 1MB limit
                raise ValueError('sizelimit')
            picture.name = 'p_' + str(self.pk) + file_extension  ## str(datetime.now().microsecond)
            self.picture = picture

        return picture

    def set_location(self):
        return None

    # Reset Password
    reset_token = models.TextField(max_length=200, null=True, blank=True)
    update_token_at = models.DateTimeField(default=None, null=True, blank=True)
    ask_reset_at = models.DateTimeField(default=dt.now, null=True, blank=True)

    # def __str__(self):
    #     return "%s %s" % (self.get_name(), self.get_last_name())

    def __str__(self):
        try:
            return self.user.email
        except:
            return 'Error'

    # def __repr__(self):
    #     return self.__str__()

    class Meta:
        ordering = ('user',)



    @classmethod
    def createold(cls, email, first_name, last_name, picture, password=None, gender=None,
               birthdate=None, city=None, occupation=None, twitter_username=None, place=None, tags=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = False
            user.save()

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = cls(user=user)
            profile.picture = picture
            profile.gender = gender
            profile.birthdate = birthdate
            profile.city = city
            profile.occupation = occupation
            profile.twitter_username = twitter_username
            profile.place = place
            profile.save()

        if not user.is_active:
            profile.reset_token = Profile.get_new_reset_token()
            profile.save()
            return profile
        raise EmailAlreadyUsed

    @classmethod
    def delete_account(cls, user_id):
        from crmconnector.models import Party
        user = User.objects.get(pk=user_id)
        profile = user.profile
        try:
            # Crm
            party = Party(user)
            party.find_and_delete()
            # Tags
            profile.delete()
            user.delete()
        except:
            raise

    def send_email(self, subject, message):
        """
        Send Async Email to the user
        :param subject: Subject of the email
        :param message: Email Content
        :return: Nothing
        """
        import threading
        thr = threading.Thread(
            target=Profile._send_email,
             kwargs=dict(
                 message=message,
                 subject=subject,
                 receiver_name=self.user.get_full_name(),
                 receiver_email=self.user.email
             )
        )
        thr.start()

    def get_name(self):
        import unicodedata
        return unicodedata.normalize('NFKD', self.user.first_name).encode('ascii', 'ignore')

    def get_last_name(self):
        import unicodedata
        return unicodedata.normalize('NFKD', self.user.last_name).encode('ascii', 'ignore')

    def get_location(self):
        return {k: v for x in [self.place] if x for k, v in json.loads(x).items()}

    @staticmethod
    def _send_email(subject, message, receiver_name, receiver_email):
        """
        Send Email method
        :param subject: Subject of the email
        :param message: Email Content
        :param receiver_name: Name of the receiver
        :param receiver_email: Email of the receiver
        :return: Nothing
        """
        from utils.mailer import EmailHelper
        EmailHelper.send_email(message=message,
                               subject=subject,
                               receiver_name=receiver_name,
                               receiver_email=receiver_email)

    @staticmethod
    def get_new_reset_token():
        """
        Generate a new reset Token
        :return: String
        """
        return str(uuid.uuid4())

    def update_reset_token(self):
        """
        Generate a new reset Token
        :return: String
        """
        import pytz
        self.reset_token = (uuid.uuid4())
        self.update_token_at = pytz.utc.localize(dt.now())
        self.save()

    @classmethod
    def search_members(cls, search_string=None, restrict_to=None):
        profiles = Profile.objects.all().select_related('user')

        if restrict_to == 'tags':
            filter = (Q(tags__name=search_string))
        elif restrict_to == 'sectors':
            filter = (Q(sector=search_string))
        elif restrict_to == 'basic':
            filter = (
                Q(user__email__icontains=search_string) |
                Q(user__first_name__icontains=search_string) |
                Q(user__last_name__icontains=search_string)
            )
        else:
            filter = (
                Q(user__email__icontains=search_string) |
                Q(user__first_name__icontains=search_string) |
                Q(user__last_name__icontains=search_string) |
                Q(tags__name__icontains=search_string) |
                Q(twitter_username__icontains=search_string) |
                Q(occupation__icontains=search_string) |
                Q(sector__icontains=search_string) |
                Q(city__icontains=search_string) |
                Q(location__city_alias__icontains=search_string) |
                Q(location__country_alias__alias__icontains=search_string)
            )

        return profiles.filter(filter & Q(user__isnull=False)).distinct().order_by('-pk') \
            if search_string is not None \
            else profiles.filter().distinct().order_by('-pk')

    @classmethod
    def get_last_n_members(cls, n):
        return cls.objects.order_by('-user__date_joined')[:n]

    @classmethod
    def get_by_email(cls, email):
        return cls.objects.get(user__email=email)

    @classmethod
    def get_by_id(cls, profile_id):
        return cls.objects.get(id=profile_id)

    @classmethod
    def get_hot_tags(cls, tag_number=4):
        tags = [t["name"] for p in Profile.objects.all() for t in p.tags.values()]
        hot = Counter(tags).most_common(int(tag_number))
        return hot

    @classmethod
    def get_sectors(cls):
        from collections import Counter

        print('sectors')
        print(Profile.objects.values_list('sector', flat=True))
        print('endsectors')

        #flat_sectors = filter(lambda x: x is not None and x.strip() != '', Profile.objects.values_list('sector', flat=True))
        flat_sectors = filter(lambda x: x is not None and x.strip() != '', Profile.objects.values_list('sector', flat=True))
        sectors = Counter(flat_sectors).most_common(1000)
        return sectors

    @classmethod
    def get_places(cls):
        # places = filter(lambda x: x is not None, Profile.objects.values_list('place', flat=True))
        print(Profile.objects.values_list('place', flat=True))
        places = [x for x in Profile.objects.values_list('place', flat=True) if x is not None]
        return places

    def sanitize_place(self, force=False):
        try:
            if not self.place or 'city' not in self.place or force is not False:
                city = self.city
                place = GoogleHelper.get_city(city)
                if place:
                    self.place = json.dumps(place)
                    self.save()
        except Exception as e:
            print('error')
            print('e')

    def set_place(self, place):
        self.place = place
        try:
            if not self.place or 'city' not in self.place:
                new_place = GoogleHelper.get_city(self.city)
                if new_place:
                    self.place = json.dumps(new_place)
                    self.save()
            if self.place or 'city' in self.place:
                place = json.loads(self.place)
                location = Location.create(
                    lat=repr(place['lat']),
                    lng=repr(place['long']),
                    city=place['city'],
                    state=place['state'],
                    country=place['country'],
                    country_short=place['country_short'],
                    post_code=place['post_code'] if 'post_code' in place else '',
                    city_alias=place['city']+','
                )
                self.location = location
                self.save()
        except Exception as e:
            print(e)

    def add_interest(self, interest_obj):
        from utils.mailer import EmailHelper

        # Check existing realation between same interest related model and same profile
        ct_id = ContentType.objects.get_for_model(interest_obj).pk
        existing_interest = Interest.objects.filter(content_type_id=ct_id, profile_id=self.pk, object_id=interest_obj.pk)
        # If doesnt exist create interest and relations
        if len(existing_interest) == 0:
            interest = Interest(content_object=interest_obj)
            interest.profile = self
            interest.save()

    def get_interests(self, filter_class=None):
        interests = [x.get() for x in self.profile_interest.all()]
        if filter_class == 'events' or filter_class == 'news':
            res = ModelHelper.filter_instance_list_by_class(interests, EntityProxy, filter_class)
            return res
        else:
            filter_class = ModelHelper.get_by_name(EntityProxy.singular_name(filter_class))
            return ModelHelper.filter_instance_list_by_class(interests, filter_class)

    def delete_interest(self, interest_obj, interest_id):
        # Get interest-related-model class type id
        # Get content type from model instance
        ct_id = ContentType.objects.get_for_model(interest_obj).pk
        # Get Interest record
        interest = Interest.objects.filter(content_type_id=ct_id, object_id=interest_id, profile_id=self.pk)
        interest.delete()

    def is_this_interested_by_me(self, entity):
        ct_id = ContentType.objects.get_for_model(entity).pk
        return len(self.profile_interest.filter(object_id=entity.id, content_type_id=ct_id)) == 1

    def interest_this(self, entity):
        if self.is_this_interested_by_me(entity):
            self.delete_interest(entity, entity.id)
        else:
            # add interest
            self.add_interest(entity)
        return self.is_this_interested_by_me(entity)

    def add_bookmark(self, bookmark_obj):
        ct_id = ContentType.objects.get_for_model(bookmark_obj).pk
        existing_interest = Bookmark.objects.filter(
            content_type_id=ct_id, profile_id=self.pk,
            object_id=bookmark_obj.pk
        )
        # If doesnt exist create interest and relations
        if len(existing_interest) == 0:
            bookmark = Bookmark(content_object=bookmark_obj)
            bookmark.profile = self
            bookmark.save()

    def get_bookmarks(self, filter_class=None):
        bookmarks = [x.get() for x in self.profile_bookmark.all()]
        if filter_class == 'events' or filter_class == 'news':
            res = ModelHelper.filter_instance_list_by_class(bookmarks, EntityProxy, filter_class)
            return res
        else:
            filter_class = ModelHelper.get_by_name(EntityProxy.singular_name(filter_class))
            return ModelHelper.filter_instance_list_by_class(bookmarks, filter_class)

    def is_this_bookmarked_by_me(self, entity):
        return len(self.profile_bookmark.filter(object_id=entity.id)) == 1

    def bookmark_this(self, entity):
        if self.is_this_bookmarked_by_me(entity):
            # remove bookmark
            self.delete_bookmark(entity, entity.id)
        else:
            # add bookmark
            self.add_bookmark(entity)

        return len(self.profile_bookmark.filter(object_id=entity.id)) == 1

    def delete_bookmark(self, bookmark_obj, bookmark_id):
        # Get interest-related-model class type id
        ct_id = ContentType.objects.get_for_model(bookmark_obj).pk
        # Get Interest record
        bookmark = Bookmark.objects.filter(content_type_id=ct_id, object_id=bookmark_id, profile_id=self.pk)
        bookmark.delete()

    def set_crm_id(self, crm_id):
        self.crm_id = crm_id
        self.save()

    def get_crm_id_and_save(self, force=False):
        from crmconnector.models import CRMConnector
        try:
            if not self.crm_id or force:
                print('no_crmid')
                crm_user = CRMConnector.search_party_by_email(self.user.email)
                self.crm_id = crm_user['id'] if 'id' in crm_user else None
                self.save()
        except Exception as e:
            print(e)


class Invitation(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    sender_email = models.EmailField(_('Sender email address'), max_length=254)
    sender_first_name = models.TextField(_('Sender first name'), max_length=200, null=False, blank=False, default='--')
    sender_last_name = models.TextField(_('Sender last name'), max_length=200, null=False, blank=False, default='--')

    receiver_email = models.EmailField(_('Receiver email address'), max_length=254)
    receiver_first_name = models.TextField(_('Receiver first name'), max_length=200, null=False, blank=False, default='--')
    receiver_last_name = models.TextField(_('Receiver last name'), max_length=200, null=False, blank=False, default='--')

    sender_verified = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, sender_email, sender_first_name, sender_last_name, receiver_email, receiver_first_name,
               receiver_last_name, sender_verified=True, user=None):

        # @TODO: remove when sanitize old user whit no profile from db
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        try:
            cls.__validate(sender_email=sender_email, receiver_email=receiver_email)
        except:
            raise

        # try:
        #     Invitation.objects.get(receiver_email=HashHelper.md5_hash(receiver_email))
        #     raise UserAlreadyInvited
        # except Invitation.DoesNotExist:
        #     pass

        invitation = cls(
            profile=profile,
            sender_email=HashHelper.md5_hash(sender_email) if not profile else sender_email,
            sender_first_name=HashHelper.md5_hash(sender_first_name) if not profile else sender_first_name,
            sender_last_name=HashHelper.md5_hash(sender_last_name) if not profile else sender_last_name,
            receiver_first_name=HashHelper.md5_hash(receiver_first_name),
            receiver_last_name=HashHelper.md5_hash(receiver_last_name),
            receiver_email=HashHelper.md5_hash(receiver_email),
            sender_verified=sender_verified
        )
        invitation.save()
        return invitation

    @classmethod
    def __validate(cls, sender_email, receiver_email, user=None):

        # Check if SENDER try to invite himself -> SelfInvitation
        if sender_email == receiver_email:
            raise SelfInvitation

        # Check if RECEIVER is already a member -> EmailAlreadyUsed
        try:
            User.objects.get(email=receiver_email)
            raise EmailAlreadyUsed
        except User.DoesNotExist:
            pass

        # Check if SENDER has already send invitation to RECEIVER -> UserAlreadyInvited
        if Invitation.get_by_email(receiver_email=receiver_email, sender_email=sender_email):
            raise UserAlreadyInvited


    @classmethod
    def get_by_email(cls, sender_email=None, receiver_email=None):
        q = Q()
        sender_email and q.add(Q(sender_email=HashHelper.md5_hash(sender_email)) | Q(sender_email=sender_email), q.AND)
        receiver_email and q.add(Q(receiver_email=HashHelper.md5_hash(receiver_email)) | Q(receiver_email=receiver_email), q.AND)
        return cls.objects.filter(q).distinct()

    @classmethod
    def can_invite(cls, sender_email, receiver_email):
        return len(cls.get_by_email(sender_email, receiver_email)) < 1

    @classmethod
    def deobfuscate_email(cls, email, first_name=None, last_name=None):
        hashed = HashHelper.md5_hash(email)
        sender_dict = {
            'sender_email': email,
            'sender_first_name': first_name,
            'sender_last_name': last_name
        }
        receiver_dict = {
            'receiver_email': email,
            'receiver_first_name': first_name,
            'receiver_last_name': last_name
        }
        cls.objects.filter(sender_email=hashed).update(**{k: v for k, v in sender_dict.items() if v is not None})

    @classmethod
    def confirm_sender(cls, sender_email, receiver_email):
        try:
            cls.__validate(sender_email=sender_email, receiver_email=receiver_email)
        except UserAlreadyInvited:
            pass
        except:
            raise

        existent_invitation = cls.objects.filter(
            sender_email=HashHelper.md5_hash(sender_email),
            receiver_email=HashHelper.md5_hash(receiver_email)
        )
        if len(existent_invitation):
            existent_invitation[0].sender_verified = True
            existent_invitation[0].save()
            return existent_invitation[0]
        else:
            return False


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message_text = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=dt.now)
    # type = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('created_at', 'title',)

    @classmethod
    def create(cls, user, title, message_text):
        model = cls(cls, user, title, message_text)
        return model

    def __str__(self):
        return self.message_text


class Company(models.Model):
    logo = models.ImageField(_('Logo'), upload_to='images/company')
    name = models.CharField(_('Name'), max_length=200, null=False, blank=False)
    description = models.TextField(_('Description'), null=False, blank=False)
    tags = models.ManyToManyField(Tag, related_name='company_tags')

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile_bookmark', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get(self):
        return self.content_object


class Interest(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile_interest', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def get(self):
        return self.content_object

    def __str__(self):
        return 'Interest(Profile=' + str(self.profile.pk) + ', ' +self.content_object.__class__.__name__ + '=' + str(self.object_id)+')'


class Challenge(models.Model):

    les_choices = (
        (0, 'Spain'),
        (1, 'Italy'),
        (2, 'Slovakia'),
        (3, 'United Kingdom'),
    )

    company = models.ForeignKey(Company, related_name='challenges', blank=True, null=True, on_delete=models.CASCADE)

    title = models.CharField(_('Title'), max_length=50)
    description = models.CharField(_('Description'), max_length=200)
    picture = models.ImageField(_('Challenge picture'), upload_to='images/challenge')

    details = models.TextField(_('Details'))

    tags = models.ManyToManyField(Tag, related_name='challenge_tags')

    start_date = models.DateTimeField(_('Start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End date'), blank=True, null=True)

    coordinator_email = models.EmailField(_('Coordinator email address'), max_length=254)
    notify_admin = models.BooleanField(_('Notifiy Coordinator when user add/remove interest'), default=True)
    notify_user = models.BooleanField(_('Notifiy User when removes interest'), default=True)

    les = models.IntegerField(default=0, choices=les_choices)
    profile = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    published = models.BooleanField(_('Published'), default=False)
    closed = models.BooleanField(_('Closed'), default=False)
    restricted_to = models.CharField(_('Restricted to area of'), max_length=100, blank=True)

    interest = GenericRelation(Interest)

    def interested(self, filter_class=None):
        interests = self.interest.all().order_by('-created_at')
        interested = [x.profile for x in interests] if len(interests) > 0 else []
        return ModelHelper.filter_instance_list_by_class(interested, filter_class)

    @classmethod
    def create(cls, title):
        model = cls(title=title)
        model.save()
        return model

    @staticmethod
    def retrieve_les_label(code):
        for les in Challenge.les_choices:
            if code == les[0]:
                return les[1]
        return 'less found undefined'

    def __str__(self):
        return self.title

    def clean(self):
        if not self.profile and not self.company:
            raise ValidationError('Provide a company or a profile as promoter of this challenge')
        elif self.profile and self.company:
            raise ValidationError('You can choose a profile OR a company as promoter of this challenge no both of them')


class Project(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project_contributors = models.ManyToManyField(Profile, related_name='project_contributors',
                                                  through='ProjectContributor')
    name = models.CharField(_('Name'), max_length=50, default='')
    picture = models.ImageField(_('Challenge picture'), upload_to='images/projects')
    description = models.TextField(_('Description'), default='')
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)

    start_date = models.DateTimeField(_('Start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End date'), blank=True, null=True)

    project_url = models.CharField(_('Title'), max_length=50, blank=True, null=True)

    creator_role = models.TextField(_('Creator Role'), blank=True, null=True)

    interest = GenericRelation(Interest)

    def __str__(self):
        return self.name

    def interested(self, filter_class=None):
        interests = self.interest.all().order_by('-created_at')
        interested = [x.profile for x in interests] if len(interests) > 0 else []
        return ModelHelper.filter_instance_list_by_class(interested, filter_class)

    def get_tags(self):
        return self.tags.all()
        #return map(lambda x: x.name, self.tags.all())

    def set_tags(self, tags):
        self.tags.clear()
        for tagName in [x.lower().capitalize() for x in tags.split(",")]:
            self.tags.add(Tag.objects.filter(name=tagName).first() or Tag.create(name=tagName))


class ProjectContributor(models.Model):
    # ToDo add token to avoid actions not allowed
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(_('Status'), max_length=50, default='pending')


class EntityProxy(models.Model):
    externalId = models.CharField(default='0', max_length=50)
    # NB type MUST be:
    # - news
    # - events
    type = models.CharField(_('Type'), max_length=50, default='news')

    interest = GenericRelation(Interest)

    class Meta:
        unique_together = ('externalId', 'type',)

    def interested(self, filter_class=None):
        interests = self.interest.all().order_by('-created_at')
        interested = map(lambda x: x.profile, interests) if len(interests) > 0 else []
        return ModelHelper.filter_instance_list_by_class(interested, filter_class)

    def get_real_object(self):
        '''
        You should be able to return a complete object from proxy using the external_id
        :return: complete object parsed by Watchtower
        '''
        method_to_call = 'get_' + self.type + '_detail'
        results = getattr(DSPConnectorV13, method_to_call)(entity_id=self.externalId)[self.type]
        return results

    @classmethod
    def singular_name(cls, name=None):
        return re.sub(r'^(?!news)(\w+)s$', r'\1', name) if name else ''
