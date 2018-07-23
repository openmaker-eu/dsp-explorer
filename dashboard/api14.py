
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
from connectors.insight.connector import InsightConnectorV10 as Insight

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
        elif entity == 'lovers':
            return interested(request._request, entity='profile', entity_id=user_id)
        elif entity == 'projects' or entity == 'challenges':
            local_entities = Project.objects.order_by('-end_date')
            if not profile:
                local_entities = local_entities[:5]
            results = results+ProjectSerializer(local_entities, many=True).data
            local_entities = Challenge.objects.order_by('-end_date')
            if not profile:
                local_entities = local_entities[:5]
            results = results+ChallengeSerializer(local_entities, many=True).data
            results = sorted(results, key=lambda k: k['end_date'] or '', reverse=False)
        elif entity == 'matches':
            local_entities = Profile.objects.get(pk=user_id).best_matches()
            results = ProfileSerializer(local_entities, many=True).data
        else:
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
                    reccomended = Insight.reccomended_entity(crm_id=request.user.profile.crm_id, entity_name=entity)
                    for index, topic_id in enumerate(topics_id_list):
                        results.append(getattr(DSPConnectorV13, method_to_call)(topic_id=topic_id)[entity])
                    results = reccomended + mix_result_round_robin(*results)
            except DSPConnectorException:
                pass
            except AttributeError as a:
                pass

        return Response(results[:20] if len(results) > 20 else results)


class entity_details(APIView):
    def get(self, request, entity, entity_id):
        print(entity)
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

@api_view(['POST'])
def signup(request):
    from utils.mailer import EmailHelper

    data = {key: value for (key, value) in request.data.items()}

    email = data.get('email', False)
    password = data.get('password', False)
    password_confirm = data.get('password_confirm', False)

    if len(User.objects.filter(email=email)) > 0:
        return Response(data={'error': 'User already exist'}, status=401)

    if not password or password != password_confirm:
        return Response(data={'error': 'Password and password confirm don\'t match'}, status=401)

    user = User.create(**data)
    profile = Profile.create(user=user, **data)

    # Send email
    confirmation_link = request.build_absolute_uri('/onboarding/confirmation/{TOKEN}'.format(TOKEN=profile.reset_token))

    EmailHelper.email(
        template_name='onboarding_email_template',
        title='OpenMaker - Confirm your email',
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
    from crmconnector.models import CRMConnector
    from oauth.models import TwitterProfile

    user = authenticate(
        username=request.data.get('username', False),
        password=request.data.get('password', False)
    )
    twitter_auth = request.COOKIES.get('twitter_oauth', None)
    delete_twitter_coookie = False

    # Check authentication status
    if user is not None:
        login(request, user)
        if twitter_auth:
            try:
                twitter_profile = TwitterProfile.objects.filter(pk=twitter_auth).first()
                twitter_profile.profile_id = user.profile.id
                twitter_profile.save()
                delete_twitter_coookie = True
            except Exception as e:
                print('error twitter auth')
                print(e)
    else:
        return Response(data={'error': 'Username or password are wrong'}, status=401)

    # Try to fill crm_id if not present
    if not user.profile.crm_id:
        try:
            crm_user = CRMConnector.search_party_by_email(user.profile.user.email)
        except Exception as e:
            print(e)

    # Build Response
    response = Response({
        'authorization': AuthUser.authorization(request),
        'has_questions': AuthUser.authorization(request) > 0 and True,
        'user': UserSerializer(user, many=False).data if request.user.is_authenticated else None
    })
    delete_twitter_coookie and True
    response.delete_cookie('twitter_oauth')
    return response

@api_view(['POST'])
def apilogout(request):
    from django.contrib.auth import logout
    logout(request)
    return Response({'authorization': 0})
