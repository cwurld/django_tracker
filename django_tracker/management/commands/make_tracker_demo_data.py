from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Generate demo data'

    def handle(self, *args, **options):
        group = Group.objects.create('django_tracker')

        # A user that just generates page views
        User.objects.create_user('user1', 'user1@test.com', 'test')

        # A user that generates page views and can view the tracker stats.
        user2 = User.objects.create_user('user2', 'user2@test.com', 'test')
        user2.groups.add(group)

        su = User.objects.create_user('su', 'su@test.com', 'test')
        su.is_superuser = True
        su.is_staff = True
        su.save()
