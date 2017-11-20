# -*- coding: utf-8 -*-
import json
from django.forms.models import model_to_dict
from django.db import models
import itertools
from django.db.models.query import QuerySet
from json_tricks.np import dump, dumps, load, loads, strip_comments
import operator
from capsule import CRMConnector
from copy import copy, deepcopy
from utils.Colorizer import Colorizer
from itertools import chain


class Party(object):

    __capsule_party = None
    __local_email = None
    __local_websites = None
    __social_allowed_names = {

        'SKYPE': 'SKYPE',
        'TWITTER': 'TWITTER',
        'FACEBOOK': 'FACEBOOK',
        'XING': 'XING',
        'FEED': 'FEED',
        'FLICKR': 'FLICKR',
        'GITHUB': 'GITHUB',
        'YOUTUBE': 'YOUTUBE',
        'INSTAGRAM': 'INSTAGRAM',
        'PINTEREST': 'PINTEREST',

        'GOOGLE_PLUS': 'GOOGLE_PLUS',
        'GOOGLEPLUS': 'GOOGLE_PLUS',
        'GOOGLE-PLUS': 'GOOGLE_PLUS',

        'LINKED_IN': 'LINKED_IN',
        'LINKEDIN': 'LINKED_IN',
        'LINKED-IN': 'LINKED_IN',
    }

    def __init__(self, user):

        self.__local_email = user.email

        # Standard Mandatory Fields
        self.fields = []
        self.type = 'person'
        self.firstName = user.first_name
        self.lastName = user.last_name
        self.emailAddresses = [{'address': user.email}]
        self.jobTitle = user.profile.occupation

        self.__social_links = json.loads(user.profile.socialLinks)

        # Standard Optional Fields
        if len(user.profile.tags.all()) > 0:
            self.tags = map(lambda x: {'name': x.name}, user.profile.tags.all())
        if user.profile.organization:
            self.organisation = {'name': user.profile.organization}

        # Custom Fields
        for custom_id, local_value in self.get_custom_field(user).iteritems():
            if local_value and local_value is not None and local_value != '':
                self.fields.append({
                    "value": local_value,
                    "definition": {"id": int(custom_id)}
                })

        self.websites = []
        for social in self.__social_links:
            if social['link'] != '' and social['name'].upper() in self.__social_allowed_names:
                self.websites.append({
                    'service': self.__social_allowed_names[social['name'].upper()],
                    'address': social['link']
                })

    def __str__(self):
        return dumps(self)

    def as_dict(self):
        # return dict((x, y) for x, y in self.__dict__.items() if x[:1] != '_')
        return self.__dict__

    ###################
    # PUBLIC METHODS #
    ##################

    def get_custom_field(self, user):

        custom_fields = {
            '444006': user.profile.city,
            '448805': user.profile.sector,
            '411952': user.profile.size,
            '444014': user.profile.technical_expertise,
            '412036': user.profile.technical_expertise,
            '444008': user.profile.occupation,
            '444007': user.profile.birthdate.strftime("%Y-%m-%d"),
            '411953': user.profile.gender.capitalize(),
            '444016': user.profile.statement if len(user.profile.statement) < 250 else user.profile.statement[:247]+'...',

            # # Types of innovation
            '411984': 'Product innovation' in user.profile.types_of_innovation,
            '411985': 'Process innovation' in user.profile.types_of_innovation,
            '411987': 'Technological innovation' in user.profile.types_of_innovation,
            '411988': 'Business model innovation' in user.profile.types_of_innovation,
            '411989': 'Social innovation' in user.profile.types_of_innovation,

            # @TODO: make methods in model that saves and retrieve this
            '444010': ','.join(map(lambda x: x.name, user.profile.source_of_inspiration.all())) if len(user.profile.source_of_inspiration.all()) > 0 else None
        }

        return dict((k, v) for k, v in custom_fields.iteritems() if v)

    def update(self):
        self.__capsule_party and self.get()
        # print json.dumps(self.as_dict(), indent=1)
        CRMConnector.update_party(self.__capsule_party['id'], {'party': self.as_dict()})

    def create(self):
        CRMConnector.add_party({'party': self.as_dict()})

    def get(self):
        remote_party = CRMConnector.search_party_by_email(self.emailAddresses[0]['address'])
        if remote_party:
            self.__capsule_party = remote_party
        else:
            self.__capsule_party = None
        return remote_party

    def delete(self):
        if not self.__capsule_party:
            # @TODO : write error/exception
            return 'No remote id set'
        return CRMConnector.delete_party(self.__capsule_party['id'])

    def find_and_delete(self):
        self.get()
        if self.__capsule_party:
            return CRMConnector.delete_party(self.__capsule_party['id'])
        # @TODO : write error/exception
        return 'error'

    def create_or_update(self):
        self.get()
        if self.__capsule_party:
            clone = self.__merge_all()
            return clone.update()
        return self.create()

    def safe_update(self):
        self.emailAddresses[0]['address'] in self.__capsule_party['emailAddresses'] and self.emailAddresses.pop(0)
        self.__exclude_custom_fields()
        return CRMConnector.update_party(self.__capsule_party['id'], {'party': self.as_dict()})

    def safe_create_or_update(self):
        self.__exclude_custom_fields()
        return self.create_or_update()

    ###################
    # PRIVATE METHODS #
    ###################

    # Check for custom field type or data not compatible with analogous on CRM
    # If data does no math will be unset before save/update
    def __exclude_custom_fields(self):
        remote_custom_fields = self.get_custom_field_definitions()
        for field in self.fields:
            customs = filter(lambda x: x['id'] == field['definition']['id'], remote_custom_fields)
            if len(customs) > 0:
                custom = customs[0]
                if custom['type'] == 'list' and not field['value'] in custom['options']:
                    print Colorizer.Yellow('Excluding field : %s ' % field)
                    self.fields.remove(field)
                    print Colorizer.Yellow('Field Excluded')

        # print Colorizer.Green('USER DATA :')
        # print Colorizer.Yellow(json.dumps(self.as_dict(), indent=2))

    # CRM does not check for duplicated on some fields
    # Those methods find match between local and CRM data an merge in unique object without duplicates
    def __merge_all(self):
        clone = deepcopy(self)
        clone.__merge_email()
        clone.__merge_websites()
        return clone

    def __merge_email(self):
        if self.__capsule_party and len(self.__capsule_party['emailAddresses']) > 0:
            self.emailAddresses = self.__capsule_party['emailAddresses']
            email_match = filter(lambda x: x['address'] == self.__local_email, self.__capsule_party['emailAddresses'])
            if len(email_match) == 0:
                self.emailAddresses.append({'address': self.__local_email})

    def __merge_websites(self):
        # for key in self.__capsule_party['websites'].iterkeys():
        #     self.__capsule_party['websites'][key]['_delete'] = True
        self.websites = self.websites + map(self.prova, self.__capsule_party['websites'])

        # if self.__capsule_party and len(self.__capsule_party['websites']) > 0 and len(self.websites) > 0:
        #     self.websites = map(
        #         lambda x: self.__get_merged_websites(x),
        #         self.websites
        #     )

    def prova(self, website):
        website['_delete'] = True
        return website

    def __get_merged_websites(self, local_social):
        match = filter(lambda x: x['service'] == local_social['service'], self.__capsule_party['websites'])
        if len(match) > 0:
            match[0]['address'] = local_social['address']
            return match[0]
        return local_social

    # ###############
    # CLASS METHODS #
    # ###############

    @classmethod
    def all(cls):
        return CRMConnector.get_all_parties()

    @classmethod
    def get_custom_field_definitions(cls):
        return CRMConnector.get_custom_field_definitions('parties')


