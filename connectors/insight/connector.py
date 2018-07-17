import requests
from django.conf import settings
from urllib.parse import urlencode

class InsightConnectorV10(object):

    @classmethod
    def questions(cls, crm_ids):
        print(crm_ids)
        return cls.get('recommendation/questions', {"crm_ids": crm_ids})

    @classmethod
    def feedback(cls, crm_id, temp_id, feedback):
        return cls.get('feedback/send_feedback', {'crm_id': crm_id, 'temp_id': temp_id, 'feedback': feedback})

    @classmethod
    def question_feedback(cls, crm_id, question_id, answer_id):
        return cls.get('feedback/question', {'crm_id': crm_id, 'question_id': question_id, 'answer_id': answer_id})

    @classmethod
    def profile_questions(cls, crm_ids):
        '''

        :param crm_id:
        :return:
        '''

        # @TODO: this is a FAKE response since there is no user questions API available
        try:
            response = cls.get('recommendation/questions', {"crm_ids": crm_ids})
            json_decoded = response.json() if response.status_code < 205 else []

            import random
            results = json_decoded['users']
            for user in results:
                [x.update({'feedback': random.choice(['agree', 'disagree', 'notsure'])}) for x in user['questions']]

        except Exception as e:
            results = []
            print(e)

        return results

    @classmethod
    def reccomended_entity(cls, crm_id, entity_name):
        allowed_entities = ['news', 'events']
        try:
            results = cls.get('recommendation/'+entity_name, {'crm_ids': [crm_id]}) if entity_name in allowed_entities else {}
            json_decoded = results.json() if results.status_code < 205 else []
            reccomendations = json_decoded['users'][0][entity_name]
            return reccomendations
        except Exception as e:
            print(e)
            return []

    @classmethod
    def reccomended_user(cls, crm_id):
        results = cls.get('recommendation/users', {'crm_ids': [crm_id]})
        return results


    @classmethod
    def get(cls, endpoint, querydict={}):
        querydict['api_key'] = settings.INSIGHT_API_KEY
        querydict = '?' + urlencode(querydict, False) if querydict and len(querydict) > 0 else ''
        url = settings.INSIGHT_API + 'v1.0/' + endpoint + querydict
        try:
            response = requests.get(url, params=querydict, timeout=8)
        except Exception as e:
            print(e)
        return response