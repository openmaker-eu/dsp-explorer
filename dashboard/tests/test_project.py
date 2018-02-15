# coding=utf-8
from django.test import TestCase, Client
from utils import testhelpers
from dashboard.models import Profile
import json
from dashboard.models import Profile, User, SourceOfInspiration, Tag, Project, Interest, Company
from django.shortcuts import render, reverse
from utils.Colorizer import Colorizer
import datetime
import pytz
from django.utils import timezone


class ProjectTestCase(TestCase):

    user = None

    @classmethod
    def setUpTestData(cls):
        user = testhelpers.create_test_user()
        cls.user = User.objects.get(email=user.email)

    def test1_create_project(self):
        print Colorizer.LightPurple('\n[TEST project] should create a project')
        project = Project(
            title='Prova project',
            picture='images/profile/default_user_icon.png',
            details='Prova description'
        )
        project.profile = self.user.profile
        project.save()
        self.assertTrue(Project.objects.get(title='Prova project'), Colorizer.Red('Create project Error'))

    def test2_add_project_contributor(self):
        print Colorizer.LightPurple('\n[TEST project] should add a contributor to project')
        project = Project(
            title='Prova project',
            picture='images/profile/default_user_icon.png',
            details='Prova description'
        )
        project.profile = self.user.profile
        project.save()
        project.contributors.add(self.user.profile)
        project.save()

        new_project = Project.objects.get(title='Prova project')

        self.assertGreater(len(new_project.contributors.all()), 0, Colorizer.Red('Add contributor to project error'))

    # def test3_get_profile_from_project(self):
    #     print Colorizer.LightPurple('\n[TEST project] should add a contributor to project')
    #     project = Project(
    #         title='Prova project',
    #         picture='images/profile/default_user_icon.png',
    #         details='Prova description'
    #     )
    #     project.profile = self.user.profile
    #     project.save()
    #     new_project = Project.objects.get(title='Prova project')
    #
    #     self.assertGreater(len(new_project.contributors.all()), 0, Colorizer.Red('Add contributor to project error'))


    # def test2_profile_interest_in_project(self):
    #     print Colorizer.LightPurple('\n[TEST project] should link an interest(project)')
    #
    #     project.create('test project')
    #     project = project.objects.get(title='test project')
    #
    #     self.user.profile.add_interest(project)
    #     interests = self.user.profile.get_interests()
    #
    #     self.assertGreater(len(interests), 0, Colorizer.Red('No project linked'))
    #
    # def test3_profile_interest_in_company(self):
    #     print Colorizer.LightPurple('\n[TEST project] should link an interest(Company)')
    #
    #     self.user.profile.add_interest(self.company)
    #     interests = self.user.profile.get_interests()
    #
    #     self.assertGreater(len(interests), 0, Colorizer.Red('No Company linked'))
    #
    # def test4_profile_filter_interest_project(self):
    #     print Colorizer.LightPurple('\n[TEST project] should return only interests that are projects')
    #
    #     project.create('test project')
    #     project = project.objects.get(title='test project')
    #     self.user.profile.add_interest(project)
    #
    #     self.user.profile.add_interest(self.company)
    #     interests = self.user.profile.get_interests(project)
    #
    #     self.assertTrue(all(isinstance(x, project) for x in interests), Colorizer.Red('Filter interest does not return a list of project'))
    #
    # def test5_get_interested_from_project(self):
    #     print Colorizer.LightPurple('\n[TEST project] should return a list of profile interested in a project')
    #
    #     project.create('test project')
    #     project = project.objects.get(title='test project')
    #     self.user.profile.add_interest(project)
    #
    #     profiles = project.interested()
    #
    #     self.assertTrue(all(isinstance(x, Profile) for x in profiles), Colorizer.Red('project related interest are not a porofile list'))
    #
    # def test6_delete_interest_from_profile(self):
    #     print Colorizer.LightPurple('\n[TEST project] should should delete interest(project) from profile')
    #
    #     project.create('test project')
    #     project = project.objects.get(title='test project')
    #     self.user.profile.add_interest(project)
    #
    #     self.user.profile.delete_interest(project, project.id)
    #     projects = self.user.profile.get_interests(project)
    #
    #     self.assertEqual(len(projects), 0, Colorizer.Red('User interest(project) is not deleted'))
    #



