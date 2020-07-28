import os
import codecs
import csv
from collections import namedtuple

import dateutil.parser

Record = namedtuple('Record', 'datetime url email ip')


def read_tracker_file(tracker_dir: str, the_date: str, target: str, exclude_anonymous: bool = False):
    """
    
    :param tracker_dir: 
    :param the_date: 
    :param target: options: all, anonymous-all, anonymous-ip, user-email
    :param exclude_anonymous: 
    :return: 
    """
    target_ip = None
    target_email = None
    if target.startswith('user'):
        target_email = target.split('-')[1]
    elif target.startswith('anonymous'):
        target_ip = target.split('-')[1]

    fname = os.path.join(tracker_dir, str(the_date) + '.dat')
    if os.path.exists(fname):
        fp = codecs.open(fname, 'rb', 'utf-8')
        reader = csv.reader(fp)
        rows = []
        for row in reader:
            r = Record(*row)

            if r.email == 'anonymous' and r.url in ['/accounts/login/', '/accounts/logout/']:
                continue

            if exclude_anonymous and r.email == 'anonymous' and target_ip != 'all':
                continue

            if (
                    (target == 'all') or
                    (target == 'anonymous-all' and r.email == 'anonymous') or
                    (target_email == r.email or target_ip == r.ip)
            ):
                rows.append(r)

        fp.close()
    else:
        rows = []
    return rows


def histogram_one_day(tracker_dir: str, the_date: str, target: str, **kwargs):
    rows = read_tracker_file(tracker_dir, the_date, target, **kwargs)
    if rows is None:
        return None

    histogram = [0]*24
    for row in rows:
        dt = dateutil.parser.parse(row.datetime)
        histogram[dt.hour] += 1
    return histogram
