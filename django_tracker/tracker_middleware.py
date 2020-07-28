import os
import codecs
import csv

from django.conf import settings
from django.utils import timezone


# noinspection PyMethodMayBeStatic
class TrackerManager:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 302:
            return response

        # Exclude super users
        if request.user.is_superuser:
            return response

        # Exclude some files based on the file ext
        root, ext = os.path.splitext(request.path)
        ext_list = ['.css', '.jpg', '.gif', '.png', '.js', '.ico']
        if ext in ext_list:
            return response

        # Exclude some files based on url
        url_excludes = [r'/django_tracker', ]
        for x in url_excludes:
            if x in request.path:
                return response

        # Ignore ajax interactions
        if 'xhr' in request.GET:
            return response

        tracker_dir = os.path.join(settings.MEDIA_ROOT, 'tracker')
        if not os.path.exists(tracker_dir):
            os.mkdir(tracker_dir)

        # Get IP address
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            # For shared server on Webfaction. Based on http://djangosnippets.org/snippets/1706/
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        else:
            ip = request.META['REMOTE_ADDR']

        if request.user.is_anonymous:
            user = 'anonymous'
        else:
            user = request.user.email or request.user.username

        now = timezone.localtime(timezone.now())
        file_path = os.path.join(tracker_dir, str(now.date()) + '.dat')
        fp = codecs.open(file_path, 'ab', 'utf-8')
        writer = csv.writer(fp)
        writer.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), request.path, user, ip])
        fp.close()

        return response
