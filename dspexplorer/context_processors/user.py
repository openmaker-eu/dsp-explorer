from ..site_helpers import User
from dashboard.serializer import UserSerializer

def authorization(request):
    '''
    Define user page level authorization(@TODO: EX badge system)
    :param request:
    :return: authorization dictionary
    '''

    context = {
        'om_authorization': User.authorization(request),
        'page_info': {
            'name': request.resolver_match.url_name,
            'options': request.resolver_match.kwargs
        }
    }
    if request.user.is_authenticated:
        context['json_user'] = UserSerializer(request.user).data
        request.user.profile.get_crm_id_and_save()

    return context
