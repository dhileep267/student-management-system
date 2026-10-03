from django.contrib import admin

from .models import Student, Attendance, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "age",
        "email",
        "course",
        "phone",
    )

    search_fields = (
        "name",
        "email",
        "course",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "date",
        "status",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "student__name",
        "student__email",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "duration",
    )

    search_fields = (
        "name",
    )