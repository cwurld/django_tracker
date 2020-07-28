from unittest import TestCase
import datetime
import os

from django_tracker.utils import read_tracker_file

from dateutil.rrule import rrule, DAILY


def get_users(tracker_dir, start_date, stop_date):
    anonymous_users = set()
    users = set()
    for dt in rrule(DAILY, dtstart=start_date, until=stop_date):
        rows = read_tracker_file(tracker_dir, dt.date(), 'all')
        for row in rows:
            if row.email == 'anonymous':
                anonymous_users.add(row.ip)
            else:
                users.add(row.email)
    anonymous_users = sorted(list(anonymous_users))
    users = sorted(list(users))
    return anonymous_users, users


class GetAnonymousUsers(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tracker_dir = os.getcwd() + '/tests/data/django_tracker'

    def test_1(self):
        start_date = datetime.date(2020, 7, 27)
        stop_date = datetime.date(2020, 7, 27)
        anonymous_users, users = get_users(self.tracker_dir, start_date, stop_date)
        self.assertEqual(['111.111.111.111', '127.0.0.1'], anonymous_users)
        self.assertEqual(['user1@test.com'], users)
        # print('done')
