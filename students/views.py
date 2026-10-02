from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count

from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import StudentForm
from .models import Student, Department
from .permissions import IsAdminOrReadOnly
from .serializers import StudentSerializer, RegisterSerializer


from drf_spectacular.utils import extend_schema, OpenApiResponse


# =====================================================
# NORMAL DJANGO VIEWS
# =====================================================

@login_required
def student_list(request):

    query = request.GET.get("q", "").strip()
    age = request.GET.get("age", "").strip()

    students = Student.objects.all()

    # Search
    if query:
        students = students.filter(
            name__icontains=query
        )

    # Filter
    if age:
        students = students.filter(
            age=age
        )

    # Pagination
    paginator = Paginator(students, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "students/list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "age": age
        }
    )


@login_required
def student_create(request):

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
            "You don't have permission to edit students."
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
            "student": student
        }
    )


@login_required
def student_delete(request, pk):

    if not request.user.is_staff:
        messages.error(
            request,
            "You don't have permission to delete students."
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


# =====================================================
# DRF VIEWSET
# =====================================================

class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()

    serializer_class = StudentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrReadOnly
    ]


# =====================================================
# REGISTER
# =====================================================

class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [AllowAny]


# =====================================================
# LOGOUT
# =====================================================
@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(
            description="Successfully logged out"
        ),
        400: OpenApiResponse(
            description="Invalid or missing refresh token"
        ),
    }
)
class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )

        except TokenError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# =====================================================
# DASHBOARD / STATISTICS API
# =====================================================
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

        # Total students
        total_students = Student.objects.count()

        # Total departments
        total_departments = Department.objects.count()

        # Average age
        average_age = Student.objects.aggregate(
            average_age=Avg("age")
        )["average_age"]

        # Students in each department
        students_per_department = Department.objects.annotate(
            student_count=Count("students")
        )

        department_data = {}

        for department in students_per_department:
            department_data[department.name] = department.student_count

        # Students in each course
        students_per_course = Student.objects.values(
            "course"
        ).annotate(
            student_count=Count("id")
        )

        course_data = {}

        for course in students_per_course:
            course_data[course["course"]] = course["student_count"]

        # Final response
        return Response({
            "total_students": total_students,
            "total_departments": total_departments,
            "average_age": round(average_age, 2) if average_age else 0,
            "students_per_department": department_data,
            "students_per_course": course_data
        })