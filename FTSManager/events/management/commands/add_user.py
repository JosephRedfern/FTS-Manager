from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
import ldap

class Command(BaseCommand):
    help = 'Add a specific user from LDAP to FTS-Manager'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=str)

    def handle(self, *args, **options):
        l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
        #l.simple_bind_s(settings.USERS_DN)

        total = 0
        total_created = 0

        for user_id in options['user_id']:
            print("Looking up {}".format(user_id))
            results = l.search_s(settings.USERS_DN, ldap.SCOPE_SUBTREE, "(uid={})".format(user_id))
            for e, r in results:
                username = r['uid'][0].decode('utf-8')
                first_name = r['givenName'][0].decode('utf-8')
                last_name = r['sn'][0].decode('utf-8')
                email = r['mail'][0].decode('utf-8')
                user, created = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
                total += 1
                if created:
                    user.set_unusable_password()
                    user.save()
                    total_created += 1
                    print("Added {}".format(user_id))
                else:
                    print("{} already exists".format(user_id))

        print("Found {}/{} users, added {}".format(total, len(options['user_id']), total_created))
