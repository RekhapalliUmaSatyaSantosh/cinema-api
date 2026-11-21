import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial API superuser if one does not exist."

    def handle(self, *args, **options):
        User = get_user_model()

        # Never replace or reset an existing superuser.
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("A superuser already exists. Skipping.")
            return

        username = os.environ.get("BOOTSTRAP_ADMIN_USERNAME")
        email = os.environ.get("BOOTSTRAP_ADMIN_EMAIL", "")
        password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError(
                "Bootstrap admin credentials are missing from environment."
            )

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("Initial superuser created successfully.")
        )