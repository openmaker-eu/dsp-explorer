from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from crmconnector.capsule import CRMConnector
from .models import Profile, Invitation, User
from utils.hasher import HashHelper
from utils.mailer import EmailHelper
from .exceptions import EmailAlreadyUsed
from .serializer import ProfileSerializer
from dspconnector.connector import DSPConnector, DSPConnectorException
from utils.api import *


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
        Please visit the <strong><a href="http://openmaker.eu/" target="_blank">Open Maker website for more information</a></strong>.
        '''
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
    last_twenty = Profile.objects.order_by('-user__date_joined')[:21]
    serializer = ProfileSerializer(instance=last_twenty, many=True)
    return JsonResponse({'status': 'ok',
                         'result': serializer.data}, status=200)


def get_feeds(request, theme_name, date='yesterday', cursor=-1):
    try:
        feeds = DSPConnector.get_feeds(theme_name, date, cursor)
    except DSPConnectorException:
        feeds = {}
    return JsonResponse({'status': 'ok',
                         'result': feeds}, status=200)


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


@csrf_exempt
def post_om_invitation(request):
    if request.method != 'POST':
        return not_authorized()
    try:

        sender_first_name = request.POST['sender_first_name']
        sender_last_name = request.POST['sender_last_name']
        sender_email = request.POST['sender_email']
        receiver_first_name = request.POST['receiver_first_name']
        receiver_last_name = request.POST['receiver_last_name']
        receiver_email = request.POST['receiver_email']

        if sender_first_name == '' or  sender_last_name == '' or sender_email == '' or receiver_first_name == '' or receiver_last_name == '' or receiver_email == '':
            return bad_request("Please fill al the fields")

    except KeyError:
        return bad_request("Please fill al the fields")
        
        # check if sender is already a dsp user (profile)
        # yes --> tell him to do the invitation from the dsp platform
        # no --> check if the receiver is not invited yet or if it's already a dsp user
        # already dsp user message
        # already invited --> tell sender that the receiver has been already invited
        # not already invited --> send to the sender a verification email
    
    # sender already a DSP user?
    try:
        User.objects.get(email=sender_email)
        return success("error", "You are already a DSP member, make the invitation using the DSP platform")
    except User.DoesNotExist:
        pass
    
    # receiver already a DSP user?
    try:
        User.objects.get(email=receiver_email)
        return success("error", "You are trying to invite an already DSP member")
    except User.DoesNotExist:
        pass
    
    # receiver already invited?
    try:
        Invitation.objects.get(receiver_email=HashHelper.md5_hash(receiver_email))
        return success("error", "You are trying to invite an already invited user")
    except Invitation.DoesNotExist:
        pass
    
    # send verification mail and create a invitation entry with profile None and sender_verification to False
    invitation = model_to_dict(Invitation.create(user=None,
                                                 sender_email=sender_email,
                                                 sender_first_name=sender_first_name,
                                                 sender_last_name=sender_last_name,
                                                 receiver_first_name=receiver_first_name,
                                                 receiver_last_name=receiver_last_name,
                                                 receiver_email=receiver_email,
                                                 sender_verified=False
                                                 ))
    
    activation_link = 'http://{}/om_confirmation/{}/{}/{}/{}/{}/{}'.format(
        get_current_site(request),
        sender_first_name.encode('base64'),
        sender_last_name.encode('base64'),
        sender_email.encode('base64'),
        receiver_first_name.encode('base64'),
        receiver_last_name.encode('base64'),
        receiver_email.encode('base64'))

    subject = 'OpenMaker Nomination.. almost done!'
    content = '''
Hi <strong>{}</strong>,<br>
we truly appreciate your contribution to the growth of the <strong>OpenMaker community</strong>.<br><br>
Please, click <strong><a href="{}">HERE</a></strong> to verify your e-mail and confirm your nomination.<br>
If you wish to get more information on the OpenMaker chain of nomination and on the community,<br>
contact us at: info@openmaker.eu<br><br>

If you have received this email by mistake please ignore it.<br><br>

Regards,<br>
OpenMaker Team.
'''.format(sender_first_name, activation_link)
    
    EmailHelper.send_email(
        message=content,
        subject=subject,
        receiver_email=sender_email,
        receiver_name=''
    )
    
    return success("ok", "Pending invitation added", invitation)
