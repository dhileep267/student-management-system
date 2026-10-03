from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .forms import StudentForm
from .models import Student, Department
from .permissions import IsAdminOrReadOnly
from .serializers import StudentSerializer, RegisterSerializer



# =========================
# WEB LOGIN
# =========================
def web_login(request):
    if request.user.is_authenticated:
        logout(request)

    return render(
        request,
        "students/login.html"
    )

def staff_login(request):
    if request.user.is_authenticated:
        return redirect("student_list")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("student_list")

        messages.error(
            request,
            "Invalid staff username or password."
        )

    return render(request, "students/staff_login.html")


def student_login(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect("student_list")

        messages.error(
            request,
            "Invalid student username or password."
        )

    return render(request, "students/student_login.html")
@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect("web_dashboard")

    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(
            request,
            "No student profile is linked to this account."
        )
        logout(request)
        return redirect("web_login")

    return render(
        request,
        "students/student_dashboard.html",
        {
            "student": student,
        }
    )
def web_register(request):
    if request.user.is_authenticated:
        return redirect("student_list")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "students/register.html")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "students/register.html")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect("student_list")

    return render(request, "students/register.html")
def web_logout(request):
    logout(request)
    return redirect("web_login")


# =========================
# STUDENT WEB PAGES
# =========================

@login_required
def student_list(request):
    query = request.GET.get("q", "").strip()
    age = request.GET.get("age", "").strip()

    if request.user.is_staff:
        students = Student.objects.all()

        if query:
            students = students.filter(
                name__icontains=query
            )

        if age:
            students = students.filter(
                age=age
            )

    else:
        try:
            students = Student.objects.filter(
                user=request.user
            )
        except Exception:
            students = Student.objects.none()

    paginator = Paginator(students, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "students/list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "age": age,
        },
    )

@login_required
def student_create(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "Only staff members can add students."
        )
        return redirect("student_list")

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student added successfully."
            )

            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/form.html",
        {"form": form}
    )


@login_required
def student_update(request, pk):
    if not request.user.is_staff:
        messages.error(
            request,
            "Only staff members can edit students."
        )
        return redirect("student_list")

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("student_list")

    else:
        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/form.html",
        {
            "form": form,
            "student": student,
        }
    )


@login_required
def student_delete(request, pk):
    if not request.user.is_staff:
        messages.error(
            request,
            "Only staff members can delete students."
        )
        return redirect("student_list")

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":
        student.delete()

        messages.success(
            request,
            "Student deleted successfully."
        )

    return redirect("student_list")

# =========================
# DRF STUDENT API
# =========================

class StudentViewSet(viewsets.ModelViewSet):

    serializer_class = StudentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrReadOnly,
    ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Student.objects.all()

        return Student.objects.filter(
            user=self.request.user
        )

# =========================
# API REGISTER
# =========================

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# =========================
# API LOGOUT
# =========================

@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {
                    "type": "string"
                }
            },
            "required": ["refresh"],
        }
    },
    responses={
        200: OpenApiResponse(
            description="Successfully logged out"
        ),
        400: OpenApiResponse(
            description="Invalid or missing refresh token"
        ),
    },
)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "error": "Refresh token is required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "message": "Successfully logged out"
                },
                status=status.HTTP_200_OK,
            )

        except TokenError as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# =========================
# DASHBOARD API
# =========================

@extend_schema(
    responses={
        200: OpenApiResponse(
            description="Dashboard statistics"
        )
    }
)
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_students = Student.objects.count()

        total_departments = Department.objects.count()

        average_age = Student.objects.aggregate(
            average_age=Avg("age")
        )["average_age"]

        students_per_department = (
            Department.objects.annotate(
                student_count=Count("students")
            )
        )

        department_data = {}

        for department in students_per_department:
            department_data[department.name] = department.student_count

        students_per_course = (
            Student.objects
            .values("course")
            .annotate(student_count=Count("id"))
        )

        course_data = {}

        for course in students_per_course:
            course_data[course["course"]] = course["student_count"]

        return Response(
            {
                "total_students": total_students,
                "total_departments": total_departments,
                "average_age": (
                    round(average_age, 2)
                    if average_age
                    else 0
                ),
                "students_per_department": department_data,
                "students_per_course": course_data,
            }
        )

@login_required
def web_dashboard(request):

    # =========================
    # BASIC STATISTICS
    # =========================

    total_students = Student.objects.count()

    total_departments = Department.objects.count()

    average_age = Student.objects.aggregate(
        average_age=Avg("age")
    )["average_age"]


    # =========================
    # STUDENTS PER DEPARTMENT
    # =========================

    students_per_department = list(
        Department.objects
        .annotate(student_count=Count("students"))
        .values("name", "student_count")
    )


    # =========================
    # STUDENTS PER COURSE
    # =========================

    students_per_course = list(
        Student.objects
        .values("course")
        .annotate(student_count=Count("id"))
    )


    # =========================
    # RECENT STUDENTS
    # =========================

    recent_students = Student.objects.order_by(
        "-created_at"
    )[:5]


    # =========================
    # SEND DATA TO TEMPLATE
    # =========================

    return render(
        request,
        "dashboard.html",
        {
            "total_students": total_students,

            "total_departments": total_departments,

            "average_age": (
                round(average_age, 2)
                if average_age
                else 0
            ),

            "students_per_department": students_per_department,

            "students_per_course": students_per_course,

            "recent_students": recent_students,
        },
    )
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Attendance, Student
@login_required
def attendance_page(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "Only staff members can access attendance."
        )
        return redirect("student_dashboard")

    selected_date = request.GET.get("date") or str(date.today())

    students = Student.objects.all().order_by("id")

    attendance_records = Attendance.objects.filter(
        date=selected_date
    )

    attendance_map = {
        record.student_id: record.status
        for record in attendance_records
    }

    if request.method == "POST":
        selected_date = request.POST.get("date")

        for student in students:
            status_value = request.POST.get(
                f"status_{student.id}"
            )

            if status_value in ["Present", "Absent"]:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={
                        "status": status_value
                    }
                )

        messages.success(
            request,
            "Attendance saved successfully."
        )

        return redirect(
            f"/api/attendance/?date={selected_date}"
        )

    # Add status directly to each student
    for student in students:
        student.attendance_status = attendance_map.get(
            student.id,
            "Present"
        )

    return render(
        request,
        "students/attendance.html",
        {
            "students": students,
            "selected_date": selected_date,
        },
    )

@login_required
def student_attendance(request):
    if request.user.is_staff:
        return redirect("attendance")

    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(
            request,
            "No student profile is linked to this account."
        )
        logout(request)
        return redirect("web_login")

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by("-date")

    return render(
        request,
        "students/student_attendance.html",
        {
            "student": student,
            "attendance_records": attendance_records,
        },
    )