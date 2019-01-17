import re

from django.http import HttpResponse


class AccessTokenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_api_route = re.match(r"^/api/v1/", request.path)
        return self.get_response(request)

    def process_template_response(self, request, response):
        return response
