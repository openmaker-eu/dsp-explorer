import json
import logging

logger = logging.getLogger(__name__)

from dashboard.models import User, Profile, Tag
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from connectors.insight.connector import InsightConnectorV10 as Insight


class questions(APIView):

    parser_classes = (MultiPartParser, JSONParser)
    questions = []

    def get(self, request, action=None):

        entity_name = request.query_params.get('entity_name', None)
        entity_id = request.query_params.get('entity_id', None)
        temp_id = request.query_params.get('entity_temp_id', None)
        profile_id = request.query_params.get('profile_id', None)

        print('action')
        print(action)

        if request.user.is_authenticated:
            # Request for edit profile
            action == 'profileedit' and self.edit_profile_questions(request)
            # Request for chatbot
            action == 'chatbot' and self.chatbot_question(request)
            # Feedback
            entity_name and temp_id and self.feedback_questions(request, entity_name, temp_id)
            action == 'profile' and self.profile_questions(request, profile_id)

        else:
            # Request for signup questions
            not action and self.signup_questions(request)
            # Chatbot for visitors
            action == 'chatbot' and self.visitor_questions(request)

        return Response({'questions': self.questions})

    def post(self, request, action=None):
        '''

        :param request:
        :param action:
        :return:
            200 code for success
            403 if there is an error + {'error': [Error description]}
        '''

        try:
            # Send Chatbot Feedback to Insight
            if action == 'chatbot' and request.user.is_authenticated:
                return Response(Insight.feedback(
                    temp_id=request.data.get('temp_id', None),
                    crm_id=request.user.profile.crm_id,
                    feedback=request.data.get('feedback', None),
                ))
            # Update User
            not action and self.update_user(request)

        except Exception as e:
            return Response(data={'error': 'error send feedback'}, status=403)
        return Response()

    def feedback_questions(self, request, entity_name, entity_id):
        self.questions = [] \
            if entity_name in ['challenges', 'projects'] \
            else [
                self.question('rate_entity', entity_name=entity_name, entity_id=entity_id, first_name=request.user.first_name),
                self.question('rate_bye', entity_name=entity_name, first_name=request.user.first_name)
            ]

    def visitor_questions(self, request):
        self.questions = [
            self.question('signup_proposal'),
            self.question('signup_proposal_2')
        ]

    def profile_questions(self, request, profile_id):
        try:
            crm_ids = [
                Profile.objects.filter(pk=request.user.profile.id).first().crm_id,
                Profile.objects.filter(pk=profile_id).first().crm_id
            ]

            questions = Insight.profile_questions(crm_ids)
            self.questions = {
                x['temp_id']: x.update({'feedback': [x['feedback']]}) or x
                for x in questions[0]['questions']
            }

            if crm_ids[0] != crm_ids[1]:
                for question in questions[0]['questions']:
                    question['feedback'].append('agree')

                # for question in questions[1]['questions']:
                    #     print(question)
                    #     temp_id = question['temp_id']
                    #     crm_id = questions[1]['crm_id']
                    #     print(temp_id)
                    #     if temp_id in self.questions:
                    #         self.questions[temp_id]['feedback'].append(question['feedback'])

            self.questions = [ self.map_remote_to_local_questions(q) for q in self.questions.values()]

        except Exception as e:
            print(e)


    def signup_questions(self, request):
        self.questions = [
            self.question('signup_welcome'),
            self.question('user_full_name'),
            self.question('user_gender'),
            self.question('user_birthdate'),
            self.question('user_city'),
            self.question('user_occupation'),
            self.question('activity_question'),
            self.question('user_tags'),
            self.question('user_signup_data'),
            self.question('signup_bye'),
        ]

    def chatbot_question(self, request):
        try:
            welcome = self.question('welcome', first_name=request.user.first_name)
            bye = self.question('nice_talking', first_name=request.user.first_name)

            # or '145489262'
            crm_id = request.user.profile.crm_id
            response = Insight.questions(crm_ids=[crm_id])
            if response.status_code < 205:
                res_dict = response.json()
                questions = res_dict['users'][0]['questions']
                type = res_dict['users'][0]['feedback_type']
                self.questions = [welcome] + [self.map_remote_to_local_questions(q, type) for q in questions] + [bye]
        except Exception as e:
            print(e)
            self.questions = None

    def edit_profile_questions(self, request):

        user = request.user
        profile = request.user.profile
        questions = [
            self.make('name', 'name', 'What is your name?', value=[user.first_name, user.last_name]),
            self.make('gender', 'select', 'What is your gender?',
                      options=({'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}, {'value': 'other', 'label': 'Does it matter?'})
                      ),
            self.make('occupation', 'text', 'What is your occupation?'),
            self.make('birthdate', 'date', 'What is your birthdate?',
                      max=str((datetime.datetime.now()-datetime.timedelta(days=16*365)).strftime('%Y/%m/%d')),
                      value=profile.birthdate.strftime('%Y/%m/%d'),
                      ),
            self.make('city', 'city', 'What is your city?', value={'city': profile.city, 'place': {}}),
            self.make('tags', 'multi_select', 'Choose 3 tags',
                      options=[x.name for x in Tag.objects.all()],
                      value=[x.name for x in profile.tags.all()],
                      ),
            self.make('activity-question', 'activity-question', 'What is your activity?',
                      value={
                          "domain": profile.domain and profile.domain.split(",") ,
                          "area": profile.area and profile.area.split(","),
                          "technology": profile.technology and profile.technology.split(","),
                          "skills": profile.technology and profile.skills.split(",")
                      }
                      ),
            self.make('statement', 'textarea', 'Short description about you (optional)'),
            self.make('picture', 'imageupload', 'Upload you profile image (optional)',
                      value=profile.picture.url if profile.picture else None,
                      apicall='/api/v1.4/questions/',
                      emitevent='entity.change.all'
                      ),
        ]

        # Add Values
        for question in questions:
            question['value'] = question.get('value', None) \
                                or getattr(profile, question['name'], None) \
                                or getattr(user, question['name'], None)

        self.questions = questions + [self.make('edit_end', 'success', 'Profile updated'), ]

    def map_remote_to_local_questions(self, question, feedback_type='disagree_notsure_agree'):
        if feedback_type == 'disagree_notsure_agree':
            question['actions'] = {
                'type': 'buttons',
                'options': ['agree', 'disagree', 'notsure']
            }
            return self.make(name='', type='question', **question)

    def update_user(self, request):
        user = request.user
        profile = request.user.profile

        try:
            # User
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)

            # Profile
            profile.city = request.data.get('city', profile.city)
            profile.place = json.loads(request.data.get('place', profile.place))
            profile.birthdate = request.data.get('birthdate', profile.birthdate)
            profile.occupation = request.data.get('occupation', profile.occupation)
            profile.statement = request.data.get('statement', profile.statement)

            # Activity
            profile.domain = request.data.get('domain', profile.domain)
            profile.area = request.data.get('area', profile.area)
            profile.technology = request.data.get('technology', profile.technology)
            profile.skills = request.data.get('skills', profile.skills)

            # Profile Extra
            profile.tags_create_or_update(request.data.get('tags', None), clear=True)
            profile.picture_set_or_update(request.data.get('picture', None))

            user.save()
            profile.save()

        except Exception as error:
            return Response(data={'error': error}, status=403)

    @classmethod
    def question(cls, question, **kwargs):
        from dashboard.models import EntityProxy

        first_name = kwargs.get('first_name', '')
        entity_id = kwargs.get('entity_id', '')
        entity_name = kwargs.get('entity_name', '')

        static_questions = {
            'welcome': {
                'type': "question",
                'question': 'Hi, '+first_name+'!',
                'text': "Do you have time for some questions?",
                'actions': {'options': [{'label': 'yes, sure!'},  {'value': 'goto:last', 'label': 'no, thanks'}]}
            },
            'nice_talking': {
                'type': "question",
                'question': "Nice talking "+first_name+"!",
                'text': "Have a nice day",
                'actions': {'options': ['  Bye!  ']}
            },
            'rate_entity': {
                "type": 'question',
                "temp_id": entity_id,
                "super_text": "Hi! " + first_name + "",
                "question": "Do you like the " + EntityProxy.singular_name(entity_name) + " on this page?",
                "text": "Click on the stars to rate from 1 to 5",
                "actions": {'type': 'stars', 'amount': 5}
            },
            'rate_bye': {
                'type': "question",
                'question': 'Thank you!, '+first_name+'!',
                'text': "Now i will be able to show you more interesting " + entity_name,
                'actions': {'options': ['  Tank you!  ']}
            },
            'signup_proposal': {
                'type': "question",
                'question': 'Hi visitor!',
                'text': "Do you know that signed users have access to more content than you?",
                'actions': {'options': ['Tel me more',  {'value': 'event:chatbot.close', 'label': 'I dont mind'}]}
            },
            'signup_proposal_2': {
                'type': "question",
                "super text": 'You can view only 5 contents per day',
                'question': 'If you signup you will have full access to the site contents.' ,
                'text': "Do you Want to signup?",
                'actions': {'options': [{'value': 'event:question.modal.open', 'label': 'Yes'}, 'Not now' ]}
            },
        }

        form_questions = {
            'signup_welcome': cls.make('signup_welcome', 'message', 'Signup', value='Signup to Openmaker Explorer'),
            'user_full_name': cls.make('name', 'name', 'Who are you?'),
            'user_gender': cls.make('gender', 'select', 'What is your gender?',
                 options=({'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}, {'value': 'other', 'label': 'Does it matter?'})
            ),
            'user_birthdate': cls.make('birthdate', 'date', 'What is your birthdate?',
                 max=str((datetime.datetime.now()-datetime.timedelta(days=16*365)).strftime('%Y/%m/%d'))
            ),
            'user_city': cls.make('city', 'city', 'What is your city?'),
            'user_occupation': cls.make('occupation', 'text', 'What is your occupation?'),
            'activity_question': cls.make('activity_question', 'activity-question', 'What is your activity?'),
            'user_tags': cls.make('tags', 'multi_select', 'Choose 3 tags', options=[x.name for x in Tag.objects.all()]),
            'user_signup_data': cls.make('signup', 'signup', 'Your login information', apicall='/api/v1.4/signup/'),
            'signup_bye': cls.make('signup_end', 'success', 'Thank you', value='Check your inbox for a confirmation email'),
        }

        return static_questions.get(question, None) or form_questions.get(question, None)

    @classmethod
    def make(cls, name, type, label='', **kwargs):
        question = {'name': name, 'type': type, 'label': label}
        for key, arg in kwargs.items():
            question[key] = arg
        return question
