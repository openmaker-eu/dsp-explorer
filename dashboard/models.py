# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime as dt
from utils.hasher import HashHelper
import uuid
from .exceptions import EmailAlreadyUsed, UserAlreadyInvited, SelfInvitation, InvitationAlreadyExist, InvitationDoesNotExist
from opendataconnector.odconnector import OpenDataConnector
from restcountriesconnector.rcconnector import RestCountriesConnector
import json
from utils.GoogleHelper import GoogleHelper
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


class ModelHelper:
    @classmethod
    def filter_instance_list_by_class(cls, list_to_filter, filter_class=None):
        return filter(lambda x: isinstance(x, filter_class), list_to_filter) \
            if filter_class is not None else list_to_filter


class Tag(models.Model):
    name = models.TextField(_('Name'), max_length=200, null=False, blank=False)

    @classmethod
    def create(cls, name):
        tag = Tag(name=name)
        tag.save()
        return tag

    def __unicode__(self):
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

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(_('Picture'), upload_to='images/profile', null=True, blank=True)
    gender = models.TextField(_('Gender'), max_length=500, null=True, blank=True)
    city = models.TextField(_('City'), max_length=500, null=True, blank=True)
    occupation = models.TextField(_('Occupation'), max_length=500, null=True, blank=True)
    birthdate = models.DateTimeField(_('Birth Date'), blank=True, null=True)

    twitter_username = models.TextField(_('Twitter Username'), max_length=100, blank=True, null=True)
    place = models.TextField(_('Place'), max_length=500, blank=True, null=True)

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

    socialLinks = models.TextField(
        _('Social Links'),
        max_length=200,
        null=True,
        blank=True,
        default='[{"name":"twitter","link":""},{"name":"google-plus","link":""},{"name":"facebook","link":""}]'
    )

    def set_location(self):
        return None

    # Reset Password
    reset_token = models.TextField(max_length=200, null=True, blank=True)
    update_token_at = models.DateTimeField(default=None, null=True, blank=True)
    ask_reset_at = models.DateTimeField(default=dt.now, null=True, blank=True)

    # def __str__(self):
    #     return "%s %s" % (self.get_name(), self.get_last_name())

    def __unicode__(self):
        try:
            return self.user.email
        except:
            return 'Error'

    # def __repr__(self):
    #     return self.__str__()

    class Meta:
        ordering = ('user',)

    @classmethod
    def create(cls, email, first_name, last_name, picture, password=None, gender=None,
               birthdate=None, city=None, occupation=None, twitter_username=None, place=None):
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
    def search_members(cls, search_string, restrict_to=None):
        if restrict_to == 'tags':
            return cls.objects \
                .filter(Q(tags__name=search_string)) \
                .distinct()
        if restrict_to == 'sectors':
            return cls.objects \
                .filter(Q(sector=search_string)) \
                .distinct()

        return cls.objects\
            .filter(
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
                )\
            .distinct()

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
        from itertools import chain
        from collections import Counter
        tags = chain.from_iterable([map(lambda t: t['name'], tag) for tag in map(lambda p: p.tags.values(),
                                                                                 Profile.objects.all())])
        hot = Counter(tags).most_common(int(tag_number))
        return hot

    @classmethod
    def get_sectors(cls):
        from collections import Counter
        flat_sectors = filter(lambda x: x is not None and x.strip() != '', Profile.objects.values_list('sector',
                                                                                                       flat=True))
        sectors = Counter(flat_sectors).most_common(1000)
        return sectors

    @classmethod
    def get_places(cls):
        places = filter(lambda x: x is not None, Profile.objects.values_list('place', flat=True))
        return places

    def sanitize_place(self):
        try:
            if not self.place or 'city' not in self.place:
                city = self.city
                place = GoogleHelper.get_city(city)
                if place:
                    self.place = json.dumps(place)
                    self.save()
        except Exception as e:
            print 'error'
            print e

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
            print e

    def add_interest(self, interest_obj):
        # Check existing realation between same interest related model and same profile
        ct_id = ContentType.objects.get_for_model(interest_obj).pk
        existing_interest = Interest.objects.filter(content_type_id=ct_id, profile_id=self.pk, object_id=interest_obj.pk)
        # If doesnt exist create interest and relations
        if len(existing_interest) == 0:
            interest = Interest(content_object=interest_obj)
            interest.profile = self
            interest.save()

    def get_interests(self, filter_class=None):
        interests = map(lambda x: x.get(), self.profile_interest.all())
        return ModelHelper.filter_instance_list_by_class(interests, filter_class)

    def delete_interest(self, interest_obj, interest_id):
        # Get interest-related-model class type id
        ct_id = ContentType.objects.get_for_model(interest_obj).pk
        # Get Interest record
        interest = Interest.objects.filter(content_type_id=ct_id, object_id=interest_id)
        return interest.delete()


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
        cls.objects.filter(sender_email=hashed).update(**{k: v for k, v in sender_dict.iteritems() if v is not None})
        cls.objects.filter(receiver_email=hashed).update(**{k: v for k, v in receiver_dict.iteritems() if v is not None})

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
    user = models.ForeignKey(User)
    title = models.CharField(_('Title'), max_length=100)
    message_text = models.TextField(_('Message'), max_length=500)
    created_at = models.DateTimeField(default=dt.now)

    class Meta:
        ordering = ('created_at', 'title',)

    @classmethod
    def create(cls, user, title, message_text):
        model = cls(cls, user, title, message_text)
        return model

    def __str__(self):
        return self.message_text


class Company(models.Model):
    logo = models.ImageField(_('Company picture'), upload_to='images/company')
    name = models.CharField(_('Name'), max_length=200, null=False, blank=False)
    description = models.TextField(_('Description'), null=False, blank=False)
    tags = models.ManyToManyField(Tag, related_name='company_tags')

    def __unicode__(self):
        return self.name


class Interest(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile_interest')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def get(self):
        return self.content_object

    def __unicode__(self):
        return 'Interest(Profile=' + str(self.profile.pk) + ', ' +self.content_object.__class__.__name__ + '=' + str(self.object_id)+')'


class Challenge(models.Model):

    les_choices = (
        (0, 'Spain'),
        (1, 'Italy'),
        (2, 'Slovakia'),
        (3, 'United Kingdom'),
    )

    company = models.ForeignKey(Company, related_name='challenges', blank=True, null=True)

    title = models.CharField(_('Title'), max_length=50)
    description = models.CharField(_('Description'), max_length=200)
    picture = models.ImageField(_('Challenge picture'), upload_to='images/challenge')

    details = models.TextField(_('Details'))

    tags = models.ManyToManyField(Tag, related_name='challenge_tags')

    start_date = models.DateTimeField(_('Start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End date'), blank=True, null=True)
    coordinator_email = models.EmailField(_('Coordinator email address'), max_length=254)
    les = models.IntegerField(default=0, choices=les_choices)
    profile = models.ForeignKey(Profile, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    published = models.BooleanField(_('Published'), default=False)
    closed = models.BooleanField(_('Closed'), default=False)

    interest = GenericRelation(Interest,)

    def interested(self, filter_class=None):
        interests = self.interest.all().order_by('-created_at')
        interested = map(lambda x: x.profile, interests) if len(interests) > 0 else []
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

    def __unicode__(self):
        return self.title.encode('utf-8')

    def clean(self):
        if not self.profile and not self.company:
            raise ValidationError('Provide a company or a profile as promoter of this challenge')
        elif self.profile and self.company:
            raise ValidationError('You can choose a profile OR a company as promoter of this challenge no both of them')

