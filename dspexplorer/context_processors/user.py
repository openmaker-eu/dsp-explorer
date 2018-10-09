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
        },
        'bookmarks': {},
    }

    if request.user.is_authenticated:
        context['json_user'] = UserSerializer(request.user).data
        profile = request.user.profile

        request.user.profile.crm_id is None and request.user.profile.get_crm_id_and_save()

        context['bookmarks'] = {
            'news': len(profile.get_interests('news')),
            'events': len(profile.get_interests('events')),
            'projects': len(profile.get_interests('projects')) + len(profile.get_interests('challenges')),
        }

    return context
