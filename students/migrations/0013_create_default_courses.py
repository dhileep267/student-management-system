
from django.db import migrations


def create_courses(apps, schema_editor):

    Course = apps.get_model("students", "Course")

    Course.objects.get_or_create(
        name="BSc AI/ML",
        defaults={
            "description": "Bachelor of Science in Artificial Intelligence and Machine Learning",
            "duration": "3 Years",
        },
    )

    Course.objects.get_or_create(
        name="BCA",
        defaults={
            "description": "Bachelor of Computer Applications",
            "duration": "3 Years",
        },
    )

    Course.objects.get_or_create(
        name="BSc Data Science",
        defaults={
            "description": "Bachelor of Science in Data Science",
            "duration": "3 Years",
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0012_alter_student_course"),
    ]

    operations = [
        migrations.RunPython(create_courses),
    ]

