from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Generate demo data'

    def handle(self, *args, **options):
        User.objects.create_user('user1', 'user1@test.com', 'test')
        User.objects.create_user('user2', 'user2@test.com', 'test')
        su = User.objects.create_user('su', 'su@test.com', 'test')
        su.is_superuser = True
        su.is_staff = True
        su.save()
