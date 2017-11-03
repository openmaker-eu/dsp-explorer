from django.views.decorators.csrf import csrf_exempt
from utils.api import *
import requests, json

rasa_url = 'http://localhost:5000'


@csrf_exempt
def message_to_rasa_nlu(request):
    if request.method != 'POST':
        return not_authorized()
    try:
        message = request.POST['message']
    except KeyError:
        return bad_request('Message missing')

    # call to rasa NLU

    data = {'q': message}

    try:
        req = requests.post(url=rasa_url + '/parse', data=json.dumps(data))
    except Exception as e:
        print e
        return error()

    intent = req.json()['intent']['name']

    # switch case for dumb response

    return success('ok', 'response from rasa NLU', req.text)