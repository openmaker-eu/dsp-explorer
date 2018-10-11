import os
import sys
import django

sys.path.append("/dspexplorer/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'dspexplorer.settings'
django.setup()

from dashboard.models import User, Profile, Location, Invitation
import json
from utils.GoogleHelper import GoogleHelper
from utils.Colorizer import Colorizer

activities = {
    'domain': ['Art','Recycling','Disused Spaces','Urban Farming','Gardening','Machinary','Digital fabrication','Organic Waste','Fashion','Education','Social Service','Health','Game and Entertainment','Graphics','Textile and Clothing','Ceramics','Metal','Wood','Manufacturing General','IT','Robotics','IoT','Electronics'],
    'area': ['3D Modelling','3D printing','3D printing : BJ','3D printing : Cladding','3D printing : Concrete 3D printing','3D printing : FFF','3D printing : LOM','3D printing : Material Jetting','3D printing : Material Jetting','3D printing : Printing Material','3D printing : SLS','3D printing: SLA','Collaboration','Collaboration : Connecting','Collaboration : Content communities','Collaboration : Online Collaborative Design Platform','Collaboration : Questionnaire','Collaboration : Source Code Management','Collaboration : Team Collaboration','Collaboration: Collaborative Design','Commercialization','Commercialization : Co Design','Commercialization : Funding','Commercialization : Sales','Communication','Communication : Social Networking Sites', 'Design' ,'Design : Simulation','Design: Drag and Drop Production','Electronics','Electronics : DIY Electronics','Interaction','Interaction : 3D Interaction','Interaction : 3D Visualisation','Interaction : Display','Interaction : Input','Internet of things','Internet of things : Data analytics','Internet of things : Database','Internet of things : Visualisation','Learning','Learning : Content Communities','Milling','Modelling','Modelling : DIY Electronics','Organisation' ,'Organisation : Community Tools','Robotics','Sharing','Sharing : Blogs','Sharing : Collaborative Projects','Sharing : Content communities','Sharing : Files Repository','Sharing : Virtual Game Worlds','Sharing : Virtual Social Worlds','Software Development','Software Development : Cloud Computing','Software Development : Programming','Software Development : Team Collaboration','Telecommunication','Telecommunication : Long Range','Telecommunication : Short Range'],
    'technology': ['3D files repository', '3D modelling software', '3D printing service', '3D scanning software', '5G', 'Artificial Intelligence', 'Augmented reality', 'Blockchain Technology', 'Blog Platform', 'Bookmarking', 'Brain Computer Interface', 'Broadcasting platform', 'Business Intelligence Software', 'Cave automatic virtual environment', 'Chatbot Platform', 'Cloud Services', 'CNC - Open Source', 'CNC - Plug and Play', 'Community Discussion Forum', 'Competition Platform', 'Computer Vision', 'Crowdfunding Management', 'Customization software', 'Dataflow programming', 'Descriptive Analytics', 'Diagnostic Analytics', 'Directory', 'Distributed Computing', 'Documentation Platform', 'Domestic Robots', 'Donation Platform', 'eCommerce Website', 'Equity crowdfunding', 'Event management platform', 'FDM - Kit / DIY', 'Filament Recycling', 'Fog Computing', 'Free CAD software', 'Gamification', 'Gaming', 'Gesture Recognition', 'Graph Database', 'Grid Computing', 'Home Automation', 'IaaS', 'Image sharing platform', 'Indoor Localisation', 'Instruction platforms', 'Laser Melting Metal', 'LPWAN', 'Machine Learning', 'Maker Academies', 'Massive Open Online Course', 'Microcontroller', 'Mixed Reality', 'Nanoelectronics', 'NB-IoT', 'News Aggregation', 'News blogs', 'Online big data analytics', 'Online circuit design platform', 'Online market place', 'Online Reviews', 'Optical head-mounted display', 'Organisation search engine', 'P2P', 'P2P Lending', 'PaaS', 'Personal Networks', 'Phone AR', 'Podcast platform', 'Predictive Analytics', 'Prescriptive Analytics', 'Product Discussion Forum', 'Project Hosting platform', 'Project management platform', 'Reward crowdfunding', 'Robotic Arm', 'SaaS', 'Sensor Data Collection Platforms', 'SLS - Kit / DIY', 'SLS - Plug and Play', 'Smart Contracts', 'Smart Glasses', 'Speech Recognition', 'Survey Platform', 'Team Communication', 'Time Series Database', 'Timezone management', 'Video sharing platform', 'Virtual reality', 'Visual Programming', 'Visualisation', 'WiKi platform', 'Z-Wave', 'ZigBee'],
    'skills': ['Coding: Python', 'Coding: Processing', 'Coding: Django', 'Graphic design', 'Wood carving', 'Clay Sculpting', 'Team Management', 'Workshop Coordination', 'Budgeting', 'Marketing', 'Product design', 'Creative writing', 'Lecturing', 'Painting', 'Social entrepreneurship', 'Drawing']
}


def user_sync_template(callback=lambda x: x, args=[]):
    errored = []
    profiles = Profile.objects.filter(user__email=args[0]) \
        if len(args) > 0 \
        else Profile.objects.all()
    print(' ')
    print(Colorizer.Yellow('############ START UPDATING ###########'))
    print(' ')
    for k, profile in enumerate(profiles):
        counter = '('+str(k) + ' of ' + str(len(profiles))+')'
        results = callback(profile)
        if results is not True:
            print(Colorizer.Red(counter + 'UPDATE ERROR : ' + profile.user.email))
            [print('   '+line) for line in str(results['error']).split('\n')]
            errored.append(results)
        else:
            print(Colorizer.Cyan(counter) + '' + Colorizer.Green('User updated: ')+profile.user.email)

    print(Colorizer.Yellow(' '))
    print(Colorizer.Yellow('############### RESULTS ###############'))
    print('')
    print(Colorizer.Green(str(len(profiles)-len(errored)) + ' USERS WAS SUCCESFULLY UPDATED'))
    print(' ')
    print(Colorizer.Red(str(len(errored)) + ' USERS WITH ERRORS'))
    for error in errored:
        print('    ')
        print('    '+Colorizer.Red(error['user'].email+' - UUID: '+str(error['user'].id)))
        print('      | EXCEPTION: ')
        [print('      | '+line) for line in str(error['error']).split('\n')]
    print(Colorizer.Yellow(' '))
    print(Colorizer.Yellow('#######################################'))


def sanitize_place(user):
    try:
        if user.profile:
            user.profile.sanitize_place(force=True)
    except Exception as e:
        print(Colorizer.Red('###############################'))
        print(Colorizer.Red('sanitize place error'))
        print(Colorizer.Red(e))
        print(Colorizer.Red('###############################'))
    else:
        print(Colorizer.Green('PLACE OK: '+user.email))


def add_location_to_user(user):
    try:
        if user.profile.place:
            place = json.loads(user.profile.place)

            location = Location.create(
                lat=repr(place['lat']),
                lng=repr(place['long']),
                city=place['city'],
                state=place['state'],
                country=place['country'],
                country_short=place['country_short'],
                post_code=place['post_code'] if 'post_code' in place else '',
                city_alias=place['city']+','
            )
            user.profile.location = location
            user.profile.save()

    except Exception as e:
        print(Colorizer.Red('###############################'))
        print(Colorizer.Red('Add location error'))
        print(Colorizer.Red(e))
        print(Colorizer.Red('###############################'))
    else:
        print(Colorizer.Green('LOCATION OK: '+user.email))


def deobfuscate_invitation(user):
    try:
        Invitation.deobfuscate_email(user.email, user.first_name, user.last_name)
    except Exception as e:
        print('Error Deobfuscation')
        print(e)


def add_crm_id_to_profile(user):
    try:
        user.profile.get_crm_id_and_save()
    except Exception as e:
        print(e)


def sync_profiles(profile):
    from crmconnector.models import Party
    try:
        party = Party(profile.user)
        party.create_or_update()
        return True
    except Exception as e:
        return {'user': profile.user, 'error': e}


def update_activities(user):
    res = {
        'domain': [],
        'area': [],
        'technology': [],
        'skills': []
    }

    def update_res(tag, output):
        print(tag)
        for key in output.keys():
            if tag in activities[key]:
                print(tag)
                res[key].append(tag)

    [update_res(tag, res) for tag in user.profile.tags.all()]


