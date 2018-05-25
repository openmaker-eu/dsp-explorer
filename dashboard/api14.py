
from django.http import JsonResponse

from django.core.exceptions import ObjectDoesNotExist
from .models import ModelHelper

from .serializer import ProfileSerializer, ProjectSerializer, ChallengeSerializer
from dspconnector.connector import DSPConnector, DSPConnectorException, DSPConnectorV12, DSPConnectorV13
from utils.api import not_authorized, not_found, error, bad_request, success

import json
import random, logging

logger = logging.getLogger(__name__)

from dashboard.serializer import BookmarkSerializer, InterestSerializer
from dashboard.models import User, Profile, Tag
import datetime
from .helpers import mix_result_round_robin
from dashboard.models import Challenge, Project

from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.serializers import serialize
from dspexplorer.site_helpers import User as AuthUser
from dashboard.serializer import UserSerializer, TagSerializer, ProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser

def __wrap_response(*args, **kwargs):
    try:
        results = args[0](args[1:])
    except DSPConnectorException:
        return JsonResponse({
            'status': 'error',
            'result': {}
        }, status=400)
    return JsonResponse({
        'status': 'ok',
        'result': results
    }, status=200)


def get_entity_details(request, entity='news', entity_id=None):
    results = []
    profile = None

    try:
        method_to_call = 'get_' + entity+'_detail'
        results = getattr(DSPConnectorV13, method_to_call)(entity_id=entity_id)[entity]
    except DSPConnectorException:
        pass
    except AttributeError as a:
        if entity == 'projects':
            local_entities = Project.objects.get(pk=entity_id)
            results = ProjectSerializer(local_entities).data
        else:
            local_entities = Challenge.objects.get(pk=entity_id)
            results = ChallengeSerializer(local_entities, many=True).data

    return success('ok', 'single entity', results)

@api_view(['GET', 'POST'])
def bookmark(request, entity='news', entity_id=None):
    # GET return status of a bookmark (ES: {bookmarked:true|false})
    # POST toggle status of a bookmark an return it (ES: {bookmarked:true|false})
    try:
        local_entity = None
        profile = request.user.profile
        try:
            local_entity = ModelHelper.find_this_entity(entity, entity_id)
        except ObjectDoesNotExist as odne:
            return Response({}, status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            return Response(profile.bookmark_this(local_entity))
        else:
            return Response(profile.is_this_bookmarked_by_me(local_entity))
    except Exception as e:
        return Response({}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_bookmarks(request):
    try:
        profile = request.user.profile
        results = profile.get_bookmarks()
        serialized = BookmarkSerializer(results, many=True).data
        return Response(serialized)
    except Exception as e:
        return Response({}, status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_bookmark_by_entities(request, entity=None):
    try:
        profile = request.user.profile
        results = profile.get_bookmarks(entity)
        serialized = BookmarkSerializer(results, many=True).data
        return Response(serialized)
    except Exception as e:
        return Response({}, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def interest(request, entity, user_id=None):
    """
    :param request:
    :param entity:
    :param user_id:
    :return:
        GET:
            return all the interest shown by specified user that belongs to specific entitiy type
            if no user id specified will use the logged user
    """
    profile = request.user.profile if \
        request.user.is_authenticated and \
        not user_id else \
        Profile.objects.filter(pk=user_id).first()

    if not profile:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    try:
        model_class = ModelHelper.get_by_name(entity.capitalize())
        model_serializer = ModelHelper.get_serializer(entity.capitalize())
        interest = profile.interests(model_class)
        res = model_serializer(interest, many=True).data
        return Response(res)
    except Exception as e:
        print('Error')
        print(e)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def my_interest(request, entity, entity_id):
    """

    :param request:
    :param entity:
    :param entity_id:
    :return:
            GET : if logged user is interested
            POST : toggle interest and return if logged user is interested
    """
    profile = request.user.profile
    local_entity = ModelHelper.find_this_entity(entity, entity_id)
    if request.method == 'GET':
        return Response(profile.is_this_interested_by_me(local_entity))
    else:
        return Response(profile.interest_this(local_entity))


@api_view(['GET'])
def user_projects(request, profile_id):
    """

    :param request:
    :param profile_id:
    :return:
            List of project created by specific user
            if profile_id is not provided logged user will be used
    """
    profile = Profile.objects.filter(pk=profile_id).first() if profile_id else request.user.profile
    projects = Project.objects.filter(profile=profile)
    serialized = ProjectSerializer(projects, many=True).data
    return Response(serialized)


@api_view(['GET'])
def interested(request, entity='news', entity_id=None):
    """

    :param request:
    :param entity:
    :param entity_id:
    :return:
        If request's user exists, the api will return all user interested in the entity specified
        If request is from an anonymous users, just the number of interested people is will be returned
    """
    try:
        local_entity = ModelHelper.find_this_entity(entity, entity_id)
        res = ProfileSerializer(local_entity.interested(), many=True).data if request.user.is_authenticated \
            else len(local_entity.interested())
        return Response(res)
    except Exception as e:
        return Response({}, status=status.HTTP_404_NOT_FOUND)


def get_interests(request):
    try:
        profile = request.user.profile
        results = profile.get_interests()
        serialized = InterestSerializer(results, many=True).data
        return JsonResponse({
            'status': 'ok',
            'result': serialized,
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'ko',
            'result': 'Unhautorized',
        }, status=403)


class entity(APIView):
    def get(self, request, entity, user_id=None):
        """

        :param request:
        :param entity:
        :param user_id:
        :return:
        """

        #TODO make cursor works
        profile = None
        results = []
        local_entities = None
        try:
            profile = request.user.profile
        except:
            profile = None

        # Local entities
        if entity == 'loved':
            return interest(request._request, entity='profile', user_id=user_id)
        if entity == 'lovers':
            return interested(request._request, entity='profile', entity_id=user_id)
        if entity == 'projects':
            local_entities = Project.objects.all()
            if not profile:
                local_entities = local_entities[:5]
            results.extend(ProjectSerializer(local_entities, many=True).data)
            local_entities = Challenge.objects.all()
            if not profile:
                local_entities = local_entities[:5]
            results.extend(ChallengeSerializer(local_entities, many=True).data)

        # Remote Entities
        try:
            topics_list = DSPConnectorV12.get_topics()['topics']
            topics_id_list = [x['topic_id'] for x in topics_list]
            method_to_call = 'get_' + entity

            if not profile:
                selected_topic = random.choice(topics_id_list)
                results = getattr(DSPConnectorV13, method_to_call)(topic_id=selected_topic)[entity]
                results = results[:5]
            else:
                for index,topic_id in enumerate(topics_id_list):
                    results.append(getattr(DSPConnectorV13, method_to_call)(topic_id=topic_id)[entity])
                results = mix_result_round_robin(*results)
        except DSPConnectorException:
            pass
        except AttributeError as a:
            pass

        return Response(results[:20] if len(results) > 20 else results)


class entity_details(APIView):
    def get(self, request, entity='news', entity_id=None):
        results = []
        if entity == 'projects':
            local_entities = Project.objects.get(pk=entity_id)
            results = ProjectSerializer(local_entities).data
        elif entity == 'challenges':
            local_entities = Challenge.objects.get(pk=entity_id)
            results = ChallengeSerializer(local_entities).data
        elif entity == 'profile':
            local_entities = Profile.objects.get(pk=entity_id)
            results = ProfileSerializer(local_entities).data
        else:
            try:
                method_to_call = 'get_' + entity+'_detail'
                results = getattr(DSPConnectorV13, method_to_call)(entity_id=entity_id)[entity][0]
            except DSPConnectorException:
                pass
            except AttributeError as a:
                pass

        return Response(results)


class questions(APIView):

    parser_classes = (MultiPartParser,)
    questions = []

    def get(self, request):
        # Request for signup questions
        if not request.user.is_authenticated:
            self.questions = [
                self.make('register', 'message', 'Signup', value='Signup to Openmaker Explorer'),
                self.make('name', 'name', 'Who are you?'),
                self.make('gender', 'select', 'What is your gender?',
                    options=({'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}, {'value': 'other', 'label': 'Does it matter?'})
                ),
                self.make('birthdate', 'date', 'What is your birthdate?', max=str((datetime.datetime.now()-datetime.timedelta(days=16*365)).strftime('%Y/%m/%d'))),
                self.make('city', 'city', 'What is your city?'),
                self.make('occupation', 'text', 'What is your occupation?'),
                self.make('activity-question', 'activity-question', 'What is your activity?'),
                self.make('tags', 'multi_select', 'Choose 3 tags', options=[x.name for x in Tag.objects.all()]),
                self.make('signup', 'signup', 'Your login information', apicall='/api/v1.4/signup/'),
                self.make('sugnup_end', 'success', 'Thank you', value='Check your inbox for a confirmation email'),
            ]

        # Request for a specific set of questions
        if request.user.is_authenticated and len(request.query_params) > 0:
            action = request.query_params.get('action', None)

            # Request for the edit profile questions
            action == 'edit-profile' and self.edit_profile(request)

        return Response({'questions': self.questions})

    def edit_profile(self, request):

        user = request.user
        profile = request.user.profile
        questions = [
            self.make('name', 'name', 'What is your name?', value=[user.first_name, user.last_name]),
            self.make('gender', 'select', 'What is your gender?',
                options=({'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}, {'value': 'other', 'label': 'Does it matter?'})
            ),
            self.make('occupation', 'text', 'What is your occupation?'),
            self.make('birthdate', 'date', 'What is your birthdate?',
                max=str((datetime.datetime.now()-datetime.timedelta(days=16*365)).strftime('%Y/%m/%d')),
                value=profile.birthdate.strftime('%Y/%m/%d'),
            ),
            self.make('city', 'city', 'What is your city?', value={'city': profile.city, 'place': {}}),
            self.make('tags', 'multi_select', 'Choose 3 tags',
                options=[x.name for x in Tag.objects.all()],
                value=[x.name for x in profile.tags.all()],
            ),
            self.make('activity-question', 'activity-question', 'What is your activity?',
                value={
                    "domain": profile.domain.split(","),
                    "area": profile.area.split(","),
                    "technology": profile.technology.split(","),
                    "skills": profile.skills.split(",")
                }
            ),
            self.make('statement', 'textarea', 'Short description about you (optional)'),
            self.make('picture', 'imageupload', 'Upload you profile image (optional)',
                      value=profile.picture.url if profile.picture else None,
                      apicall='/api/v1.4/questions/',
                      emitevent='entity.change.all'
            ),
        ]

        # Add Values
        for question in questions:
            question['value'] = question.get('value', None) \
                                or getattr(profile, question['name'], None) \
                                or getattr(user, question['name'], None)

        self.questions = questions + [self.make('edit_end', 'success', 'Profile updated'), ]

    def make(self, name, type, label='', **kwargs):
        question = {'name': name, 'type': type, 'label': label}
        for key, arg in kwargs.items():
            question[key] = arg
        return question

    def post(self, request):
        user = request.user
        profile = request.user.profile

        print('ACTIVITY: ')
        print(request.data)
        try:
            # User
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)

            # Profile
            profile.city = request.data.get('city', profile.city)
            profile.place = json.loads(request.data.get('place', profile.place))
            profile.birthdate = request.data.get('birthdate', profile.birthdate)
            profile.occupation = request.data.get('occupation', profile.occupation)
            profile.statement = request.data.get('statement', profile.statement)

            # Activity
            profile.domain = request.data.get('domain', profile.domain)
            profile.area = request.data.get('area', profile.area)
            profile.technology = request.data.get('technology', profile.technology)
            profile.skills = request.data.get('skills', profile.skills)

            # Profile Extra
            profile.tags_create_or_update(request.data.get('tags', None), clear=True)
            profile.picture_set_or_update(request.data.get('picture', None))

        except Exception as error:
            return Response(data={'error': error}, status=403)

        user.save()
        profile.save()

        return Response()


@api_view(['POST'])
def signup(request):
    from utils.mailer import EmailHelper

    email = request.data.get('email', False)
    password = request.data.get('password', False)
    password_confirm = request.data.get('password_confirm', False)

    if len(User.objects.filter(email=email)) > 0:
        return Response(data={'error': 'User already exist'}, status=401)

    if not password or password != password_confirm:
        return Response(data={'error': 'Password and password confirm don\'t match'}, status=401)

    user = User.create(**request.data)
    profile = Profile.create(user=user, **request.data)

    # Send email
    confirmation_link = request.build_absolute_uri('/onboarding/confirmation/{TOKEN}'.format(TOKEN=profile.reset_token))

    EmailHelper.email(
        template_name='onboarding_email_template',
        title='OpenMaker Nomination done!',
        vars={
            'FIRST_NAME': user.first_name.encode('utf-8'),
            'LAST_NAME': user.last_name.encode('utf-8'),
            'CONFIRMATION_LINK': confirmation_link,
        },
        receiver_email=user.email
    )

    return Response({'success': True}) if profile else Response(data={'error': 'error creating user'}, status=403)


@api_view(['GET'])
def authorization(request):
    return Response({
        'authorization': AuthUser.authorization(request),
        'user': UserSerializer(request.user, many=False).data if request.user.is_authenticated else None
    })

@api_view(['POST'])
def apilogin(request):
    user = authenticate(
        username=request.data.get('username', False),
        password=request.data.get('password', False)
    )
    if user is not None:
        login(request, user)
    else:
        return Response(data={'error': 'Username or password are wrong'}, status=401)

    return Response({
        'authorization': AuthUser.authorization(request),
        'user': UserSerializer(user, many=False).data if request.user.is_authenticated else None
    })


@api_view(['POST'])
def apilogout(request):
    from django.contrib.auth import logout
    logout(request)
    return Response({'authorization': 0})