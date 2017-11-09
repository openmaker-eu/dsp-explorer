from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime as dt
from utils.hasher import HashHelper
import uuid
from .exceptions import EmailAlreadyUsed, UserAlreadyInvited


class Tag(models.Model):
    name = models.TextField(_('Name'), max_length=200, null=False, blank=False)

    @classmethod
    def create(cls, name):
        tag = Tag(name=name)
        tag.save()
        return tag


class SourceOfInspiration(models.Model):
    name = models.TextField(_('Name'), max_length=200, null=False, blank=False)

    @classmethod
    def create(cls, name):
        source = SourceOfInspiration(name=name)
        source.save()
        return source


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

    tags = models.ManyToManyField(Tag, related_name='profile_tags')
    source_of_inspiration = models.ManyToManyField(SourceOfInspiration, related_name='profile_sourceofinspiration')

    socialLinks = models.TextField(
        _('Social Links'),
        max_length=200,
        null=True,
        blank=True,
        default='[{"name":"twitter","link":""},{"name":"google-plus","link":""},{"name":"facebook","link":""}]'
    )

    # Reset Password
    reset_token = models.TextField(max_length=200, null=True, blank=True)
    update_token_at = models.DateTimeField(default=None, null=True, blank=True)
    ask_reset_at = models.DateTimeField(default=dt.now, null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.get_name(), self.get_last_name())
    
    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ('user',)

    @classmethod
    def create(cls, email, first_name, last_name, picture, password=None, gender=None,
               birthdate=None, city=None, occupation=None, twitter_username=None, place=None):

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email,
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

    def send_email(self, subject, message):
        """
        Send Async Email to the user
        :param subject: Subject of the email
        :param message: Email Content
        :return: Nothing
        """
        import threading
        thr = threading.Thread(target=Profile._send_email,
                               kwargs=dict(message=message,
                                           subject=subject,
                                           receiver_name=self.user.get_full_name(),
                                           receiver_email=self.user.email
                                           ))
        thr.start()

    def get_name(self):
        import unicodedata
        return unicodedata.normalize('NFKD', self.user.first_name).encode('ascii', 'ignore')

    def get_last_name(self):
        import unicodedata
        return unicodedata.normalize('NFKD', self.user.last_name).encode('ascii', 'ignore')

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
    def search_members(cls, search_string):
        from django.db.models import Q
        return cls.objects\
            .filter(Q(user__email__icontains=search_string) |
                Q(user__first_name__icontains=search_string) |
                Q(user__last_name__icontains=search_string) |
                Q(tags__name__icontains=search_string) |
                Q(twitter_username__icontains=search_string) |
                Q(occupation__icontains=search_string) |
                Q(city__icontains=search_string))\
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
    def create(cls, user, sender_email, sender_first_name, sender_last_name, receiver_email, receiver_first_name,
               receiver_last_name, sender_verified=True):
        try:
            Invitation.objects.get(receiver_email=HashHelper.md5_hash(receiver_email))
            raise UserAlreadyInvited
        except Invitation.DoesNotExist:
            pass
        try:
            user = User.objects.get(email=receiver_email)
            raise EmailAlreadyUsed
        except User.DoesNotExist:
            pass

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None
            
        invitation = cls(profile=profile,
                         sender_email=HashHelper.md5_hash(sender_email) if not profile else sender_email,
                         sender_first_name=HashHelper.md5_hash(sender_first_name) if not profile else sender_first_name,
                         sender_last_name=HashHelper.md5_hash(sender_last_name) if not profile else sender_last_name,
                         receiver_first_name=HashHelper.md5_hash(receiver_first_name),
                         receiver_last_name=HashHelper.md5_hash(receiver_last_name),
                         receiver_email=HashHelper.md5_hash(receiver_email),
                         sender_verified=sender_verified)
        invitation.save()
        return invitation


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
