import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a Django superuser from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Superuser setup skipped: DJANGO_SUPERUSER_USERNAME and "
                    "DJANGO_SUPERUSER_PASSWORD are required."
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)

        changed = created
        if email and user.email != email:
            user.email = email
            changed = True

        if not user.is_staff:
            user.is_staff = True
            changed = True

        if not user.is_superuser:
            user.is_superuser = True
            changed = True

        # Re-applying the configured password makes recovery easy if it is changed
        # in Railway Variables. The password itself is never logged.
        user.set_password(password)
        changed = True

        if changed:
            user.save()

        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' {action} successfully."))
