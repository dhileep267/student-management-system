from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0010_add_course_fk"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="course",
        ),
        migrations.RenameField(
            model_name="student",
            old_name="course_fk",
            new_name="course",
        ),
    ]
