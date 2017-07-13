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
from datetime import datetime
from utils.emailtemplate import invitation_base_template_header, invitation_base_template_footer, invitation_email_confirmed, invitation_email_receiver, onboarding_email_template
from crmconnector import capsule

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import logging


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


def onboarding(request):
    
    if request.method == 'POST':
        try:
            email = request.POST['email']
            pasw = request.POST['password']
            pasw_confirm = request.POST['password_confirm']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            gender = request.POST['gender']
            birthdate_dt = datetime.strptime(request.POST['birthdate'], '%Y/%m/%d')
            city = request.POST['city']
            occupation = request.POST['occupation']
            tags = request.POST['tags']
            twitter_username = request.POST.get('twitter', '')
        except ValueError:
            messages.error(request, 'Incorrect birthdate format: it must be YYYY/MM/DD')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        except KeyError:
            messages.error(request, 'Please fill the required fields!')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        
        # check password
        if pasw != pasw_confirm:
            messages.error(request, 'Password and confirm password must be the same')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        
        # Check image and get url
        try:
            file = request.FILES['profile_img']
            filename, file_extension = os.path.splitext(file.name)
            
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if not (file_extension in allowed_extensions):
                raise ValueError
            # TODO Use ABSOLUTE PATH
            imagename = str(datetime.now().microsecond) + '_' + str(file._size) + file_extension
            imagepath = '/'+default_storage.save('static/images/profile/'+imagename, ContentFile(file.read()))
        except ValueError:
            messages.error(request, 'Profile Image is not an image file')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        except:
            # # TODO Use ABSOLUTE PATH
            imagepath = 'static/user_icon.png'
        
        # Check if user exist
        try:
            User.objects.get(email=email)
            messages.error(request, 'User is already a DSP member!')
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        except User.DoesNotExist:
            pass
        
        # profile create
        try:
            profile = Profile.create(email, first_name, last_name, imagepath, pasw, gender, birthdate_dt,
                                     city, occupation, tags, twitter_username)
        except Exception as e:
            messages.error(request, 'Error creating user')
            logging.error('Error creating user: %s' % str(e))
            return HttpResponseRedirect(reverse('dashboard:onboarding'))
        
        confirmation_link = request.build_absolute_uri('/onboarding/confirmation/{TOKEN}'.format(TOKEN=profile.reset_token))
        
        # send e-mail
        subject = 'Onboarding... almost done!'
        content = "{}{}{}".format(invitation_base_template_header,
                                  onboarding_email_template.format(FIRST_NAME=first_name,
                                                                   LAST_NAME=last_name,
                                                                   CONFIRMATION_LINK=confirmation_link,
                                                                   ),
                                  invitation_base_template_footer)
        
        EmailHelper.send_email(
            message=content,
            subject=subject,
            receiver_email=email
        )
        
        messages.success(request, 'Confirmation mail sent!')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    
    return render(request, 'dashboard/onboarding.html', {})


def onboarding_confirmation(request, token):
    # Check for token
    try:
        profile = Profile.objects.get(reset_token=token)
    except Profile.DoesNotExist:
        messages.error(request, 'Token expired')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    
    #Check for user on Capsupe CRM
    user = capsule.CRMConnector.search_party_by_email(profile.user.email)
    if user:
        try:
            capsule.CRMConnector.update_party(user['id'], {'party': {
                        'emailAddresses': [{'address': profile.user.email}],
                        'type': 'person',
                        'firstName': profile.user.first_name,
                        'lastName': profile.user.last_name,
                        'jobTitle': profile.occupation,
                        'pictureURL': profile.picture_url
                    }
                })
        except:
            messages.error(request, 'Some error occures, please try again!')
            logging.error('[VALIDATION_ERROR] Error during CRM Creation for user: %s' % profile.user.id)
            # TODO SEND ERROR EMAIL TO ADMIN
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
    else:
        try:
            capsule.CRMConnector.add_party({'party': {
                    'emailAddresses': [{'address': profile.user.email}],
                    'type': 'person',
                    'firstName': profile.user.first_name,
                    'lastName': profile.user.last_name,
                    'jobTitle': profile.occupation,
                    'pictureURL': profile.picture_url
                }
            })
        except:
            messages.error(request, 'Some error occures, please try again!')
            logging.error('[VALIDATION_ERROR] Error during CRM Creation for user: %s' % profile.user.id)
            # TODO SEND ERROR EMAIL TO ADMIN
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
    profile.user.is_active = True
    profile.user.save()
    profile.update_reset_token()
    messages.success(request, 'Your account is now active. Please login with your credentials!')
    return HttpResponseRedirect(reverse('dashboard:dashboard'))


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
            # ToDo OnBoarding link
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
            content = "{}{}{}".format(invitation_base_template_header,
                                      invitation_email_confirmed,
                                      invitation_base_template_footer)
            
            
            EmailHelper.send_email(
                message=content,
                subject=subject,
                receiver_email=sender_email,
                receiver_name=''
            )
            
            subject = 'You are invited to join the OpenMaker community!'
            content = "{}{}{}".format(invitation_base_template_header,
                                      invitation_email_receiver.format(RECEIVER_FIRST_NAME=receiver_first_name,
                                                                       RECEIVER_LAST_NAME=receiver_last_name,
                                                                       SENDER_FIRST_NAME=sender_first_name,
                                                                       SENDER_LAST_NAME=sender_last_name),
                                      invitation_base_template_footer)
            
            EmailHelper.send_email(
                message=content,
                subject=subject,
                receiver_email=receiver_email,
                receiver_name=''
            )
            messages.success(request, 'Invitation complete!')
    
    except Invitation.DoesNotExist:
        messages.error(request, 'Invitation does not exist')
    return HttpResponseRedirect('http://openmaker.eu/confirmed/')
