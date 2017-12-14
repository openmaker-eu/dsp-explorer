# coding=utf-8
from django.test import TestCase, Client
from utils import testhelpers
from dashboard.models import Profile
import json
from dashboard.models import Profile, User, SourceOfInspiration, Tag, Invitation
from django.shortcuts import render, reverse
from utils.Colorizer import Colorizer
import datetime
import pytz
from django.utils import timezone
from dashboard.exceptions import EmailAlreadyUsed, UserAlreadyInvited, SelfInvitation, InvitationAlreadyExist, InvitationDoesNotExist
from utils.hasher import HashHelper


class ProfileTestCase(TestCase):

    client = Client()
    user = None
    password = '12345678'

    @classmethod
    def setUpTestData(cls):
        user = testhelpers.create_test_user()
        cls.user = User.objects.filter(email=user.email)[0]
        cls.login()
        cls.reset_invitations()

    #############
    # UNIT TEST #
    #############

    # Invitation Find By Email
    def test0_invitation_search_by_email_obfuscated(self):
        # assert should find obfuscated email providing clear email
        self.assertGreater(len(Invitation.get_by_email(sender_email=self.invitation['sender_email'])), 0, 'Cannot find invitatiton by email')

    def test0_invitation_search_by_email_not_obfuscated(self):
        # assert should find clear email providing clear email
        invitation = Invitation.objects.get(sender_email=HashHelper.md5_hash(self.invitation_2['sender_email']))
        invitation.sender_email = self.invitation_2['sender_email']
        invitation.save()
        self.assertGreater(len(Invitation.get_by_email(sender_email=self.invitation_2['sender_email'])), 0, 'Cannot find invitatiton by email')

    # Invitation Can invite
    def test0_invitation_cannot_invite(self):
        # assert should return false if invitation exist
        self.assertFalse(
            Invitation.can_invite(
                sender_email=self.invitation['sender_email'],
                receiver_email=self.invitation['receiver_email']
            ),
            'Can invite should return return false if invitation exist'
        )

    def test0_invitation_can_invite(self):
        # assert should return true if invitation does not exist
        self.assertTrue(
            Invitation.can_invite(
                sender_email=self.invitation['sender_email'],
                receiver_email='i_do_not_exist@fakeuser.ix'
            ),
            'Can invite function should return true if invitation does not exist'
        )

    # Invitation Creation
    def test1_invitation_create_non_member_email(self):
        # assert should create invitation for both non-members data
        self.assertGreater(len(Invitation.objects.all()), 0, 'Cannot create invitation')

    def test2_invitation_confirm_sender_exist(self):
        # assert should confirm invitation if sender exist
        Invitation.confirm_sender(sender_email=self.invitation['sender_email'], receiver_email=self.invitation['receiver_email'])
        confirmed = Invitation.get_by_email(sender_email=self.invitation['sender_email'])
        self.assertTrue(confirmed[0].sender_verified, 'Invitation should be confirmed with existing sender and receiver emails')

    # Invitation Confirmation
    def test3_invitation_confirm_sender_doesnt_exist(self):
        # assert should not confirm invitation if invitation does not exist
        Invitation.confirm_sender(sender_email='i_do_not_exist@fakeuser.ix', receiver_email=self.invitation['receiver_email'])
        confirmed = Invitation.get_by_email(sender_email=self.invitation['sender_email'])
        self.assertFalse(confirmed[0].sender_verified, 'Invitation should not be confirmed with fake email')

    def test4_invitation_confirm_receiver_exist(self):
        # assert should not create invitation if receiver is already a member
        clone = {k: v for k, v in self.invitation.items()}
        clone['receiver_email'] = self.user.email
        self.assertRaises(EmailAlreadyUsed, Invitation.create, **clone)

    # Invitation deobfuscate emails
    def test5_invitation_debfuscation_exist(self):
        # assert should deobfuscate invitation
        Invitation.deobfuscate_email(self.invitation['sender_email'])
        invitation = Invitation.get_by_email(receiver_email=self.invitation['receiver_email'])
        self.assertEqual(
            invitation[0].__dict__['sender_email'],
            self.invitation['sender_email'],
            'Should deobfuscate provided email'
        )

    def test6_invitation_debfuscation_doesnt_exist(self):
        # assert should deobfuscate invitation
        Invitation.deobfuscate_email('i_do_not_exist@fakeuser.ix')
        invitation = Invitation.get_by_email(receiver_email=self.invitation['receiver_email'])
        self.assertNotEqual(
            invitation[0].__dict__['sender_email'],
            self.invitation['sender_email'],
            'Should not deobfuscate provided email'
        )

    def test7_invitation_debfuscation_first_and_last_name(self):
        # assert should deobfuscate first_name and last_name
        self.reset_invitations()
        Invitation.deobfuscate_email(self.invitation['sender_email'], self.invitation['sender_first_name'], self.invitation['sender_last_name'])
        invitation = Invitation.get_by_email(sender_email=self.invitation['sender_email'])

        self.assertEqual(
            invitation[0].sender_first_name+invitation[0].sender_last_name,
            self.invitation['sender_first_name']+self.invitation['sender_last_name'],
            'Should deobfuscate first_name and last_name'
        )

    def test8_invitation_debfuscation_first_name_only(self):
        # assert should deobfuscate first_name only
        self.reset_invitations()
        Invitation.deobfuscate_email(self.invitation['sender_email'], self.invitation['sender_first_name'])
        invitation = Invitation.get_by_email(sender_email=self.invitation['sender_email'])

        self.assertEqual(
            invitation[0].sender_first_name+invitation[0].sender_last_name,
            self.invitation['sender_first_name']+HashHelper.md5_hash(self.invitation['sender_last_name']),
            'Should deobfuscate first_name and last_name'
        )

    ###########
    # Helpers #
    ###########

    @classmethod
    def login(cls):
        return cls.client.login(username=cls.user.username, password=cls.password)

    @classmethod
    def get_profile_page(cls):
        return cls.client.get('/profile/%s/' % cls.user.profile.pk, follow=True)

    @classmethod
    def post_profile(cls, data):
        # @TODO: this not send vaid data
        extra = {'birthdate': '1983/05/14'}
        data = {
            k: v
            for to_merge in [cls.user.__dict__, cls.user.profile.__dict__, extra]
            for k, v in to_merge.items()
        }
        return cls.client.post('/profile/%s/' % cls.user.profile.pk, data, follow=True)

    @classmethod
    def post_profile_test(cls, data):
        return cls.client.post('/test/', data, follow=True)

    @classmethod
    def reset_invitations(cls):

        for invit in Invitation.objects.all():
            invit.delete()

        cls.invitation = {
            'sender_email': 'sender_email@omcon.ix',
            'sender_first_name': 'adam',
            'sender_last_name': 'sender',
            'receiver_email': 'receiver_email@omcon.ix',
            'receiver_first_name': 'adam',
            'receiver_last_name': 'receiver',
            'sender_verified': False
        }
        cls.invitation_2 = {
            'sender_email': 'sender_email_2@omcon.ix',
            'sender_first_name': 'adam',
            'sender_last_name': 'sender',
            'receiver_email': 'receiver_email_2@omcon.ix',
            'receiver_first_name': 'adam',
            'receiver_last_name': 'receiver',
            'sender_verified': False
        }
        Invitation.create(**cls.invitation)
        Invitation.create(**cls.invitation_2)


        # INVITE : as logged user i can invite people that are not om_explorer members
        # should verify that invited user does not exist on explorer : (you can only invite user that are not explorer members)
        # should verify that invited user and inviting user are different : (you can not invite yourself)
        # should verify that an indentical invitation (same sender same receiver) is not not present : (to avodid duplicate invitation and email. Returns error)
        # should verify that an invitation is not not yet confirmed : (to avodid duplicate invitation email and return error)


        # OM_CONFIRMATION : confirm sender and then sends invitatin email to the invited user
        # should verify that invited user does not exist on explorer : (you can only invite user that are not explorer members)
        # should verify that an invitation exist : (to confirm an invitation that invitation must exist)
        # should verify that an invitation is not not yet confirmed : (to avodid duplicate invitation email and return error)
        # should verify that an invitation email is not sended twice if same invited_user is invited by 2 different people : (only avoid duplicated email)





