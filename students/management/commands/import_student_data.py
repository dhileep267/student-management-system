from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        call_command("loaddata", "students_data_utf8.json")

        self.stdout.write(
            self.style.SUCCESS(
                "Student data imported successfully."
            )
        )
        