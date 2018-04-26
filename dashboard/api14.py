
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

from .helpers import mix_result_round_robin
from dashboard.models import Challenge, Project

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.serializers import serialize
from dspexplorer.site_helpers import User as AuthUser


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


def bookmark(request, entity='news', entity_id=None):
    # GET return status of a bookmark (ES: {bookmarked:true|false})
    # POST toggle status of a bookmark an return it (ES: {bookmarked:true|false})
    results = {}
    try:
        local_entity = None
        profile = request.user.profile
        try:
            local_entity = ModelHelper.find_this_entity(entity, entity_id)
        except ObjectDoesNotExist as odne:
            return not_found()
        if request.method == 'POST':
            results['bookmarked'] = profile.bookmark_this(local_entity)
        else:
            results['bookmarked'] = profile.is_this_bookmarked_by_me(local_entity)
        return success('ok','bookmark',results)
    except AttributeError as a:
        return not_authorized()
    except Exception as e:
        print e
        return not_authorized()


def get_bookmarks(request):
    try:
        profile = request.user.profile
        results = profile.get_bookmarks()
        serialized = BookmarkSerializer(results, many=True).data
        return JsonResponse({
            'status': 'ok',
            'result': serialized,
        }, status=200)
    except Exception as e:
        print e
        return not_authorized()


def get_bookmark_by_entities(request, entity=None):
    try:

        entity = entity[:-1]
        profile = request.user.profile
        results = profile.get_bookmarks(entity)
        serialized = BookmarkSerializer(results, many=True).data

        return JsonResponse({
            'status': 'ok',
            'result': serialized,
        }, status=200)
    except Exception as e:
        print e
        return not_authorized()


def interest(request, entity='news', entity_id=None):
    '''
    :param request:
    :param entity:
    :param entity_id:
    :return:
        GET mode
            If request's user exists, the api will return all user interested in the entity specified
            If request is from an anonymous users, just the number of interested people is will be returned
        POST mode(only for logged)
            Toggle the interest for the specified entity for the logged user
    '''
    results = {}
    local_entity = None
    try:
        #logged user
        profile = request.user.profile
        try:
            local_entity = ModelHelper.find_this_entity(entity, entity_id)
        except ObjectDoesNotExist as odne:
            return not_found()
        if request.method == 'GET':
            results['iaminterested'] = profile.is_this_interested_by_me(local_entity)
            results['interested'] = ProfileSerializer(local_entity.interested(),many=True).data
            results['interested_counter'] = len(local_entity.interested())

        else:
            # Toggle interest
            results['iaminterested'] = profile.interest_this(local_entity)
            results['interested'] = ProfileSerializer(local_entity.interested(), many=True).data
            results['interested_counter'] = len(local_entity.interested())
        return JsonResponse({
            'status': 'ok',
            'result': results,
        }, status=200)
    except Exception as e:
        #Anonymous user
        if request.method == 'GET':
            local_entity = ModelHelper.find_this_entity(entity, entity_id)
            results['interested_counter'] = len(local_entity.interested())
            return JsonResponse({
                'status': 'ok',
                'result': results,
            }, status=202)
        else:
            return not_authorized()


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


def user_authorization(request):
    from dspexplorer.site_helpers import User
    return JsonResponse({
        'status': 'ok',
        'result': User.authorization(request) ,
    }, status=200)

@api_view(['POST'])
def apilogin(request):
    from django.contrib.auth import authenticate, login, logout
    data = json.loads(request.body)
    user = authenticate(
        username=data.get('username', False),
        password=data.get('password', False)
    )
    if user is not None:
        login(request, user)
    else:
        raise Http404('Username or password are wrong')

    return Response({'authorization': AuthUser.authorization(request)})

@api_view(['POST'])
def apilogout(request):
    from django.contrib.auth import logout
    logout(request)
    return Response({'authorization': 0})


@api_view(['GET'])
def questions(request):
    questions = (
        {'id': '2', 'type': 'text', 'label':' What is your first name', 'data': ''},
        {'id': '2', 'type': 'text', 'label': 'What is your last name', 'data': ''},
        {'id': '1', 'type': 'ddl', 'label':' What is your gender', 'data':
            ({'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}, {'value': 'other', 'label': 'Does it matter?'})
         },
        {'id': '3', 'type': 'slider', 'label': 'How much do you like openmaker?', 'data': 90},
        {'id': '4', 'type': 'login', 'label': 'Your login information'}
    )
    return Response({'questions': questions})



class entity(APIView):
    def get(self, request, entity):
        #TODO make cursor works
        profile = None
        results = []
        local_entities = None
        try:
            profile = request.user.profile
        except:
            profile = None
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
            local_entities = Project.objects.all()
            if not profile:
                local_entities = local_entities[:5]
            results.extend(ProjectSerializer(local_entities, many=True).data)
            local_entities = Challenge.objects.all()
            if not profile:
                local_entities = local_entities[:5]
            results.extend(ChallengeSerializer(local_entities, many=True).data)

        return Response(results[:20])


class entity_details(APIView):
    def get(self, request, entity='news', entity_id=None):
        results = []
        if entity == 'projects':
            local_entities = Project.objects.get(pk=entity_id)
            results = ProjectSerializer(local_entities).data
        elif entity == 'challenges':
            local_entities = Challenge.objects.get(pk=entity_id)
            results = ChallengeSerializer(local_entities).data
        else:
            try:
                method_to_call = 'get_' + entity+'_detail'
                results = getattr(DSPConnectorV13, method_to_call)(entity_id=entity_id)[entity][0]
            except DSPConnectorException:
                pass
            except AttributeError as a:
                pass

        return Response(results)
