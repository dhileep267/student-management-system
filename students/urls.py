from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    StudentViewSet,
    RegisterView,
    LogoutView,
    DashboardView,
    web_login,
    web_logout,
    web_dashboard,
    staff_login,
    student_login,
    student_dashboard,
    student_create,
    student_update,
    student_delete,
    attendance_page,
    student_attendance,
)


router = DefaultRouter()

router.register(
    "students",
    StudentViewSet,
    basename="student"
)


urlpatterns = [
    path("", include(router.urls)),

    # Student CRUD
    path(
        "create/",
        student_create,
        name="student_create"
    ),

    path(
        "update/<int:pk>/",
        student_update,
        name="student_update"
    ),

    path(
        "delete/<int:pk>/",
        student_delete,
        name="student_delete"
    ),

    # JWT
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # API authentication
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),

    # API dashboard
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard"
    ),

    # Web login
    path(
        "login/",
        web_login,
        name="web_login"
    ),

    path(
        "staff-login/",
        staff_login,
        name="staff_login"
    ),

    path(
        "student-login/",
        student_login,
        name="student_login"
    ),

    # Student dashboard
    path(
        "student-dashboard/",
        student_dashboard,
        name="student_dashboard"
    ),

    # Attendance
    path(
        "attendance/",
        attendance_page,
        name="attendance"
    ),

    # Web logout
    path(
        "web-logout/",
        web_logout,
        name="web_logout"
    ),
    path(
    "student-attendance/",
    student_attendance,
    name="student_attendance"
),
]