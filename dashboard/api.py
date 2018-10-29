from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile, Invitation, User, ProjectContributor, Bookmark, ModelHelper

from utils.mailer import EmailHelper
from .serializer import ProfileSerializer, ProjectSerializer, ChallengeSerializer
from dspconnector.connector import DSPConnector, DSPConnectorException, DSPConnectorV12, DSPConnectorV13
from utils.api import not_authorized, not_found, error, bad_request, success
import json
from datetime import date, timedelta
import random, logging, requests
from crmconnector.models import Party
from django.core.paginator import Paginator
from utils.Colorizer import Colorizer
logger = logging.getLogger(__name__)

from dashboard.serializer import BookmarkSerializer, InterestSerializer

from .helpers import mix_result_round_robin
from django.http import HttpResponse
from django.apps import apps
import math
from dashboard.exceptions import EmailAlreadyUsed, UserAlreadyInvited, SelfInvitation
from dashboard.models import Challenge, Project, Tag, EntityProxy
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt

from django.urls import reverse
import os, re
from django.http import Http404


def search_members(request, search_string=None, extra_params=None):

    # Can be 3, 2 or 1 column in the frontend
    members_per_page = 24

    search_string = request.POST.get('search_query', '') if not search_string else search_string

    # A QuerySet wit all the active users as results if no search string is provided else return the filtered QuerySet
    results = Profile.search_members(search_string, request.GET.get('restrict_to', None))
    count = results.count()

    # Pagination
    page = request.GET.get('page', 1)
    max_page = int(math.ceil(float(count)/float(members_per_page))) or 1
    paginator = Paginator(results, members_per_page)
    paginated_results = paginator.page(page)

    # Serialize
    serializer = ProfileSerializer(instance=paginated_results, many=True)

    # Response
    return JsonResponse({
        'status': 'ok',
        'search_string': search_string,
        'result': serializer.data,
        'page': page,
        'max_page': max_page,
        'results_count': count
    }, status=200)


def get_last_members(request):
    last_twenty = Profile.get_last_n_members(21)
    serializer = ProfileSerializer(instance=last_twenty, many=True)
    return JsonResponse({
        'status': 'ok',
        'result': serializer.data
    }, status=200)


def get_feeds(request, theme_name, date='yesterday', cursor=-1):
    try:
        feeds = DSPConnector.get_feeds(theme_name, date, cursor)
    except DSPConnectorException:
        feeds = {}
    return JsonResponse(
        {
            'status': 'ok',
            'result': feeds
        }, status=200)


def get_themes(request):
    try:
        themes = DSPConnector.get_themes()
    except DSPConnectorException:
        themes = {}
    return JsonResponse({'status': 'ok',
                         'result': themes}, status=200)


def get_influencers(request, theme_name):
    try:
        influencers = DSPConnector.get_influencers(theme_name)
    except DSPConnectorException:
        influencers = {}
    return JsonResponse({'status': 'ok',
                         'result': influencers}, status=200)


def get_hot_tags(request, tag_number=4):
    return JsonResponse({
        'status': 'ok',
        'result': [{'hashtag': t[0], 'count': t[1]} for t in Profile.get_hot_tags(tag_number)]
    }, status=200)


def get_sector(request):
    return JsonResponse(
        {'status': 'ok',
         'sectors': [
             {'name': t[0], 'size': t[1]} for t in Profile.get_sectors()]
         }, status=200)


def get_places(request):
    return JsonResponse(
        {
            'status': 'ok',
            'places': Profile.get_places()
        }, status=200)


def get_user_stats(request):
    n_profiles = len(Profile.objects.all())

    n_male = len(Profile.objects.filter(gender='male'))
    n_female = len(Profile.objects.filter(gender='female'))
    n_other = n_profiles - n_male - n_female

    return JsonResponse({'status': 'ok',
                         'n_profiles': n_profiles,
                         'gender_info': {'n_male': n_male, 'n_female': n_female, 'other': n_other,
                                         'n_male_%': float(n_male)*100/n_profiles,
                                         'n_female_%': float(n_female) * 100 / n_profiles,
                                         'n_other_%': float(n_other) * 100 / n_profiles},
                         }, status=200)


@csrf_exempt
def post_om_invitation(request):

    if request.method != 'POST':
        return not_authorized()
    try:
        sender_first_name = request.POST['sender_first_name'].title()
        sender_last_name = request.POST['sender_last_name'].title()
        sender_email = request.POST['sender_email'].lower()
        receiver_first_name = request.POST['receiver_first_name'].title()
        receiver_last_name = request.POST['receiver_last_name'].title()
        receiver_email = request.POST['receiver_email'].lower()

        if sender_first_name.strip() == '' \
                or sender_last_name.strip() == '' \
                or sender_email.strip() == '' \
                or receiver_first_name.strip() == '' \
                or receiver_last_name.strip() == '' \
                or receiver_email.strip() == '':
            return bad_request("Please fill al the fields")


        # Return to dsp error page if sender is already a DSP user?
        try:
            User.objects.get(email=sender_email)
            return HttpResponseRedirect('http://openmaker.eu/error_sender/')
        except User.DoesNotExist:
            pass

        Invitation.create(
            sender_email=sender_email,
            sender_first_name=sender_first_name,
            sender_last_name=sender_last_name,
            receiver_first_name=receiver_first_name,
            receiver_last_name=receiver_last_name,
            receiver_email=receiver_email,
            sender_verified=False
        )

        activation_link = 'http://{}/om_confirmation/{}/{}/{}/{}/{}/{}'.format(
            get_current_site(request),
            sender_first_name.encode('utf-8').encode('base64'),
            sender_last_name.encode('utf-8').encode('base64'),
            sender_email.encode('base64'),
            receiver_first_name.encode('utf-8').encode('base64'),
            receiver_last_name.encode('utf-8').encode('base64'),
            receiver_email.encode('base64'))

        EmailHelper.email(
            template_name='invitation_email_confirm',
            title='OpenMaker Nomination.. almost done!',
            vars={
                'SENDER_NAME': sender_first_name,
                'CONFIRMATION_LINK': activation_link
            },
            receiver_email=sender_email
        )

    except KeyError:
        return bad_request("Please fill al the fields")
    except EmailAlreadyUsed:
        return HttpResponseRedirect('http://openmaker.eu/error_receiver/')
    except UserAlreadyInvited:
        return HttpResponseRedirect('http://openmaker.eu/error_invitation/')
    except SelfInvitation:
        # @TODO : make appropriate page in openmaker
        return bad_request("Sender and receiver must be different")
    except Exception as e:
        #@TODO : make appropriate page in openmaker
        return bad_request("Some erro occour please try again")

    return HttpResponseRedirect('http://openmaker.eu/pending_invitation/')

    # sender already a DSP user?
    # try:
    #     User.objects.get(email=sender_email)
    #     return HttpResponseRedirect('http://openmaker.eu/error_sender/')
    # except User.DoesNotExist:
    #     pass

    # receiver already a DSP user?
    # try:
    #     User.objects.get(email=receiver_email)
    #     return HttpResponseRedirect('http://openmaker.eu/error_receiver/')
    # except User.DoesNotExist:
    #     pass

    # receiver already invited?
    # try:
    #     Invitation.objects.get(receiver_email=HashHelper.md5_hash(receiver_email))
    #     return HttpResponseRedirect('http://openmaker.eu/error_invitation/')
    # except Invitation.DoesNotExist:
    #     pass

    # return HttpResponseRedirect('http://openmaker.eu/pending_invitation/')


def get_om_events(request):
    from django.conf import settings
    from eventbrite import Eventbrite
    eventbrite = Eventbrite(settings.ITA_API_KEY)
    try:
        ita_events = eventbrite.get('/users/me/owned_events')
        return JsonResponse({
            'status': 'ok',
            'results': {
                'italy': ita_events
            }}, status=200)
    except Exception as e:
        print(e.message)
        return JsonResponse({
            'status': 'error',
            'results': {}},
            status=500)

###########
# API V 1.4
###########

class v14:
    @staticmethod
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


    @staticmethod
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

        return success('ok','single entity',results)

    @staticmethod
    def get_entity(request, entity= 'news'):
        #TODO make cursor works
        profile = None
        results = []
        local_entities = None
        try:
            profile = request.user.profile
        except:
            # NOt logged user
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

        return success('ok','entity list',results)


    @staticmethod
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
            print(e)
            return not_authorized()

    @staticmethod
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
            print(e)
            return not_authorized()

    @staticmethod
    def get_bookmark_by_entities(request, entity=None):
        try:
            profile = request.user.profile
            results = profile.get_bookmarks(entity)
            serialized = BookmarkSerializer(results, many=True).data

            return JsonResponse({
                'status': 'ok',
                'result': serialized,
            }, status=200)
        except Exception as e:
            print(e)
            return not_authorized()

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def user_authorization(request):
        from dspexplorer.site_helpers import User
        return JsonResponse({
            'status': 'ok',
            'result': User.authorization(request) ,
        }, status=200)

    @staticmethod
    def login(request):
        from django.contrib.auth import authenticate, login

        from dashboard.serializer import UserSerializer
        from django.core.serializers import serialize


        data = json.loads(request.body)

        user = authenticate(
            username=data.get('username', False),
            password=data.get('password', False)
        )

        if user is not None:
            login(request, user)
        else:
            raise Http404('Username or password are wrong')

        return JsonResponse({
            'status': 'ok',
            'result': serialize('json', [user]),
        }, status=200)

    @staticmethod
    def logout(request):
        from django.contrib.auth import logout

        logout(request)

        return JsonResponse({
            'status': 'ok',
            'result': '',
        }, status=200)

###########
# API V 1.3
###########

class v13:
    @staticmethod
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

    @staticmethod
    def get_influencers(request, topic_id=1, location=None):
        if not location:
            place = json.loads(request.user.profile.place)
            location = place['country_short']
        try:
            results = DSPConnectorV13.get_influencers(topic_id, location)
        except DSPConnectorException:
            results = {}
        return JsonResponse({
            'status': 'ok',
            'result': results
        }, status=200)

    @staticmethod
    def get_audiences(request, topic_id=1, location=None):
        results = {}
        if not location:
            place = json.loads(request.user.profile.place)
            location = place['country_short']
        try:
            results = DSPConnectorV13.get_audiences(topic_id, location)
        except DSPConnectorException:
            results = {}
        return JsonResponse({
            'status': 'ok',
            'result': results
        }, status=200)

    @staticmethod
    def get_events(request, topic_id, location='', cursor=0):
        try:
            events = DSPConnectorV13.get_events(topic_id, location, cursor)
        except DSPConnectorException:
            events = {}
        'previous_cursor' not in events and events.update({'previous_cursor': 0})

        return JsonResponse({
            'status': 'ok',
            'result': events
        }, status=200)


    @staticmethod
    def get_hashtags(request, topic_id=1, date_string='yesterday'):
        try:
            results = DSPConnectorV13.get_hashtags(topic_id, date_string)['hashtags']
        except DSPConnectorException:
            results = {}
        return JsonResponse({
            'status': 'ok',
            'result': results
        }, status=200)

    @staticmethod
    def get_news(request, topic_id=1, date_string='yesterday', cursor=0):

        item_per_page = 20
        news = []
        next_cursor = 0
        resp = {}

        try:
            results = DSPConnectorV13.get_news(topic_id, date_string, cursor)
            # news = results['news']
            # next_cursor = results['next_cursor']/item_per_page
            # resp = {'news': news, 'next_cursor': next_cursor, 'max_page': None}
        except DSPConnectorException:
            pass
        return JsonResponse({
            'status': 'ok',
            'result': results,
        }, status=200)

    # @staticmethod
    # def get_themes(request):
    #     return v13.__wrap_response(v13.get_themes)
    @staticmethod
    def project_invitation_confirmation(request, status=None, project_id=None, profile_id=None):
        pass

    @staticmethod
    def project_invitation(request, status=None):

        # ToDo add token to avoid actions not allowed

        from dashboard.serializer import ProjectContributorSerializer
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                project_id = body['project_id']
                profile_id = body['profile_id']

                profile = Profile.objects.get(id=profile_id)
                project = Project.objects.get(id=project_id, profile=request.user.profile)

                # can not invite yourself
                if profile == request.user.profile:
                    return bad_request('you are the owner of the project')

                contribution = ProjectContributor.objects.filter(project=project, contributor=profile)

                if len(contribution):
                    if status is not None:
                        # update the status of the invitation / collaboration
                        contribution.update(status=status)
                        serialized = ProjectContributorSerializer(contribution).data
                        return success('ok', 'invitation updated', serialized)
                    else:
                        # ToDo send e-mail
                        email_context = {
                            'FIRST_NAME': profile.user.first_name,
                            'LAST_NAME': profile.user.last_name,
                            'PROJECT_OWNER_FIRST_NAME': request.user.first_name,
                            'PROJECT_OWNER_LAST_NAME': request.user.last_name,
                            'PROJECT_NAME': project.name,
                            'CONFIRMATION_LINK': 'http://{}/profile/{}/invitation/{}/accepted/'.format(
                                get_current_site(request),
                                profile.id,
                                project.id,
                            ),
                            'DECLINE_LINK': 'http://{}/profile/{}/invitation/{}/declined/'.format(
                                get_current_site(request),
                                profile.id,
                                project.id,
                            ),
                        }

                        if contribution.first().status == 'pending':
                            message = 'invitation re-sent'
                        else:
                            contribution.update(status='pending')
                            message = 'invitation sent'

                        EmailHelper.email(
                            template_name='collaborator_invitation',
                            title='Openmaker Explorer - Project nomination',
                            vars=email_context,
                            receiver_email=profile.user.email
                        )

                        serialized = ProjectContributorSerializer(contribution).data
                        return success('ok', message, serialized)
                else:
                    'CREATING NEW INVITATION'
                    # invitation not exist --> create and send e-mail
                    contribution = ProjectContributor(project=project, contributor=profile)
                    contribution.save()
                    email_context = {
                        'FIRST_NAME': profile.user.first_name,
                        'LAST_NAME': profile.user.last_name,
                        'PROJECT_OWNER_FIRST_NAME': request.user.first_name,
                        'PROJECT_OWNER_LAST_NAME': request.user.last_name,
                        'PROJECT_NAME': project.name,
                        'CONFIRMATION_LINK': 'http://{}/profile/{}/invitation/{}/accepted/'.format(
                            get_current_site(request),
                            profile.id,
                            project.id,
                        ),
                        'DECLINE_LINK': 'http://{}/profile/{}/invitation/{}/declined/'.format(
                            get_current_site(request),
                            profile.id,
                            project.id,
                        ),
                    }

                    EmailHelper.email(
                        template_name='collaborator_invitation',
                        title='Openmaker Explorer - Project nomination',
                        vars=email_context,
                        receiver_email=profile.user.email
                    )

                    serialized = ProjectContributorSerializer(contribution).data
                    return success('ok', 'invitation sent', serialized)
            except ObjectDoesNotExist as o:
                print('ERROR ObjectDoesNotExist')
                print(o)
                return error()
            except Exception as e:
                print('ERROR Exception')
                print(e)
                return error()
        else:
            bad_request('only post for now')

    @staticmethod
    def project(request, project_id=None):
        from dashboard.serializer import ProjectSerializer
        # DELETE PROJECT
        if request.method == 'DELETE' and project_id is not None:
            try:
                profile = request.user.profile
                projects = Project.objects.get(id=project_id, profile=profile)
                projects.delete()
            except ObjectDoesNotExist as e:
                print(e)
                print(not_authorized())
            return success('ok', 'project deleted', {})

        # GET ALL
        if request.method == 'GET' and project_id is None:
            try:
                profile = request.user.profile
                projects = Project.objects.filter(profile=profile)
                serialized = ProjectSerializer(projects, many=True)
                return success('ok', 'user projects', serialized.data)
            except Exception as e:
                print(e)
                return not_found()

        # GET SINGLE
        if request.method == 'GET' and project_id is not None:
            try:
                project = Project.objects.filter(id=project_id)
                serialized = ProjectSerializer(project, many=True)
                return success('ok', 'single project', serialized.data)
            except ObjectDoesNotExist as o:
                print(o)
                return not_found()
            except Exception as e:
                print(e)
                return error()

        # UPDATE
        if request.method == 'POST' and project_id is not None:
            data_to_update = {}
            data_to_update['name'] = request.POST.get('name', '')
            data_to_update['description'] = request.POST.get('description', '')
            data_to_update['start_date'] = request.POST.get('start_date', '')
            data_to_update['creator_role'] = request.POST.get('creator_role', '')
            data_to_update['project_url'] = request.POST.get('project_url', '')
            end_date = request.POST.get('end_date', '')

            # check if the image needs to be updated
            if request.POST.get('picture', None) != '':
                # image to be updated
                picture = request.FILES.get('picture')
                v13.check_image(picture)
                data_to_update['picture'] = picture
            # check if is or not an ongoing project
            try:
                if end_date != '':
                    end_date = dt.strptime(end_date, '%Y-%m-%d')
                    data_to_update['start_date'] = dt.strptime(data_to_update['start_date'], '%Y-%m-%d')
                    # if end_date > dt.now():
                    #     return bad_request('The project end_date cannot be in the future')
                    if end_date < data_to_update['start_date']:
                        return bad_request('The project end date cannot be before the project start date')
                    data_to_update['end_date'] = end_date
            except Exception as e:
                print(e)
                return error()
            # get the model object and check the profile owns that project
            try:
                profile = request.user.profile
                project = Project.objects.filter(id=project_id, profile=profile).first()
                # clear and update tag
                project.set_tags(request.POST.get('tags', ''))
                # remove tag from data_to_update
                project.__dict__.update(data_to_update)
                project.save()
            except Project.DoesNotExist as e:
                print(e)
                return not_authorized()
            except Exception as e:
                print(e)
                return error()
            result = ProjectSerializer(project).data
            return success('ok', 'project updated', result)

        # CREATE
        if request.method == 'POST' and project_id is None:
            # check if fields are filled
            try:
                project_image = request.FILES.get('picture')
                project_name = request.POST['name']
                project_description = request.POST['description']
                project_start_date = dt.strptime(request.POST['start_date'], '%Y-%m-%d')
                project_creator_role = request.POST['creator_role']
                project_url = request.POST['project_url']
                project_tags = request.POST['tags']

                # Check image
                is_image_ok = v13.check_image(project_image)
                if is_image_ok is not True:
                    return is_image_ok

            except KeyError as k:
                print(k)
                return bad_request("Please fill all the fields")
            except Exception as e:
                return bad_request(e)

            # check if is or not an ongoing project
            try:
                project_end_date = dt.strptime(request.POST['end_date'], '%Y-%m-%d')
            except KeyError:
                project_end_date = None

            # if it is not an ongoing project check dates
            if project_end_date is not None:
                if project_end_date < project_start_date:
                    return bad_request('The project END DATE cannot be before the project START DATE')

            try:
                # check user has not project with that name
                profile = request.user.profile
                projects = Project.objects.filter(profile=profile, name=project_name)
                if len(projects) > 0:
                    return bad_request('Project name already exist')

                project = Project(profile=profile,
                                  name=project_name,
                                  picture=project_image,
                                  description=project_description,
                                  start_date=project_start_date,
                                  end_date=project_end_date,
                                  creator_role=project_creator_role,
                                  project_url=project_url)
                project.save()
                project.tags.clear()
                for tagName in [x.lower().capitalize() for x in project_tags.split(",")]:
                    project.tags.add(Tag.objects.filter(name=tagName).first() or Tag.create(name=tagName))
                project.save()
                result = ProjectSerializer(project).data
            except Exception as e:
                return bad_request(e)

            return success('ok', 'project created', result)

    @staticmethod
    def check_image(project_image):
        # check image is an image and has a proper dimension
        try:
            filename, file_extension = os.path.splitext(project_image.name)
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if not (file_extension in allowed_extensions):
                raise ValueError('nonvalid')

            # limit to 1MB
            if project_image.size > 1048576:
                raise ValueError('sizelimit')
                project_image.name = str(datetime.now().microsecond) + '_' + str(project_image._size) + file_extension
        except ValueError as exc:
            if str(exc) == 'sizelimit':
                return bad_request('Image size must be less than 1MB')
            if str(exc) == 'nonvalid':
                return bad_request('The file you uploaded is not a supported image file ( you must upload a jpg or a png file')
        except KeyError as k:
            print(k)
            return bad_request("please fill all the fields")
        except Exception as e:
            print(e)
            return bad_request('Some error in the image upload process occour. Please try again.')
        else:
            return True

###########
# API V 1.2
###########

def get_topics(request):
    try:
        topics = DSPConnectorV12.get_topics()
    except DSPConnectorException:
        topics = {}
    return JsonResponse({
        'status': 'ok',
        'result': topics
    }, status=200)


def get_suggested_topic(request):
    try:
        topics = DSPConnectorV12.get_topics()['topics']
        random_topic = topics[random.randint(0, len(topics) - 1)]
    except DSPConnectorException:
        random_topic = {}
    return JsonResponse({
        'status': 'ok',
        'result': random_topic
    }, status=200)


def get_news(request, topic_ids, date_name='yesterday', cursor=-1):
    date_dict = {
        'yesterday': date.today() - timedelta(1),
        'week': date.today() - timedelta(7),
        'month': date.today() - timedelta(30)
    }
    try:
        since = date_dict[date_name].strftime('%d-%m-%Y')
        news = DSPConnectorV12.search_news(topic_ids, {'since': since, 'cursor': cursor})
    except DSPConnectorException:
        news = {}

    return JsonResponse({
        'status': 'ok',
        'result': news
    }, status=200)


def get_events(request, topic_ids, cursor=-1):
    try:
        events = DSPConnectorV12.get_events(topic_ids, cursor)
    except DSPConnectorException:
        events = {}

    return JsonResponse({
        'status': 'ok',
        'result': events
    }, status=200)


def get_audiences(request, topic_id):
    try:
        audiences = DSPConnectorV12.get_audiences(topic_id)
    except DSPConnectorException:
        audiences = {}
    return JsonResponse({
        'status': 'ok',
        'result': audiences
    }, status=200)


def update_field(request, to_be_updated, update_token):
    import threading

    if not update_token == settings.UPDATE_TOKEN:
        return not_authorized()

    if to_be_updated == 'crm':
        users = User.objects.all()
        thr = threading.Thread(target=create_or_update_party, kwargs=dict(users=users))
        thr.start()

    if to_be_updated == 'default_img':
        # update default images
        users = User.objects.all()
        thr = threading.Thread(target=update_default_profile_image, kwargs=dict(users=users))
        thr.start()

    return JsonResponse({'status': 'ok', 'updating': to_be_updated}, status=200)


def update_default_profile_image(users):
    errored = []
    sanititized = []
    for user in users:
        try:
            if user.profile.picture == 'images/profile/default_user_icon.png':
                print ('--------------------')
                print ('UPDATING USER : %s' % user)
                print ('--------------------')
                print (' ')
                if user.profile.gender == 'male': user.profile.picture = 'images/profile/male.svg'
                if user.profile.gender == 'female': user.profile.picture = 'images/profile/female.svg'
                if user.profile.gender == 'other': user.profile.picture = 'images/profile/other.svg'
                sanititized.append(user.email)
                user.profile.save()
        except Profile.DoesNotExist as e:
            errored.append(user.email)
            print(Colorizer.custom('[ERROR USER MALFORMED] : %s ' % e, 'white', 'purple'))
            print (' ')
    # PRINT RESULTS
    print ('-------------')
    print ('TOTAL RESULTS')
    print ('-------------')

    if len(errored):
        print(Colorizer.Red('%s errored users' % len(errored)))
        print(errored)

    if len(sanititized):
        print(Colorizer.Purple('%s updated users : ' % len(sanititized)))
        print(sanititized)

    elif not len(errored) and not len(sanititized):
        print(Colorizer.Green('no updates or errors'))
    print('-------------')


def create_or_update_party(users):
    errored = []
    sanititized = []
    party = None
    for user in users:
        try:
            print ('--------------------')
            print ('UPDATING USER : %s' % user)
            print ('--------------------')
            print (' ')
            # logger.debug('UPDATING %s' % user)
            party = Party(user)
            party.create_or_update()
            # logger.debug('UPDATED')
            print(Colorizer.Green('UPDATED %s' % user))
            print (' ')

        except Profile.DoesNotExist as e:
            print(Colorizer.custom('[ERROR USER MALFORMED] : %s ' % e, 'white', 'purple'))
            print(' ')

        except Exception as e:
            try:
                print(Colorizer.Red('Try to exclude incompatible custom fields for user: %s' % user))
                party.safe_create_or_update()
                sanititized.append(user.email)
                print(Colorizer.Yellow('UPDATED partially: %s' % user))
                print(' ')

            except Exception as safe_exc:
                print(Colorizer.Red('[ ERROR IN SAFE UPDATE ] : %s' % safe_exc))
                print(json.dumps(party.as_dict(), indent=1))
                print((' '))

                print(Colorizer.Red('ERROR UPDATING USER : %s' % user))
                print('ERROR: %s' % e)
                print(' ')
                errored.append(user.email)

    # PRINT RESULTS
    print('-------------')
    print('TOTAL RESULTS')
    print('-------------')

    if len(errored):
        print(Colorizer.Red('%s errored users' % len(errored)))
        # logger.error('ERROR updating users : %s' % errored)
        print(errored)

    if len(sanititized):
        print(Colorizer.Purple('%s partially updated users : ' % len(sanititized)))
        print(sanititized)

    elif not len(errored) and not len(sanititized):
        print(Colorizer.Green('No errored users'))
    print('-------------')


def check_canvas(request, twitter_username):
    url = settings.INSIGHT_BASE_URL + settings.INSIGHT_API_URL + twitter_username
    res = {}

    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        res['result'] = False
        res['status'] = 'error'
        return JsonResponse(res, status=200)

    if response.status_code == 200:
        res['result'] = True
    else:
        res['result'] = False

    res['status'] = 'ok'

    return JsonResponse(res, status=200)


@login_required
def get_invitation_csv(request):
    import csv
    try:
        if request.user.is_superuser:
            response = HttpResponse(
                csv,
                content_type='application/csv'
            )
            response['Content-Disposition'] = \
                'attachment; filename="invitation.csv"'

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="OmExplorer_invitations.csv"'

            writer = csv.writer(response, delimiter=';', lineterminator='\n', quoting=csv.QUOTE_ALL, dialect='excel')

            invitations = Invitation.objects.all()

            writer.writerow([
                'sender email',
                'sender first_name',
                'sender last_name',
                'receiver email',
                'receiver first_name',
                'receiver last_name'
            ])

            for invitation in invitations:
                writer.writerow([
                    invitation.sender_email.encode('utf8'),
                    invitation.sender_first_name.encode('utf8'),
                    invitation.sender_last_name.encode('utf8'),
                    invitation.receiver_email.encode('utf8'),
                    invitation.receiver_first_name.encode('utf8'),
                    invitation.receiver_last_name.encode('utf8'),
                ])

            return response
    except:
        return bad_request("Error generating invitation csv")


@login_required
def get_challenge(request, challenge_id=None):
    from dashboard.serializer import ChallengeSerializer

    if challenge_id is not None:
        results = ChallengeSerializer(
            Challenge.objects.filter(pk=challenge_id).order_by('-created_at')
            , many=True
        ).data[0]
    else:
        results = ChallengeSerializer(
            Challenge.objects.all().order_by('-created_at')
            , many=True
        ).data
    return JsonResponse(results, safe=False)


@login_required
def get_profile_challenge(request, profile_id):
    from dashboard.serializer import ChallengeSerializer
    results = []
    try:
        profile = Profile.objects.get(pk=profile_id)
        results = profile.get_interests(Challenge)
        results = ChallengeSerializer(results if len(results) > 0 else [], many=True).data
    except Exception as e:
        response = JsonResponse({'status': 'error', 'message': ''})
        response.status_code = 500
        return response

    return JsonResponse(results, safe=False)


@login_required
def get_profile_projects(request, profile_id):
    from dashboard.serializer import ProjectSerializer
    try:
        profile = Profile.objects.get(pk=profile_id)
        projects = Project.objects.filter(profile=profile)
        serialized = ProjectSerializer(projects, many=True)
        return success('ok', 'user projects', serialized.data)
    except Exception as e:
        print(e)
        response = JsonResponse({'status': 'error', 'message': ''})
        response.status_code = 500
        return response


@login_required
def get_interest_ids(request):
    return JsonResponse([int(x.pk) for x in request.user.profile.get_interests(Challenge)], safe=False)

@login_required
def get_interest_object_ids(request, model_object=None):
    if model_object is None:
        return bad_request('model missing')
    else:
        try:
            model = apps.get_model(app_label='dashboard', model_name=model_object.title())
            return JsonResponse([int(x.pk) for x in request.user.profile.get_interests(model)], safe=False)
        except ObjectDoesNotExist as e:
            print(e)
            error('model not found')
        except Exception as e:
            print(e)
            error()


@login_required
def interest_challenge(request, challenge_id):
    try:
        challenge = Challenge.objects.get(pk=challenge_id)
        email_context = {
            'USER_NAME': request.user.first_name+' '+request.user.last_name,
            'USER_EMAIL': request.user.email,
            'USER_URL': request.build_absolute_uri(reverse('dashboard:profile', kwargs={'profile_id': request.user.profile.pk})),
            'CHALLENGE_TITLE': challenge.title,
            'CHALLENGE_URL': request.build_absolute_uri(reverse('dashboard:challenge', kwargs={'challenge_id': challenge.pk})),
            'COORDINATOR_EMAIL': challenge.coordinator_email
        }


        if request.method == 'POST':
            # Add interest
            request.user.profile.add_interest(challenge)
            # Email Coordinator
            challenge.notify_admin and EmailHelper.email(
                template_name='challenge/challenge_coordinator_interest_added',
                title='Openmaker Explorer - Challenge interest ADDED',
                vars=email_context,
                receiver_email=email_context['COORDINATOR_EMAIL']
            )
        if request.method == 'DELETE':
            # Remove interest
            request.user.profile.delete_interest(Challenge, challenge_id)
            # Email Coordinator
            challenge.notify_admin and EmailHelper.email(
                template_name='challenge/challenge_coordinator_interest_removed',
                title='Openmaker Explorer - Challenge interest REMOVED',
                vars=email_context,
                receiver_email=email_context['COORDINATOR_EMAIL']
            )
            # Email User
            challenge.notify_user and EmailHelper.email(
                template_name='challenge/challenge_user_interest_removed',
                title='Openmaker Explorer - Challenge interest REMOVED',
                vars=email_context,
                receiver_email=email_context['COORDINATOR_EMAIL']
            )
        return JsonResponse({'status': 'success'})

    except Exception as e:
        print(e)
        response = JsonResponse({'status': 'error', 'message': e})
        response.status_code = 500
        return response


@login_required
def interest_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)

        if request.method == 'POST':
            # Add interest
            request.user.profile.add_interest(project)
            message = 'interest in project added'
        if request.method == 'DELETE':
            # Remove interest
            request.user.profile.delete_interest(Project, project_id)
            message = 'interest in project removed'
        return success('ok', message, {})

    except Exception as e:
        print(e)
        response = JsonResponse({'status': 'error', 'message': e})
        response.status_code = 500
        return response


@login_required
def interest_entity(request, entity_type='article', entity_external_id=None):
    try:
        entity = EntityProxy.objects.filter(externalId=entity_external_id, entity_type=entity_type)

        if not entity:
            entity = EntityProxy(externalId=entity_external_id, entity_type=entity_type)
            entity.save()

        if request.method == 'POST':
            # Add interest
            request.user.profile.add_interest(entity)
            message = 'interest in entity added'
        if request.method == 'DELETE':
            # Remove interest
            request.user.profile.delete_interest(EntityProxy, entity.pk)
            message = 'interest in entity removed'
        return success('ok', message, {})

    except Exception as e:
        print(e)
        response = JsonResponse({'status': 'error', 'message': e})
        response.status_code = 500
        return response
