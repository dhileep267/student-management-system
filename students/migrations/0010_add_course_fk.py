from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0008_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="course_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="students_temp",
                to="students.course",
            ),
        ),
    ]

