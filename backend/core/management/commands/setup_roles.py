from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

ROLE_RULES = {
    'Owner': {'all': True},
    'Manager': {
        'catalog': 'all', 'quotes': 'all', 'orders': 'all', 'production': 'all',
        'finance': {'view', 'add', 'change'}, 'core': {'view', 'add', 'change'},
    },
    'Designer': {
        'catalog': {'view'}, 'quotes': {'view', 'change'}, 'orders': {'view'},
        'production': {'view'}, 'core': {'view'},
    },
    'Production': {
        'catalog': {'view'}, 'quotes': {'view'}, 'orders': {'view', 'change'},
        'production': 'all', 'core': {'view'},
    },
    'Accounts': {
        'catalog': {'view'}, 'quotes': {'view'}, 'orders': {'view', 'change'},
        'finance': 'all', 'core': {'view'},
    },
    'Delivery': {
        'catalog': {'view'}, 'orders': {'view', 'change'}, 'production': {'view'},
        'core': {'view'},
    },
}

class Command(BaseCommand):
    help = 'Create/update RANL PRINT staff roles and their Django permissions.'

    def handle(self, *args, **options):
        all_perms = Permission.objects.select_related('content_type').all()
        for role, rules in ROLE_RULES.items():
            group, _ = Group.objects.get_or_create(name=role)
            group.permissions.clear()
            if rules.get('all'):
                group.permissions.set(all_perms)
            else:
                selected = []
                for app_label, actions in rules.items():
                    actions = set(actions) if actions != 'all' else {'view', 'add', 'change', 'delete'}
                    for perm in all_perms:
                        if perm.content_type.app_label != app_label:
                            continue
                        action = perm.codename.split('_', 1)[0]
                        if action in actions:
                            selected.append(perm)
                group.permissions.set(selected)
            self.stdout.write(self.style.SUCCESS(f'{role}: {group.permissions.count()} permissions'))
        self.stdout.write(self.style.SUCCESS('RANL PRINT roles are ready. Assign users to Groups in Django Admin → Users.'))
