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




