from django.http import *
from django.contrib.sites.shortcuts import get_current_site
from crmconnector.capsule import CRMConnector
from .models import Profile
from .exceptions import EmailAlreadyUsed
from .serializer import ProfileSerializer


def request_membership(request, email):
    """
    API Used to ask for DSP Registration
    :param request:
    :param email: Email of the user
    :return: Json object
    """
    party = CRMConnector.search_party_by_email(email)
    if not party:
        message = '''User not found! To become a DSP member you need to fill the onboarding form.
        Please visit the Open Maker website for more information.'''
        return JsonResponse({'status': 'error', 'message': message}, status=404)
    try:
        profile = Profile.create(email, party.get('firstName').encode('ascii', 'ignore').decode('ascii'),
                                 party.get('lastName').encode('ascii', 'ignore').decode('ascii'),
                                 party.get('pictureURL').encode('ascii', 'ignore').decode('ascii'))
    except EmailAlreadyUsed:
        return JsonResponse({'status': 'error', 'message': 'This user is already a DSP Member.'}, status=409)
    except KeyError:
        return JsonResponse({'status': 'error', 'message': 'Some error occures, please try again'}, status=500)
    except Exception as e:
        print e
        return JsonResponse({'status': 'error', 'message': 'Some error occures, please try again'}, status=500)
    message = 'Invitation sent!'
    subject_for_email = 'Welcome to DSP Explorer - Open Maker'
    message_for_email = '''
Hi!

You are about to enter to the OpenMaker Digital Social Platform (OpenMaker DSP).

The platform will provide you with an easy-to-read dashboard displaying the most relevant innovation trends and networks, expressed in intuitive and graphical representations.
DSP runs a machine learning that harvests online relations of makers and manufacturers within the digital environments that they already use, by tracing, measuring and assessing relations and trends.

The platform will collect and analyse the personal data that are already public on your social networks, and will trace your publicly available online activities on these channels (Twitter, Google +, Linkedin, Facebook, Instagram, Pinterest, YouTube, Instructables, Medium, Meet Up, GitHub, Slack).

Data will be collected and treated in Europe, by Bosphorus University, University of Zurich and IMT Lucca.

Click this link to create your account: http://{}/reset_password/{}'''.format(get_current_site(request), profile.reset_token)
    profile.send_email(subject_for_email, message_for_email)
    return JsonResponse({'status': 'ok', 'email': email, 'message': message}, status=200)


def search_members(request, search_string):
    result = Profile.search_members(search_string)
    serializer = ProfileSerializer(instance=result, many=True)
    return JsonResponse({'status': 'ok',
                         'search_string': search_string,
                         'result': serializer.data}, status=200)


def get_last_members(request):
    # TODO Get last 20 members
    return JsonResponse({'status': 'ok',
                         'result': []}, status=200)
