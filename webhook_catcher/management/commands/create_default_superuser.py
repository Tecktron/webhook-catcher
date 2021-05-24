from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Management command to create a superuser by simply providing the username/password"""

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, required=True)
        parser.add_argument("--password", type=str, required=True)

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        admin, created = User.objects.using("default").get_or_create(username=username)

        if created:
            admin.password = make_password(password)
            admin.is_superuser = True
            admin.is_staff = True
            admin.save(using="default")
            self.stdout.write(f"superuser {username} is created")
            return

        self.stdout.write(f"User {username} already exists")
