from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)

    course = models.CharField(
        max_length=100,
        default="BSc AI/ML"
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    address = models.TextField(
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.student.name} Profile"

class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"    
class Course(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField(
        blank=True
    )

    duration = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.name    