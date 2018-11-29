# -*- coding: utf-8 -*-
import json
from json_tricks.nonp import dump, dumps, load, loads, strip_comments
from crmconnector.capsule import CRMConnector
from copy import copy, deepcopy
from utils.Colorizer import Colorizer

class Party(object):

    __capsule_party = None
    __local_user = None

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

        self.__set_user(user)

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
            tags = list(set([x.name for x in user.profile.tags.all() if x.name is not None and x.name is not '']))
            self.tags = [{'name': x} for x in tags]
        if user.profile.organization:
            self.organisation = {'name': user.profile.organization}

        # Custom Fields
        for custom_id, local_value in self.get_custom_field(user).items():
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

        self.websites.append({
            'service': 'TWITTER',
            'address': user.profile.twitterauth.screen_name if hasattr(user.profile, 'twitterauth') else user.profile.twitter_username
        })

    def __str__(self):
        return dumps(self)

    def as_dict(self):
        return dict((x, y) for x, y in self.__dict__.items() if x[:6] != '_Party')

    def __set_user(self, user):
        self.__local_user = user

    def __set_party(self, party):
        self.__capsule_party = party

    ###################
    # PUBLIC METHODS #
    ##################

    def get_custom_field(self, user):
        import datetime
        birthdate = ''

        try:
            birthdate = user.profile.birthdate if isinstance(user.profile.birthdate, str) else user.profile.birthdate.strftime("%Y-%m-%d")
        except:
            pass

        custom_fields = {
            '444006': user.profile.city,
            #'448805': user.profile.sector,
            #'411952': user.profile.size,
            #'444014': user.profile.technical_expertise,
            #'412036': user.profile.technical_expertise,
            '444008': user.profile.occupation,
            '444007': user.profile.birthdate
                if isinstance(user.profile.birthdate, str)
                else user.profile.birthdate.strftime("%Y-%m-%d"),
            '411953': user.profile.gender.capitalize(),
            '444016': user.profile.statement if not user.profile.statement or len(user.profile.statement) < 250 else user.profile.statement[:247]+'...',

            # Types of innovation
            #'411984': 'Product innovation' in user.profile.types_of_innovation,
            #'411985': 'Process innovation' in user.profile.types_of_innovation,
            #'411987': 'Technological innovation' in user.profile.types_of_innovation,
            #'411988': 'Business model innovation' in user.profile.types_of_innovation,
            #'411989': 'Social innovation' in user.profile.types_of_innovation,

            #Other
            #'450899': user.profile.technical_expertise_other,
            #'450898': user.profile.role_other,
            #'450900': user.profile.sector_other,

            # @TODO: make methods in model that saves and retrieve this
            #'444010': ','.join(map(lambda x: x.name, user.profile.source_of_inspiration.all())) if len(user.profile.source_of_inspiration.all()) > 0 else None
        }

        return dict((k, v) for k, v in custom_fields.items() if v)

    def update(self):
        self.__capsule_party and self.get()
        return CRMConnector.update_party(self.__capsule_party['id'], {'party': self.as_dict()})

    def create(self):
        return CRMConnector.add_party({'party': self.as_dict()})

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
        from .exceptions import CRMdeletePartyException
        self.get()
        try:
            if self.__capsule_party:
                return CRMConnector.delete_party(self.__capsule_party['id'])
        except:
            raise CRMdeletePartyException
        # @TODO : write error/exception
        return 'error'

    def create_or_update(self, safe=False):
        from .capsule import CRMValidationException
        self.get()
        if self.__capsule_party:
            clone = self.__merge_all()
            try:
                return clone.update()
            except CRMValidationException as e:
                return clone.safe_update()
        return self.create()

    def safe_update(self):
        self.emailAddresses[0]['address'] in self.__capsule_party['emailAddresses'] and self.emailAddresses.pop(0)
        self.__exclude_custom_fields()
        return CRMConnector.update_party(self.__capsule_party['id'], {'party': self.as_dict()})

    def safe_create_or_update(self):
        self.__exclude_custom_fields()
        return self.create_or_update()

    def get_crm_id(self):
        try:
            return self.__capsule_party['id']
        except:
            return False

    ###################
    # PRIVATE METHODS #
    ###################

    # Check for custom field type or data not compatible with analogous on CRM
    # If data does no math will be unset before save/update
    def __exclude_custom_fields(self):
        remote_custom_fields = self.get_custom_field_definitions()
        for field in self.fields:
            customs = filter(lambda x: x['id'] == field['definition']['id'], remote_custom_fields)
            try:
                custom = customs[0]
                if custom['type'] == 'list' and not field['value'] in custom['options']:
                    print(Colorizer.Yellow('Excluding field : {} ',format(field)))
                    self.fields.remove(field)
                    print(Colorizer.Yellow('Field Excluded'))
            except:
                pass

    # CRM does not check for duplicated on some fields
    # Those methods find match between local and CRM data an merge in unique object without duplicates
    def __merge_all(self):
        clone = deepcopy(self)
        clone.__merge_email()
        clone.__delete_remote_websites_and_add_local()
        return clone

    def __merge_email(self):
        if self.__capsule_party and len(self.__capsule_party['emailAddresses']) > 0:
            self.emailAddresses = self.__capsule_party['emailAddresses']
            try:
                emails = [x['address'] for x in self.emailAddresses]
                self.__local_user.email not in emails and self.emailAddresses.append({'address': self.__local_user.email})
            except Exception as e:
                print('CRM MODEL ERROR: error adding email to party contacts')
                print(e)

    # Set delete flag to remote websites and add local to websites field
    # Will remove all websites on capsule crm
    def __delete_remote_websites_and_add_local(self):
        self.websites = self.websites + [x.update({'_delete': True}) or x for x in self.__capsule_party['websites']]

    # Merge remote websites with local
    # Will keep remote websites and update with local values if local name match
    def __merge_remote_websites_with_local(self):
        for key in self.__capsule_party['websites'].iterkeys():
            self.__capsule_party['websites'][key]['_delete'] = True
        if self.__capsule_party and len(self.__capsule_party['websites']) > 0 and len(self.websites) > 0:
            self.websites = [self.__get_merged_websites(x) for x in self.websites ]

    def __get_merged_websites(self, local_social):
        match = filter(lambda x: x['service'] == local_social['service'], self.__capsule_party['websites'])
        try:
            match[0]['address'] = local_social['address']
            return match[0]
        except Exception as e:
            print(e)
            pass
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


