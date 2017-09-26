from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
import ldap

class Command(BaseCommand):
    help = 'Syncs LDAP users with Django DB'

    def handle(self, *args, **options):
        l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
        #l.simple_bind_s(settings.USERS_DN)

        results = l.search_s(settings.USERS_DN, ldap.SCOPE_SUBTREE, "(cn=*)")

        total_created = 0
        total = 0

        for a,r in results:
            if 'employeeType' in r and 'Research Student' in str(r['employeeType']):
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

        self.stdout.write(self.style.SUCCESS('Found {} user(s), {} new.'.format(total, total_created)))
