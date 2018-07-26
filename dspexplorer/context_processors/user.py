from ..site_helpers import User
from dashboard.serializer import UserSerializer
from utils.helpers import encrypt, decrypt



def authorization(request):
    '''
    Define user page level authorization(@TODO: EX badge system)
    :param request:
    :return: authorization dictionary
    '''

    twitter_cookie = request.COOKIES.get('twitter_oauth', None)

    context = {
        'om_authorization': User.authorization(request),
        'twitter_auth': twitter_cookie,
        'page_info': {
            'name': request.resolver_match.url_name,
            'options': request.resolver_match.kwargs,
            'bookmark': request.GET.get('bookmark', None)
        }
    }
    if request.user.is_authenticated:
        context['json_user'] = UserSerializer(request.user).data
        request.user.profile.get_crm_id_and_save()

    return context
