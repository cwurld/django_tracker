import os
import codecs
import csv

from django.conf import settings

import dateutil.parser


TRACKER_DIR = os.path.join(settings.MEDIA_ROOT, 'tracker')


def read_tracker_file(the_date, exclude_anonymous=False, target_user=None):
    fname = os.path.join(TRACKER_DIR, str(the_date) + '.dat')
    if os.path.exists(fname):
        fp = codecs.open(fname, 'rb', 'utf-8')
        reader = csv.reader(fp)
        rows = []
        for row in reader:
            if exclude_anonymous and row[2] == 'anonymous':
                continue
            elif target_user and row[2] != target_user:
                continue
            else:
                rows.append(row)
        fp.close()
    else:
        rows = []
    return rows


def histogram_one_day(the_date, **kwargs):
    rows = read_tracker_file(the_date, **kwargs)
    if rows is None:
        return None

    histogram = [0]*24
    for row in rows:
        dt = dateutil.parser.parse(row[0])
        histogram[dt.hour] += 1
    return histogram
