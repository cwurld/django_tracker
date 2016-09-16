import os
import codecs
import csv

from django.conf import settings
from django.utils import timezone


# noinspection PyMethodMayBeStatic
class TrackerManager(object):
    def process_request(self, request):
        # Exclude super users
        if request.user.is_superuser:
            return

        # Exclude some files based on the file ext
        root, ext = os.path.splitext(request.path)
        ext_list = ['.css', '.jpg', '.gif', '.png', '.js', '.ico']
        if ext in ext_list:
            return

        # Exclude some files based on url
        url_excludes = [r'/tracker', ]
        for x in url_excludes:
            if x in request.path:
                return

        # Ignore ajax interactions
        if 'xhr' in request.GET:
            return

        tracker_dir = os.path.join(settings.MEDIA_ROOT, 'tracker')
        if not os.path.exists(tracker_dir):
            os.mkdir(tracker_dir)

        # Get IP address
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            # For shared server on Webfaction. Based on http://djangosnippets.org/snippets/1706/
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        else:
            ip = request.META['REMOTE_ADDR']

        if request.user.is_anonymous():
            user = 'anonymous'
        else:
            user = request.user.email or request.user.username

        now = timezone.localtime(timezone.now())
        fname = os.path.join(tracker_dir, str(now.date()) + '.dat')
        fp = codecs.open(fname, 'ab', 'utf-8')
        writer = csv.writer(fp)
        writer.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), request.path, user, ip])
        fp.close()
