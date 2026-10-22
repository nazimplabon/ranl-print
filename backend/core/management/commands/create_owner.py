from getpass import getpass
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create or reset the RANL PRINT owner/staff account interactively.'

    def add_arguments(self, parser):
        parser.add_argument('--username', default=None)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username') or input('Username: ').strip()
        if not username:
            raise CommandError('Username is required.')
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'Updating existing user: {username}')
        except User.DoesNotExist:
            user = User(username=username)
            self.stdout.write(f'Creating owner user: {username}')
        password = getpass('Password: ')
        confirm = getpass('Confirm password: ')
        if not password or password != confirm:
            raise CommandError('Passwords are empty or do not match.')
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        group, _ = Group.objects.get_or_create(name='Owner')
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS(f'Owner account ready: {username}'))
        self.stdout.write('Open http://127.0.0.1:8000/admin/ and log in with this account.')
