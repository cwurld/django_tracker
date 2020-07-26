from django.conf import settings
from django.http import HttpResponseRedirect

import re

# Make re patterns
URLS = tuple([re.compile(url) for url in settings.LOGIN_NOT_REQUIRED_URLS])


class RequireLoginMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        for url in URLS:
            if url.match(request.path):
                return response

        if request.user.is_anonymous:
            return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        return response
