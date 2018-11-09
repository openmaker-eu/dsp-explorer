
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
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from utils.mailer import EmailHelper
from django.urls import reverse
from datetime import datetime, timedelta
from django.db.models import Q
from .helpers import order_date_index

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
        # results = Insight.entity_detail(entity, entity_id)
        print('results')
        print(results)
    except DSPConnectorException as e:
        print('ERROR[dashboard.api14.bookmark]: DSPConnectorException')
        print(e)
    except AttributeError as a:
        print('NOT FOUND[dashboard.api14.bookmark]: DSPConnectorException')
        print(a)
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
        print('ERROR[dashboard.api14.bookmark]')
        print(e)
        return Response({}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_bookmarks(request):
    try:
        profile = request.user.profile
        results = profile.get_bookmarks()
        serialized = BookmarkSerializer(results, many=True).data
        return Response(serialized)
    except Exception as e:
        print('NOT FOUND[dashboard.api14.get_bookmarks]')
        return Response({}, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_bookmark_by_entities(request, entity=None):
    try:
        profile = request.user.profile
        results = profile.get_bookmarks(entity)
        serialized = BookmarkSerializer(results, many=True).data
        return Response(serialized)
    except Exception as e:
        print('NOT FOUND[dashboard.api14.get_bookmark_by_entities]')
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
    from dashboard.models import EntityProxy
    profile = request.user.profile if \
        request.user.is_authenticated and \
        not user_id else \
        Profile.objects.filter(pk=user_id).first()

    if not profile:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    try:
        singular_entity = EntityProxy.singular_name(entity) if entity in ['projects', 'challenges'] else entity
        model_serializer = InterestSerializer if entity in ['news', 'events'] \
            else ModelHelper.get_serializer(singular_entity.capitalize())
        interests = profile.get_interests(entity)
        res = model_serializer(interests, many=True).data
        return Response(res)
    except Exception as e:
        print('ERROR[dashboard.api14.interest]')
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
    profile = request.user.profile if request.user.is_authenticated else None
    local_entity = ModelHelper.find_this_entity(entity, entity_id)
    if profile is None:
        return Response(False)
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
        res = ProfileSerializer(local_entity.interested(), many=True).data
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


@api_view(['GET'])
def chatbot_interests(request):
    if not request.user.is_authenticated:
        return Response(data={}, status=204)
    try:
        profile = request.user.profile
        context = {
            'news': len(profile.get_interests('news')),
            'events': len(profile.get_interests('events')),
            'projects': len(profile.get_interests('projects')) + len(profile.get_interests('challenges')),
        }
        return Response(data=context)
    except Exception as e:
        print('ERROR[dashboard.api14.chatbot_interests]: Error retrieving chatbot bookmark ')
        print(e)
        return Response(data={}, status=401)


class entity(APIView):
    def get(self, request, entity, user_id=None):
        """

        :param request:
        :param entity:
        :param user_id:
        :param page:
        :return:
        """
        #TODO make cursor works
        page = int(request.GET.get('page', 1))
        is_last_page = False
        profile = request.user.profile if request.user.is_authenticated else None


        # Local entities
        if entity == 'loved':
            return interest(request._request, entity='profile', user_id=user_id)
        elif entity == 'lovers':
            return interested(request._request, entity='profile', entity_id=user_id)
        elif entity == 'projects' or entity == 'challenges':
            projects = Project.objects.order_by('-end_date') if profile \
                else Project.objects.order_by('-end_date')[:5]
            challenges = Challenge.objects.order_by('-end_date') if profile \
                else Challenge.objects.order_by('-end_date')[:5]
            # Mix Results
            results = ChallengeSerializer(challenges, many=True).data + ProjectSerializer(projects, many=True).data
            results = sorted(results, key=order_date_index, reverse=False)
        elif entity == 'matches':
            matches = Profile.objects.get(pk=user_id).best_matches()
            results = ProfileSerializer(matches, many=True).data
        else:
            # Remote Entities
            try:
                response = self.reccomended_content(request, entity, page) if profile \
                    else self.reccomended_content(request, entity, page)
                is_last_page = 'next_page' in response and response['next_page'] == 0
                results = response[entity]
            except DSPConnectorException as e:
                print('ERROR[dashboard.api14.entity.get] DSPConnectorException')
                logger.error(e)
            except AttributeError as a:
                print('ERROR[dashboard.api14.entity.get] AttributeError')
                logger.error(a)

        return Response(data=results or [], status=202 if is_last_page else 200)

    def topic_ids(self):
        topics_list = DSPConnectorV13.get_topics()['topics']
        return [x['topic_id'] for x in topics_list]

    def reccomended_content(self, request, entity, page):
        return Insight.reccomended_entity(
            crm_id=request.user.profile.crm_id if request.user.is_authenticated else None,
            entity_name=entity,
            page=page
        )

    def generic_content(self):
        pass

    def random_content_visitor(self, topics_id_list, method_to_call, entity):
        selected_topic = random.choice(topics_id_list)
        results = getattr(DSPConnectorV13, method_to_call)(topic_id=selected_topic, cursor=-1)
        return results[entity] if entity in results else []


class entity_details(APIView):
    def get(self, request, entity, entity_id):
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
                # results = getattr(DSPConnectorV13, method_to_call)(entity_id=entity_id)[entity][0]
                results = Insight.entity_details(entity, entity_id)
            except DSPConnectorException:
                pass
            except AttributeError as a:
                pass

        return Response(results)

    def delete(self, request, entity, entity_id):

        authorized = request.user.is_authenticated \
            and entity == 'projects' \
            and int(entity_id) in [x.id for x in Project.objects.filter(profile=request.user.profile)]

        if not authorized:
            return Response(status=401)

        try:
            project = Project.objects.filter(id=entity_id).first()
            project.delete()
        except Exception as e:
            print('[ERROR: dashboard.api14.entity_details.delete]')
            print(e)
        return Response()


@api_view(['POST'])
def signup(request):

    data = {key: value for (key, value) in request.data.items()}

    email = data.get('email', False)
    password = data.get('password', False)
    password_confirm = data.get('password_confirm', False)

    if len(User.objects.filter(email=email)) > 0:
        return Response(data={'error': 'User already exists'}, status=401)

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
            'FIRST_NAME': user.first_name,
            'LAST_NAME': user.last_name,
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
                print('ERROR[dashboard.api14.apilogin]: error twitter auth')
                print(e)
    else:
        user = User.objects.filter(email=request.data.get('username', False)).first()
        message = 'Your user is not yet active!<br>' \
                  'Please complete the activation process by clicking on the link in the email you received after signing up <br>' \
                  'or click on <a href="' + reverse('dashboard:resend_activation_email') + '">Resend activation email</a>' \
            if user and not user.is_active \
            else 'Username or password are wrong'

        return Response(data={'error': message}, status=401)

    # Try to fill crm_id if not present
    if not user.profile.crm_id:
        try:
            crm_user = CRMConnector.search_party_by_email(user.profile.user.email)
        except Exception as e:
            print('ERROR[dashboard.api14.apilogin]: crm_user not found')
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


@api_view(['POST'])
def apiunsubscribe(request):
    try:
        first_name = request.user.first_name
        last_name = request.user.last_name
        Profile.delete_account(request.user.pk)

        EmailHelper.email(
            template_name='account_deletion_confirmation',
            title='Openmaker Explorer account deletion',
            vars={
                'FIRST_NAME': first_name,
                'LAST_NAME': last_name,
            },
            receiver_email=request.user.email
        )
        logout(request)

    except Exception as e:
        print('ERROR[dashboard.api14.apiunsubscribe]')
        print(e)
        return Response({'error': e}, status=500)

    return Response()


@login_required
def users_csv(request):
    from django.http import HttpResponse
    import csv

    if not request.user.is_superuser:
        return HttpResponse(status=401)

    response = HttpResponse(csv, content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename="OM_users.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="OM_users.csv"'
    writer = csv.writer(response, delimiter=';', lineterminator='\n', quoting=csv.QUOTE_ALL, dialect='excel')

    writer.writerow([
        'user:email',
        'user:first_name',
        'user:last_name',
        'user:birthdate',
        'user:gender',
        'user:occupation',
        'location:city',
        'location:state',
        'location:country',
        'location:country_short',
        'location:post_code',
        'location:lat',
        'location:long',
        'activity:domain',
        'activity:area',
        'activity:technology',
        'activity:skills',
        'tags:old',
        'twitter:name'
    ])

    profiles = Profile.objects.all()
    for profile in profiles:
        try:
            location = {}
            try:
                location = json.loads(profile.place)
            except Exception as e:
                pass

            activities = {'domain': '', 'area': '', 'technology': '', 'skills': ''}
            for k, activity in activities.items():
                activitiesQuerySet = profile.tags.filter(type=k)
                activities[k] = ','.join([
                    x.name for x in activitiesQuerySet
                    if len(activitiesQuerySet) > 0
                    and x.name not in ['', False, None]
                ])

            tagsQuerySet = profile.tags.filter(type='')
            tags = ','.join([
                x.name for x in tagsQuerySet
                if len(tagsQuerySet) > 0
                and x.name not in ['', False, None]
            ])

            twitter = hasattr(profile, 'twitterauth') and profile.twitterauth or profile.twitter_username

            writer.writerow([
                profile.user.email,
                profile.user.first_name,
                profile.user.last_name,
                profile.birthdate,
                profile.gender,
                profile.occupation,

                location.get('city', ' '),
                location.get('state', ' '),
                location.get('country', ' '),
                location.get('country_short', ' '),
                location.get('post_code', ' '),
                location.get('lat', ' '),
                location.get('long', ' '),

                activities.get('domain', ' '),
                activities.get('area', ' '),
                activities.get('technology', ' '),
                activities.get('skills', ' '),

                tags,
                twitter
            ])

        except User.DoesNotExist:
            print('there are profiles without user')

    return response


# GENDER DISTRIBUTION 
@api_view(['GET'])
def gender_distribution(request):
    users_total=Profile.objects.all().count()
    male_percentage=Profile.objects.filter(Q(gender='male', user__isnull=False)).count()*100/users_total
    female_percentage=Profile.objects.filter(Q(gender='female', user__isnull=False)).count()*100/users_total
    nonspecifiedgender_percentage=Profile.objects.filter( Q(gender='other', user__isnull=False)).count()*100/users_total
    geneder_percentage= {
        "male":"%.2f"%male_percentage,
        "female":"%.2f"%female_percentage,
        "other":"%.2f"%nonspecifiedgender_percentage
    }
    print()
    return Response(geneder_percentage)


# AGE DISTRIBUTION
@api_view(['GET'])
def age_distribution(request):
    from datetime import datetime, date
    birthdates=Profile.objects.filter(Q(user__isnull=False)).values("birthdate")
    list=[]
    zero_to_thirty=[]
    thirty_to_forty=[]
    forty_to_fifty=[]
    over_fifty=[]
    today=datetime.today()
    for birthdate in birthdates:
        single_birthdate=birthdate.get('birthdate').replace(tzinfo=None)
        delta=today - single_birthdate
        age=delta.days/365
        list.append(age)
    for age in list:
        if age > 0 and age <= 30:
            zero_to_thirty.append(age)
    for age in list:
        if age >30 and age <= 40:
            thirty_to_forty.append(age)
    for age in list:
        if age > 40 and age <= 50:
            forty_to_fifty.append(age)
    for age in list:
        if age > 50 :
            over_fifty.append(age)
   
    age_intervals={
        "zero_to_thirty": len(zero_to_thirty),
        "thirty_to_forty": len(thirty_to_forty),
        "forty_to_fifty": len(forty_to_fifty),
        "over_fifty": len(over_fifty)
    }
    return Response(
           age_intervals
        )

# JOB DISTRIBUTION
@api_view(['GET'])

def job_distribution(request):
    from django.db.models import Count
    jobs= Profile.objects.filter(Q(user__isnull=False)).values("occupation").annotate(people=Count('occupation')).order_by('-people').filter()[:10]
    print(jobs)
    return Response(jobs)

#CITY DISTRIBUTION
@api_view(['GET'])

def city_distribution(request):
    from json import JSONDecodeError
    from django.db.models import Count, F
    import json
    users_total=Profile.objects.all().count()
    cities=Profile.objects.filter(Q(user__isnull=False)).values("place")
    latlong=Profile.objects.filter(Q(user__isnull=False)).values("latlong").annotate(people=Count('latlong')).annotate(city=F('city')).order_by('-people').filter()[:10]
    places=[]
    print(type(cities[0]['place']))
    print(json.loads(cities[0]['place']))
    for k,city in enumerate(cities):
        try:
            place=json.loads(city['place'])
            places.append(place)
        except JSONDecodeError as e:
            x=city['place'].replace("'","\"")
            place=json.loads(x)
            places.append(place)
        except TypeError as e:
            print('è vuoto', k)
    
        # lat=latlong[0].get('latlong').split(',')
        # lati=lat[0]

    print(place)
    print(type)
    return Response(latlong)


@login_required()
@api_view(['POST'])
def contact_user_with_email(request, user_id):
    from django.utils.html import escape, strip_tags

    if request.user.profile.id == user_id:
        return Response({'error': 'you cannot send message to yourself'}, status=422)

    email_message = strip_tags(escape(request.data.get('message', None)))

    sender = request.user
    receiver = User.objects.filter(pk=user_id).first()

    vars = {
        'SENDER_FIRST_NAME': sender.first_name,
        'SENDER_LAST_NAME': sender.last_name,
        'SENDER_PROFILE_PAGE': 'http://explorer.openmaker.eu/profile/'+str(sender.profile.id),
        'RECEIVER_FIRST_NAME': receiver.first_name,
        'RECEIVER_LAST_NAME': receiver.last_name,
        'MESSAGE': email_message
    }

    email_title = 'OpenMaker - message from : ' + (sender.first_name + ' ' + sender.last_name).title()
    EmailHelper.email('user_to_user', receiver.email, email_title, vars)

    return Response('Message sent')

