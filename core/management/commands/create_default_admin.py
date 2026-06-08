import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the first superuser from ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD."

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("Superuser already exists. Skipping default admin creation."))
            return

        username = os.environ.get("ADMIN_USERNAME", "").strip()
        email = os.environ.get("ADMIN_EMAIL", "").strip()
        password = os.environ.get("ADMIN_PASSWORD", "")

        missing = [
            name
            for name, value in [
                ("ADMIN_USERNAME", username),
                ("ADMIN_EMAIL", email),
                ("ADMIN_PASSWORD", password),
            ]
            if not value
        ]
        if missing:
            raise CommandError(
                "No superuser exists and default admin environment variables are missing: "
                + ", ".join(missing)
            )

        admin = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Default superuser created: {admin.username}"))
