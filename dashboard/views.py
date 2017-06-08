from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from utils.mailer import EmailHelper
from utils.hasher import HashHelper
from dspconnector.connector import DSPConnector, DSPConnectorException
from .models import Profile, Invitation, Feedback
from .exceptions import EmailAlreadyUsed, UserAlreadyInvited
from django.http import HttpResponseRedirect
from form import FeedbackForm


@login_required()
def dashboard(request):
    try:
        context = {'themes': DSPConnector.get_themes()}
    except DSPConnectorException as e:
        context = {'themes': []}
        messages.error(request, e.message)
    return render(request, 'dashboard/dashboard.html', context)


@login_required()
def theme(request, theme_name):
    try:
        themes = DSPConnector.get_themes()
        themes_list = [t.get('name', '') for t in themes.get('themes', []) if t.get('name', '') != theme_name]
    except DSPConnectorException as e:
        messages.error(request, e.message)
        themes_list = {}

    context = {'theme_name': theme_name,
               'themes': themes_list}
    return render(request, 'dashboard/theme.html', context)


@login_required()
def profile(request, profile_id=None):
    try:
        if profile_id:
            user_profile = Profile.get_by_id(profile_id)
        else:
            user_profile = Profile.get_by_email(request.user.email)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    context = {'profile': user_profile}
    return render(request, 'dashboard/profile.html', context)


@login_required()
def search_members(request):
    return render(request, 'dashboard/search_members.html', {})


def privacy(request):
    return render(request, 'dashboard/privacy.html', {})


@login_required()
def invite(request):
    if request.method == 'POST':
        try:
            address = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
        except KeyError:
            messages.error(request, 'Please all the fields are required!')
            return HttpResponseRedirect(reverse('dashboard:invite'))

        try:
            User.objects.get(email=address)
            messages.error(request, 'User is already a DSP member!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except User.DoesNotExist:
            pass

        try:
            Invitation.objects.get(receiver_email=HashHelper.md5_hash(address))
            messages.error(request, 'User is been already invited!')
            return HttpResponseRedirect(reverse('dashboard:invite'))
        except Invitation.DoesNotExist:
            pass

        # email not present, filling invitation model
        try:

            invitation = Invitation.create(user=request.user,
                                           sender_email=request.user.email,
                                           sender_first_name=request.user.first_name,
                                           sender_last_name=request.user.last_name,
                                           receiver_first_name=first_name,
                                           receiver_last_name=last_name,
                                           receiver_email=address,

                                           )
            subject = 'You are invited to join the OpenMaker community!'
            # TODO FIX MESSAGGIO + CONTROLLI AGGIUNTI
            content = '''
            Hi <strong>{} {}</strong>,
            you have been nominated by <strong>{} {}</strong> as an influencer in the current 4th Industrial Revolution.<br><br>

            We are building a community of people eager to drive radical change in our society, making the most of talent, knowledge and capacity to reshape production according to democratic, inclusivity and sustainability principles.<br>
            We believe in innovation centered on people, and in technology as an enabler of empowered creativity and action for individuals.<br><br>

            We are confident in the ability of open collaboration to tackle complex societal challenges, and we push for a systemic revolution in manufacturing which is  locally focused but globally connected, micro yet massive.<br>  
            We invite you to take part to this cross-border movement. Join us and make your contribution to preserve and grow the common good.<br><br>

            Click <strong><a href="http://openmaker.eu/">HERE</a></strong> to discover more or subscribe to the NL to get the latest news from the community<br><br>
            Regards,<br>
            OpenMaker Team.
                                    '''.format(invitation.receiver_first_name, invitation.receiver_last_name, invitation.sender_first_name,
                                               invitation.sender_last_name)
            EmailHelper.send_email(
                message=content,
                subject=subject,
                receiver_email=address,
                receiver_name=''
            )
            messages.success(request, 'Invitation sent!')
        except EmailAlreadyUsed:
            messages.error(request, 'User is already a member!')
        except UserAlreadyInvited:
            messages.error(request, 'User has already received an invitation!')
        except Exception as e:
            print e.message
            messages.error(request, 'Please try again!')

    return render(request, 'dashboard/invite.html', {})


def support(request):
    return render(request, 'dashboard/support.html', {})


def terms_conditions(request):
    return render(request, 'dashboard/terms_conditions.html', {})


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


def om_confirmation(request, sender_first_name, sender_last_name, sender_email, receiver_first_name,
                    receiver_last_name, receiver_email):

    # sender
    sender_first_name = sender_first_name.decode('base64')
    sender_last_name = sender_last_name.decode('base64')
    sender_email = sender_email.decode('base64')

    # receiver
    receiver_first_name = receiver_first_name.decode('base64')
    receiver_last_name = receiver_last_name.decode('base64')
    receiver_email = receiver_email.decode('base64')

    try:
        User.objects.get(email=receiver_email)
        messages.error(request, 'User is already a DSP member!')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    except User.DoesNotExist:
        pass

    try:
        invitation = Invitation.objects.get(sender_email=HashHelper.md5_hash(sender_email),
                                            receiver_email=HashHelper.md5_hash(receiver_email))

        if invitation.sender_verified:
            messages.error(request, 'Invitation already sent!')
        else:
            # invitation flow start
            invitation.sender_verified = True
            invitation.save()
            # sending invitation mail

            subject = 'OpenMaker Nomination done!'
            # TODO Fix HERE LINK
            # Want to join as well? click HERE to onboard and discover how you can contribute to accelerate the 4th Industrial Revolution!<br>
            content = '''
Hi {},<br><br>
nomination Confirmed!<br><br>
The nominated person is about to receive an invitation to join the OpenMaker Community!<br><br>

If you are curious about OpenMaker, check our <strong><a href="http://openmaker.eu/">Website</a></strong> and subscribe to our Newsletter to receive the latest updates from the community! <br>

Regards, 
OpenMaker Team
            '''.format(sender_first_name)

            EmailHelper.send_email(
                message=content,
                subject=subject,
                receiver_email=sender_email,
                receiver_name=''
            )

            subject = 'You are invited to join the OpenMaker community!'
            # ToDo add "Join our community here >> Onboarding" - mail content
            content = '''
Hi <strong>{} {}</strong>,
you have been nominated by <strong>{} {}</strong> as an influencer in the current 4th Industrial Revolution.<br><br>
 
We are building a community of people eager to drive radical change in our society, making the most of talent, knowledge and capacity to reshape production according to democratic, inclusivity and sustainability principles.<br>
We believe in innovation centered on people, and in technology as an enabler of empowered creativity and action for individuals.<br><br>
 
We are confident in the ability of open collaboration to tackle complex societal challenges, and we push for a systemic revolution in manufacturing which is  locally focused but globally connected, micro yet massive.<br>  
We invite you to take part to this cross-border movement. Join us and make your contribution to preserve and grow the common good.<br><br>
 
Click <strong><a href="http://openmaker.eu/">HERE</a></strong> to discover more or subscribe to the NL to get the latest news from the community<br><br>
Regards,<br>
OpenMaker Team.
                        '''.format(receiver_first_name,receiver_last_name,sender_first_name,sender_last_name)

            EmailHelper.send_email(
                message=content,
                subject=subject,
                receiver_email=receiver_email,
                receiver_name=''
            )
            messages.success(request, 'Invitation complete!')

    except Invitation.DoesNotExist:
        messages.error(request, 'Invitation does not exist')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))
