import json
from django.forms.models import model_to_dict
from django.db import models
import itertools
from django.db.models.query import QuerySet
from json_tricks.np import dump, dumps, load, loads, strip_comments
import operator
from capsule import CRMConnector

class Party(object):

    __capsule_id = None

    def __init__(self, user):
        self.__from_user(user)

    def __str__(self):
        return dumps(self)

    def __from_user(self, user):

        # Standard Fields
        self.fields = []
        self.type = 'person'
        self.firstName = user.first_name
        self.lastName = user.last_name
        self.emailAddresses = [{'address': user.email}]
        self.jobTitle = user.profile.occupation
        if len(user.profile.tags.all()) > 0:
            self.tags = map(lambda x: {'name': x.name}, user.profile.tags.all())

        # Custom Fields
        for custom_id, local_value in self.get_custom_field(user).iteritems():
            if local_value and local_value is not None and local_value != '':
                self.fields.append({
                    "value": local_value,
                    "definition": {"id": int(custom_id)}
                })

        # @TODO : Field that doesnt works
        # self.organisation = user.profile.organization

        # Picture cannot be edited according to CapsuleCRM Api
        # self.pictureUrl = ''

        # @TODO: Fields/Custom-Fields seems to dont have exact corrispondence on CapsuleCRM
        # self.twitter_username = user.profile.twitter_username
        # self.socialLinks = ''
        # self.role = ''
        # self.statement = ''

        return self

    def get_custom_field(self, user):

        print ','.join(map(lambda x: x.name, user.profile.source_of_inspiration.all()))
        return {

            '444006': user.profile.city,
            '411964': user.profile.sector,
            '411952': user.profile.size,
            '412035': user.profile.technical_expertise,
            '444008': user.profile.occupation,
            '444007': user.profile.birthdate.strftime("%Y-%m-%d"),
            '411953': user.profile.gender.capitalize(),
            # Types of innovation
            '411984': 'Product innovation' in user.profile.types_of_innovation,
            '411985': 'Process innovation' in user.profile.types_of_innovation,
            '411987': 'Technological innovation' in user.profile.types_of_innovation,
            '411988': 'Business model innovation' in user.profile.types_of_innovation,
            '411989': 'Social innovation' in user.profile.types_of_innovation,
            #@TODO: make methods in model that saves and retrieve this
            '444010': ','.join(map(lambda x: x.name, user.profile.source_of_inspiration.all())) if len(user.profile.source_of_inspiration.all()) > 0 else None,

            # @TODO: these fields does not work

        }

    def update(self):
        CRMConnector.update_party(self.__capsule_id, {'party': self.__dict__})

    def create(self):
        CRMConnector.add_party({'party': self.__dict__})

    def get(self):
        return CRMConnector.search_party_by_email(self.emailAddresses[0]['address'])

    def delete(self):
        if not self.__capsule_id:
            # @TODO : write error/exception
            return 'No remote id set'
        return CRMConnector.delete_party(self.__capsule_id)

    def find_and_delete(self):
        remote_party = self.get()
        if remote_party and remote_party['id']:
            self.__capsule_id = remote_party['id']
            return CRMConnector.delete_party(self.__capsule_id)
        # @TODO : write error/exception
        return 'error'

    def create_or_update(self):
        # Check If exist and update
        remote_party = self.get()
        if remote_party and remote_party['id']:
            self.__capsule_id = remote_party['id']
            return self.update()
        return self.create()

