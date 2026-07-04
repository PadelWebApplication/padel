from django.core.management.base import BaseCommand

from userauths.models import User


class Command(BaseCommand):
    help = "Create or update the local admin superuser."

    def handle(self, *args, **options):
        email = "admin@admin.com"
        password = "admin"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} superuser {email}"))
