
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or reset the dedicated bootstrap admin account."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("BOOTSTRAP_ADMIN_USERNAME")
        email = os.environ.get("BOOTSTRAP_ADMIN_EMAIL", "")
        password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError("Bootstrap credentials are missing.")

        user = User.objects.filter(username=username).first()

        if user:
            if not user.is_superuser:
                raise CommandError(
                    "This username already belongs to a non-superuser."
                )

            user.set_password(password)
            user.email = email
            user.save()
            self.stdout.write("Bootstrap admin password updated.")
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write("Bootstrap admin account created.")
