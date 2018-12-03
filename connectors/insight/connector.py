import requests
from django.conf import settings
from urllib.parse import urlencode

class InsightConnectorV10(object):

    @classmethod
    def questions(cls, crm_ids, amount=1):
        crm_ids = cls.merge_ids(crm_ids)
        res = cls.get('recommendation/questions', {"crm_ids": crm_ids, 'count': amount})
        #print(res.json())
        return res

    @classmethod
    def feedback(cls, crm_id, temp_id, feedback):
        return cls.get('feedback/send_feedback', {'crm_id': crm_id, 'temp_id': temp_id, 'feedback': feedback})

    @classmethod
    def question_feedback(cls, crm_id, question_id, answer_id):
        context = {'crm_id': crm_id, 'question_id': question_id, 'answer_id': answer_id}
        response = cls.get('feedback/question', context)
        return response

    @classmethod
    def question_contents(cls, question_ids):
        question_ids = cls.merge_ids(question_ids)
        return cls.get('recommendation/get_questions_contents', {'question_ids': question_ids})

    @classmethod
    def question_privacy(cls, crm_id, question_ids, is_private):
        question_ids = cls.merge_ids(question_ids)
        is_private = 'True' if is_private else 'False'
        return cls.get('feedback/change_privacy', {'crm_id': crm_id, 'question_ids': question_ids, 'is_private': is_private})

    @classmethod
    def profile_questions(cls, crm_ids):
        '''

        :param crm_id:
        :return:
        '''

        # @TODO: this is a FAKE response since there is no user questions API available
        try:
            response = cls.get('feedback/get_feedbacks', {"crm_ids": crm_ids})
            json_decoded = response.json() if response.status_code < 205 else []
            results = json_decoded['users']
        except Exception as e:
            results = []
            print('Error get profile questions')
            print(e)
        return results

    @classmethod
    def reccomended_entity(cls, crm_id=None, entity_name=None, page=None):
        allowed_entities = ['news', 'events']
        try:
            results = {}
            if entity_name in allowed_entities:
                querydict = {k: v for (k, v) in {'crm_id': crm_id, 'page': page}.items() if v}
                results = cls.get('recommendation/'+entity_name, querydict)
            return results.json() if results.status_code < 205 else []
        except Exception as e:
            print('[ERROR : connectors.insight.connector.InsigthConnectoV10.reccomended_entity] Error get reccomended entities')
            print(e)
            return []

    @classmethod
    def reccomended_user(cls, crm_id):
        results = cls.get('recommendation/users', {'crm_ids': [crm_id]})
        return results


    @classmethod
    def entity_details(cls, entityname, temp_id):
        try:
            results = cls.get('recommendation/get_{}_contents'.format(entityname), {'temp_ids': [temp_id]})
            return results.json()['Temporary Contents'][temp_id]
        except Exception as e:
            print('[ERROR : connectors.insight.connector.InsigthConnectoV10.entity_detail] Error get reccomended entities')
            print(e)
            return []


    @classmethod
    def get(cls, endpoint, querydict={}):
        querydict['api_key'] = settings.INSIGHT_API_KEY
        querydict = '?' + urlencode(querydict, False) if querydict and len(querydict) > 0 else ''
        url = settings.INSIGHT_API + 'v1.0/' + endpoint + querydict
        try:
            return requests.get(url, timeout=15)
        except Exception as e:
            print('ERROR[insight.connector.InsightConnectorV10.get]')
            print(e)
            return False


    @classmethod
    def merge_ids(cls, ids):
        return ','.join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])+','

    @classmethod
    def notify_user_creation(cls, crm_id):
        results = cls.get('omn_crawler/post_registered_user', {'crm_id': crm_id})
        print('Notify Insight about new users: ')
        print(results)





