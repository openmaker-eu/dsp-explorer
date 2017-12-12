# coding=utf-8
from django.test import TestCase, Client
from dashboard.models import Profile
import json
from dashboard.models import Profile, User, SourceOfInspiration, Tag
from django.shortcuts import render, reverse
from utils.Colorizer import Colorizer
import datetime
import pytz
from django.utils import timezone

def create_test_user():
    password = '12345678'

    user_data = {
        'email': 'test_unit@test.com',
        'first_name': 'aaa_unit_test',
        'last_name': 'aaa_test_unit',
        'picture': 'images/profile/default_user_icon.png',
        'password': password,
        'gender': 'Female',
        'birthdate': '1980-01-12',
        'city': 'Torreon',
        'occupation': 'tester',
        'twitter_username': '',
        'place': '{"city":"Torreon","state":"Coah.","country_short":"MX","country":"Messico","lat":25.5428443,"long":-103.40678609999998}',
    }

    Profile.create(**user_data)
    user = User.objects.filter(email=user_data['email'])[0]
    user.is_active = True

    # Extra fields
    # cls.user.profile.types_of_innovation = 'Product innovation,Technological innovation,Business model innovation'
    user.profile.organization = 'aaa_unit_test_organization'
    user.profile.statement = 'Hi im a test user generated from unit test suite'

    ## SOP
    user.profile.source_of_inspiration.add(SourceOfInspiration.create('Apple'))
    user.profile.source_of_inspiration.add(SourceOfInspiration.create('Microsoft'))
    user.profile.source_of_inspiration.add(SourceOfInspiration.create('Samsung'))
    ## Tags
    user.profile.tags.add(Tag.create('Innovation'))
    user.profile.tags.add(Tag.create('Social'))
    user.profile.tags.add(Tag.create('Design'))

    user.profile.sector = 'ICT'

    user.profile.technical_expertise = 'Digital fabrication - Digitalization of analog and traditional technologies'
    user.profile.size = 'A small enterprise (<50 staff)'

    user.profile.socialLinks = json.dumps([
        {"link": "top_ix", "name": "twitter"},
        {"link": "www.google.it", "name": "google-plus"},
        {"link": "https://www.facebook.com/topixconsortium/", "name": "facebook"}
    ])
    user.save()
    user.profile.save()
    return user


def profile_form_update_data():
    user_dict = {
        "sector": "Professional, scientific and technical activities aaa",
        "city": "Toronto, Ontario, Canada",
        "first_name": "Massimo",
        "last_name": "Santoli",
        "role_other": "Im a full stack developer in Top-ix",
        "tags": "Innovation,Software,Open", "gender": "male",
        "technical_expertise_other": "Im a talented full stack developer.",
        "technical_expertise": "Other",
        "birthdate": "1983/05/14",
        "socialLinks": "["
                       "{\"link\":\"https://twitter.com/top_ix\",\"name\":\"twitter\"},"
                       "{\"link\":\"www.google.it\",\"name\":\"google-plus\"},"
                       "{\"link\":\"https://www.facebook.com/topixconsortium/\",\"name\":\"facebook\"},"
                       "{\"name\":\"youtube\",\"link\":\"https://www.youtube.com/channel/UC2e2-e70sYMTxx1jXHdiSeg\"},"
                       "{\"name\":\"github\",\"link\":\"https://github.com/topix-hackademy\"}"
                       "]",
        "source_of_inspiration": "Science ,Culture ,Technology",
        "types_of_innovation": "Process innovation,Business model innovation and   other, development innnovation   ,Social innovation",
        "place": "{"
                 "\"city\":\"Toronto\","
                 "\"state\":\"ON\","
                 "\"country_short\":\"CA\","
                 "\"country\":\"Canada\","
                 "\"lat\":43.653226,"
                 "\"long\":-79.38318429999998"
                 "}",
        "statement": "Hi im a full stack developer!",
        "organization": "Top-ix",
        "role": "Employee",
        "csrfmiddlewaretoken": "ZPRuCqwHshEcBf6kcZ0rjUxrJnWvmbWGVIcV3wSjcC2r7uGSvkejXoZV7rkSD5T7",
        "size": "A small enterprise (<50 staff but cool)",
        "sector_other": "Developer sector",
        "occupation": "Developer"
    }
    return user_dict
