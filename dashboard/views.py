# -*- coding: utf-8 -*-
import pytz
from django.contrib.auth.models import User
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from crmconnector import capsule
from utils.mailer import EmailHelper
from utils.hasher import HashHelper
from dspconnector.connector import DSPConnectorException, DSPConnectorV12, DSPConnectorV13
from .models import Profile, Invitation, Feedback, Tag, SourceOfInspiration, Project, ProjectContributor
from .exceptions import EmailAlreadyUsed, UserAlreadyInvited, InvitationDoesNotExist, InvitationAlreadyExist, SelfInvitation
from django.http import HttpResponseRedirect
# from form import FeedbackForm
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, invitation_email_receiver
import datetime as dt, json, os, logging, re, random

from crmconnector.models import Party
from rest_framework.exceptions import NotFound
from dashboard.models import Location

logger = logging.getLogger(__name__)
from utils.GoogleHelper import GoogleHelper

@login_required()
def dashboard(request, topic_id=None):
    '''
    top_influencers_by_user_location = None
    events_by_topic_and_location = None
    audiences = None
    events_by_topic_and_location = None
    selected_topic = None
    topics = None
    last_members = None
    hot_tags = None
    json_hot_tags = None
    hot_news = None

    try:
        topics_list = DSPConnectorV12.get_topics()['topics']

        if topic_id:
            selected_topic = filter(lambda x: x['topic_id'] == int(topic_id), topics_list)[0]
        else:
            selected_topic = random.choice(topics_list)

        hot_news = DSPConnectorV13.get_news(selected_topic['topic_id'])['news'][:4]

        # check user location and according to that ask for events, influencers and audiences
        profile = request.user.profile
        user_profile_location = profile.get_location()['country_short'] if 'country_short' in profile.get_location() else ''

        top_influencers_by_user_location = DSPConnectorV13.get_influencers(
            selected_topic['topic_id'],
            user_profile_location
        )['local_influencers'][:4]
        audiences = DSPConnectorV13.get_audiences(selected_topic['topic_id'], user_profile_location)['audience_sample'][:4]

        events_by_topic_and_location = DSPConnectorV13.get_events(selected_topic['topic_id'], user_profile_location.lower())['events'][:4]

    except DSPConnectorException as e:
        messages.error(request, e.message)
        topics_list = {}
        selected_topic = 'No themes'
        context = {'selected_topic': selected_topic, 'topics': topics_list}
        return render(request, 'dashboard/theme.html', context)
    except Exception as e:
        print 'Exception -- '
        print e

    hot_tags = [t[0] for t in Profile.get_hot_tags(30)]
    last_members = Profile.get_last_n_members(3)

    context = {
        'selected_topic': selected_topic,
        'topics': topics_list,
        'last_members': last_members,
        'hot_tags': hot_tags,
        'json_hot_tags': json.dumps(hot_tags),
        'hot_news': hot_news,
        'top_influencers': top_influencers_by_user_location,
        'audiences':audiences,
        'events': events_by_topic_and_location
    }

    return render(request, 'dashboard/dashboard.html', context)
    '''
    return HttpResponseRedirect(reverse('dashboard:login'))


def news_list(request):
    context = {
        'entity': 'news',
        'slider': 'events-projects'
    }
    return render(request, 'dashboard/entity_list.html', context)


def news_detail(request, news_id):
    context = {
        'entity': 'news',
        'entity_id': news_id,
        'slider': 'events-projects'
    }
    return render(request, 'dashboard/news_detail.html', context)


def event_list(request):
    context = {
        'entity': 'events',
        'slider': 'news-projects'
    }
    return render(request, 'dashboard/entity_list.html', context)


def project_list(request):
    return render(request, 'dashboard/entity_list.html')

@login_required()
def insight(request, user_twitter_username=None):
    try:
        user_profile_twitter_username = Profile.get_by_email(request.user.email).twitter_username
    except:
        messages.warning(request, 'Hey fill your Twitter username to check your Insight data!')
        # user_profile_twitter_username = ''
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    canvas_url = settings.INSIGHT_BASE_URL + settings.INSIGHT_API_URL

    context = {
        'user_profile_twitter_username': str(user_profile_twitter_username),
        'canvas_url': str(canvas_url)
    }
    return render(request, 'dashboard/insight.html', context)


@login_required()
def theme(request, topic_id):
    selected_location = ''
    try:
        topics_list = DSPConnectorV12.get_topics()['topics']
        selected_topic = filter(lambda x: str(x['topic_id']) == str(topic_id), topics_list)[0] if topic_id else \
            random.choice(topics_list)
    except DSPConnectorException as e:
        messages.error(request, e.message)
        topics_list = {}
        selected_topic = 'No themes'
    except IndexError:
        return HttpResponseRedirect(reverse('dashboard:theme'))

    try:
        selected_location = json.loads(request.user.profile.place)['country_short']
    except:
        selected_location = ''
    context = {
        'selected_topic': selected_topic,
        'topics': topics_list,
        'selected_location': selected_location
    }
    return render(request, 'dashboard/theme.html', context)


@login_required()
def events(request, topic_id):
    user_profile_location = {}
    user_profile_location['short_code'] = json.loads(Profile.get_by_email(request.user.email).place)['country_short'].lower()
    user_profile_location['label'] = json.loads(Profile.get_by_email(request.user.email).place)['country']
    try:
        topics_list = DSPConnectorV12.get_topics()['topics']
        selected_topic = filter(lambda x: str(x['topic_id']) == str(topic_id), topics_list)[0] if topic_id else \
            random.choice(topics_list)
    except DSPConnectorException as e:
        messages.error(request, e.message)
        topics_list = {}
        selected_topic = 'No themes'
    except IndexError:
        return HttpResponseRedirect(reverse('dashboard:events'))
    context = {'selected_topic': selected_topic, 'topics': topics_list, 'country': user_profile_location}
    return render(request, 'dashboard/events.html', context)


@login_required()
def test(request):
    from dashboard.form import ProfileForm

    # print json.dumps(request.POST)
    # form = ProfileForm(data=dict(request.POST), files=request.FILES)

    # if form.is_valid():
    #     print 'Form is valid'
    #     print 'Form data :'
    #     print form.fields
    # else:
    #     print 'form not valid'
    #     print form.errors

    form = ProfileForm(request.POST or None)

    return render(request, 'test.html', {'form': form})


@login_required()
def profile(request, profile_id=None, action=None):
    try:
        if profile_id:
            user_profile = Profile.get_by_id(profile_id)
        else:
            user_profile = Profile.get_by_email(request.user.email)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    # Delete Profile
    if request.method == 'POST' and action == 'delete':
        try:
            first_name=request.user.first_name
            last_name=request.user.last_name

            Profile.delete_account(request.user.pk)
            messages.success(request, 'Account deleted')

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
            print 'error removing user'
            print e
            messages.warning(request, 'An error occour deleting your profile, please try again.')
            return HttpResponseRedirect(reverse('dashboard:profile'))

        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    # Update Profile
    if request.method == 'POST' and request.POST.get('action') != 'delete':
        new_profile = {}
        new_user = {}
        try:
            new_user['first_name'] = request.POST['first_name'].title()
            new_user['last_name'] = request.POST['last_name'].title()
            new_profile['gender'] = request.POST['gender']

            new_profile['birthdate'] = datetime.strptime(request.POST['birthdate'], '%Y/%m/%d')
            new_profile['birthdate'] = pytz.utc.localize(new_profile['birthdate'])

            new_profile['city'] = request.POST['city']
            new_profile['occupation'] = request.POST['occupation']

            new_profile['statement'] = request.POST.get('statement', None)

            # @TODO : check duplicate role assignment
            new_profile['role'] = request.POST.get('role', None)
            new_profile['role'] = request.POST.get('role', '')

            new_profile['organization'] = request.POST.get('organization', None)
            new_profile['sector'] = request.POST.get('sector', None)
            new_profile['size'] = request.POST.get('size', None)
            new_profile['technical_expertise'] = request.POST.get('technical_expertise', None)

            new_profile['technical_expertise_other'] = request.POST.get('technical_expertise_other', None)
            new_profile['role_other'] = request.POST.get('role_other', None)
            new_profile['sector_other'] = request.POST.get('sector_other', None)

            # Multiple choice fields
            new_profile['types_of_innovation'] = request.POST.get('types_of_innovation', None)
            new_profile['socialLinks'] = request.POST.get('socialLinks', None)
            
            # Many to many fields
            source_of_inspiration = request.POST.get('source_of_inspiration', None)
            
            tags = request.POST['tags']
            if tags == '' or tags == None or tags == 'undefined':
                raise KeyError
        
        except ValueError:
            messages.error(request, 'Incorrect birthdate format: it must be YYYY/MM/DD')
            return HttpResponseRedirect(reverse('dashboard:profile',  kwargs={'profile_id': user_profile.id, 'action':action}))
        except KeyError:
            print(KeyError)
            messages.error(request, 'Please fill the required fields!')
            return HttpResponseRedirect(reverse('dashboard:profile',  kwargs={'profile_id': user_profile.id, 'action':action}))
        
        # check birthdate
        if new_profile['birthdate'] > pytz.utc.localize(datetime(dt.datetime.now().year - 13, *new_profile['birthdate'].timetuple()[1:-2])):
            messages.error(request, 'You must be older than thirteen')
            return HttpResponseRedirect(reverse('dashboard:profile',  kwargs={'profile_id': user_profile.id, 'action':action}))

        # Update image
        try:
            imagefile = request.FILES['profile_img']
            filename, file_extension = os.path.splitext(imagefile.name)
            
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if not (file_extension in allowed_extensions):
                raise ValueError('nonvalid')
            
            # limit to 1MB
            if imagefile.size > 1048576:
                raise ValueError('sizelimit')
            
            imagefile.name = str(datetime.now().microsecond) + '_' + str(imagefile._size) + file_extension
        
        except ValueError as exc:
            if str(exc) == 'sizelimit':
                messages.error(request, 'Image size must be less than 1MB')
            if str(exc) == 'nonvalid':
                messages.error(request, 'Profile Image is not an image file')
            return HttpResponseRedirect(reverse('dashboard:profile'))
        
        except KeyError as exc:
            imagefile = request.user.profile.picture
        except Exception as exc:
            messages.error(request, 'Error during image upload, please try again')
            logging.error('[VALIDATION_ERROR] Error during image upload: {USER} , EXCEPTION {EXC}'.format(
                USER=request.user.email, EXC=exc
            ))
            return HttpResponseRedirect(reverse('dashboard:profile'))
        new_profile['picture'] = imagefile
        
        user = User.objects.filter(email=request.user.email).first()
        
        # Update user fields
        user.__dict__.update(new_user)
        user.save()
        # Update profile fields
        user.profile.__dict__.update(new_profile)
        user.profile.save()

        # Update place, location, country
        user.profile.set_place(request.POST.get('place', None))
        
        # Update tags
        user.profile.tags.clear()
        for tagName in map(lambda x: re.sub(r'\W', '', x.lower().capitalize(), flags=re.UNICODE), tags.split(",")):
            user.profile.tags.add(Tag.objects.filter(name=tagName).first() or Tag.create(name=tagName))
        
        # Update sourceofinnovation
        user.profile.source_of_inspiration.through.objects.all().delete()
        if source_of_inspiration:
            for tagName in map(lambda x: x.lower().capitalize(), source_of_inspiration.split(",")):
                user.profile.source_of_inspiration.add(
                    SourceOfInspiration.objects.filter(name=tagName).first() or
                    SourceOfInspiration.create(name=tagName)
                )

        # # Add location and Country
        # try:
        #     print 'profile place'
        #     if not user.profile.place or 'city' not in user.profile.place:
        #         print 'no place'
        #         new_place = GoogleHelper.get_city(user.profile.city)
        #         if new_place:
        #             user.profile.place = json.dumps(new_place)
        #             user.profile.save()
        #             print user.profile.place
        #     if user.profile.place:
        #         print 'there is place'
        #         place = json.loads(user.profile.place)
        #         location = Location.create(
        #             lat=repr(place['lat']),
        #             lng=repr(place['long']),
        #             city=place['city'],
        #             state=place['state'],
        #             country=place['country'],
        #             country_short=place['country_short'],
        #             post_code=place['post_code'] if 'post_code' in place else '',
        #             city_alias=place['city']+','
        #         )
        #
        #         user.profile.location = location
        #         user.profile.save()
        #
        # except Exception as e:
        #     print e

        # update on crm
        try:
            party = Party(user)
            party.create_or_update()
        except NotFound as e:
            messages.error(request, 'There was some connection problem, please try again')
            return HttpResponseRedirect(reverse('dashboard:profile'))
        except Exception as e:
            pass

        messages.success(request, 'Profile updated!')
        return HttpResponseRedirect(reverse('dashboard:profile'))
    
    user_profile.jsonTags = json.dumps(map(lambda x: x.name, user_profile.tags.all()))
    user_profile.jsonSourceOfInspiration = json.dumps(map(lambda x: x.name, user_profile.source_of_inspiration.all()))
    
    user_profile.types_of_innovation = user_profile.types_of_innovation and json.dumps(user_profile.types_of_innovation.split(','))
    print user_profile.pk
    context = {
        'profile': user_profile,
        'profile_action': action,
        'is_my_profile': request.user.profile.id == user_profile.id,
        'tags': json.dumps(map(lambda x: x.name, Tag.objects.all())),
        'source_of_inspiration': json.dumps(map(lambda x: x.name, SourceOfInspiration.objects.all()))
    }

    return render(request, 'dashboard/profile.html', context)


@login_required()
def community(request, search_string=''):
    return render(request, 'dashboard/community.html', {
        'search_string': search_string,
        'hot_tags': json.dumps([t[0] for t in Profile.get_hot_tags(30)]),
        'n_registered_user': Profile.objects.count()
    })


@login_required()
def invite(request):
    if request.method == 'POST':
        try:
            receiver_email = request.POST['email'].lower()
            first_name = request.POST['first_name'].title()
            last_name = request.POST['last_name'].title()

            if first_name.strip() == '' or last_name.strip() == '' or receiver_email.strip() == '':
                messages.error(request, 'Please fill all the required fields!')
                return HttpResponseRedirect(reverse('dashboard:invite'))

            Invitation.create(
                user=request.user,
                sender_email=request.user.email,
                sender_first_name=request.user.first_name,
                sender_last_name=request.user.last_name,
                receiver_first_name=first_name,
                receiver_last_name=last_name,
                receiver_email=receiver_email
            )

            # Emails
            email_vars = {
                'RECEIVER_FIRST_NAME': first_name.encode('utf-8'),
                'RECEIVER_LAST_NAME': last_name.encode('utf-8'),
                'SENDER_FIRST_NAME': request.user.first_name.encode('utf-8'),
                'SENDER_LAST_NAME': request.user.last_name.encode('utf-8'),
                'ONBOARDING_LINK': request.build_absolute_uri('/onboarding/')
            }
            # Send email to receiver only the first time
            if len(Invitation.get_by_email(receiver_email=receiver_email)) == 1:
                EmailHelper.email(
                    template_name='invitation_email_receiver',
                    title='You are invited to join the OpenMaker community!',
                    vars=email_vars,
                    receiver_email=receiver_email
                )
            # Send mail to sender
            EmailHelper.email(
                template_name='invitation_email_confirmed',
                title='OpenMaker Nomination done!',
                vars=email_vars,
                receiver_email=request.user.email
            )

            messages.success(request, 'Invitation sent!')

        except KeyError:
            messages.error(request, 'Please fill all the required fields!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except EmailAlreadyUsed:
            messages.error(request, 'User is already a member!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except UserAlreadyInvited:
            messages.error(request, 'You have already invited this Person!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except SelfInvitation:
            messages.error(request, 'You cannot invite youself!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except Exception as e:
            print e.message
            messages.error(request, 'Please try again!')
            return HttpResponseRedirect(reverse('dashboard:invite'))

    return render(request, 'dashboard/invite.html', {})


@login_required()
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                Feedback(user=request.user, title=request.POST['title'],
                         message_text=request.POST['message_text']).save()
                messages.success(request, 'Thanks for your feedback!')
            except KeyError:
                messages.warning(request, 'Error, please try again.')
        else:
            messages.error(request, 'Please all the fields are required!')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))


@login_required()
def challenge(request, challenge_id=None):
    return render(request, 'dashboard/challenge.html', {'challenge_id': challenge_id})


@login_required()
def project(request, project_id=None, action=None, profile_id=None):

    return render(request, 'dashboard/project.html', {'project_id': project_id, 'tags': json.dumps(map(lambda x: x.name, Tag.objects.all())), 'action': action})


@login_required()
def collaborator_invitation(request, profile_id=None, project_id=None, status=None):
    try:
        this_project = Project.objects.get(id=project_id)
        contributor_profile = Profile.objects.get(id=profile_id)
        contribution = ProjectContributor.objects.filter(project=this_project, contributor=contributor_profile)
        if contribution.first().status != 'pending':
            messages.warning(request, 'Collaboration expired.')
        else:
            messages.success(request, 'Collaboration updated!')
            contribution.update(status=status)
    except ObjectDoesNotExist as o:
        print o
    return HttpResponseRedirect('/profile/project/%s/detail' % this_project.id)
