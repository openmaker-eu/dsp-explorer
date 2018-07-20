from oauth.models import TwitterProfile

class UserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        twitter_cookie = request.COOKIES.get('twitter_oauth', None)
        if request.user.is_authenticated:
            if twitter_cookie and TwitterProfile.objects.filter(profile_id=request.user.profile.id).count() > 0 :
                response.delete_cookie('twitter_oauth')

        return response
