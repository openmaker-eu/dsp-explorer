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
        cls.login()
        Invitation.create(**cls.invitation)
        Invitation.create(**cls.invitation_2)

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

        print Invitation.get_by_email(sender_email=self.invitation['sender_email'])
        print Invitation.get_by_email(receiver_email=self.invitation['receiver_email'])
        print Invitation.get_by_email(sender_email=self.invitation['sender_email'], receiver_email=self.invitation['receiver_email'])
        print Invitation.get_by_email(sender_email=self.invitation['sender_email'], receiver_email='i_do_not_exist@fakeuser.ix')
        print Invitation.get_by_email(sender_email='i_do_not_exist@fakeuser.ix', receiver_email='i_do_not_exist@fakeuser.ix')
        print 'can'
        print Invitation.can_invite(sender_email=self.invitation['sender_email'], receiver_email=self.invitation['receiver_email'])
        print Invitation.can_invite(sender_email=self.invitation['sender_email'], receiver_email='i_do_not_exist@fakeuser.ix')
        print Invitation.can_invite(sender_email='i_do_not_exist@fakeuser.ix', receiver_email='i_do_not_exist@fakeuser.ix')



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

    #######################
    # TEST PAGE RESPONSE #
    #######################

    # def test1_login(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE PAGE] test login')
    #     self.assertTrue(self.client.login(username=self.user.username, password=self.password), Colorizer.Red('Error during login'))
    #
    # def test2_response(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE PAGE] test response success')
    #     response = self.get_profile_page()
    #     self.assertLessEqual(
    #         response.status_code,
    #         202,
    #         Colorizer.Red('Response Error: \n code: %s \n Info : %s' % (response.status_code, response))
    #     )
    #
    # def test3_is_profile_page(self):
    #     print Colorizer.LightPurple('\n[TEST PROFILE PAGE] assert response is a profile page')
    #     response = self.get_profile_page()
    #     self.assertEqual(
    #         response.request['PATH_INFO'],
    #         '/profile/%s/' % self.user.profile.pk,
    #         Colorizer.Red('Response is not the profile page but : %s' % response.request['PATH_INFO'])
    #     )

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


