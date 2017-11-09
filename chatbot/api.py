from django.views.decorators.csrf import csrf_exempt
from utils.api import *
import requests, json
from dspconnector.connector import DSPConnector, DSPConnectorException, DSPConnectorV12


rasa_url = 'http://localhost:5000'
# rasa_url = 'http://194.116.76.49:5000'

@csrf_exempt
def message_to_rasa_nlu(request):

    if request.method != 'POST':
        return not_authorized()
    try:
        # message = request.POST.get('message', '')
        message = request.POST['message']
    except Exception as e:
        print request.body
        return bad_request("Message missing")

    # call to rasa NLU
    data = {'q': message}
    try:
        req = requests.post(url=rasa_url + '/parse', data=json.dumps(data))
    except Exception as e:
        print e
        return error()

    # intent = req.json()['intent']['name']
    message = response(req.json())

    context = {
        'nlu': json.loads(req.text),
        'message': message
    }
    return JsonResponse(context)


def response(nlu_resp):

    resp = ''
    fallback_response = 'I dont understand'
    intent = nlu_resp['intent']['name']

    if intent == 'greet':
        resp = 'Hey there'

    elif intent == 'goodbye':
        if(float(nlu_resp['intent_ranking'][0]['confidence']) < 0.45 ):
            resp = fallback_response
        else:
            resp = 'See you soon'

    elif intent == 'search_general_information_about_open_maker':
        resp = 'Open maker is ...'

    elif intent == 'affirm':
        resp = 'Yes sure!'

    elif intent == 'search_user_by_tag':
        resp = 'Seraching user by tag...'

    elif intent == 'search_user_by_location':
        resp = 'Search user by location...'

    elif intent == 'search_news_by_theme':
        resp = 'Searching news by theme...'

    elif intent == 'search_influecers_by_theme':
        resp = "Searching influencers by theme..."

        # if( nlu_resp['entities'][0][] )
        # DSPConnectorV12.get_audiences()
        # resp = 'Open maker is ...'

    else:
        resp = fallback_response

    return resp
