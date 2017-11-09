import json
from django.forms.models import model_to_dict
from django.db import models
import itertools
from django.db.models.query import QuerySet
from json_tricks.np import dump, dumps, load, loads, strip_comments



class Party(object):
    mappings = {

        #### To remove
        'id': False,
        'password': False,
        'is_superuser': False,
        'is_staff': False,
        'is_active': False,
        'profile': False,
        'last_login': False,
        'date_joined': False,
        'ask_reset_at': False,
        'update_token_at': False,
        'reset_token': False,
        'sourceofinspiration': False,
        'user': False,
        'groups': False,
        'group': False,
        'permission': False,
        'permissions': False,

        #### To Map
        'picture': 'picture_url'

    }

    def __init__(self, user):
        self.__from_user(user)

    def __str__(self):
        return dumps(self)

    def __from_user(self, user):

        # self.fields = []
        self.type = 'person'
        self.firstName = user.first_name
        self.lastName = user.last_name
        self.emailAddresses = [{'address': user.email}]
        self.jobTitle = user.profile.occupation

        self.fields=[
            {
                "value": user.profile.source_of_inspiration or "",
                "definition": {"id": 444010}
            }
        ]

        # self.pictureURL = user.profile.picture.url if user.profile.picture else ''
        # self.twitter_username = user.profile.twitter_username

        # self.sector = ''
        # self.socialLinks = ''
        # self.types_of_innovation = ''
        # self.size = ''
        # self.city = ''
        # self.role = ''
        # self.statement = ''
        # self.occupation = ''
        # self.picture = ''
        # self.technical_expertise = ''
        # self.gender = ''
        # self.birthdate = ''
        # self.place = ''
        # self.organization = ''

        return self
