from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        user, created = User.objects.get_or_create(
            username="dhileep"
        )

        user.is_active = True
        user.is_staff = True
        user.set_password("Dhileep@2026")
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "User dhileep CREATED successfully."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "User dhileep UPDATED successfully."
                )
            )