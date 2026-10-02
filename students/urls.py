from django.urls import path, include
from rest_framework.routers import DefaultRouter


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import StudentViewSet,RegisterView , LogoutView, DashboardView,web_login,web_logout

from .views import (
    StudentViewSet,
    RegisterView,
    LogoutView,
    DashboardView,
    web_login,
    web_logout,
    student_create,
    student_update,
    student_delete,
)
router = DefaultRouter()

router.register("students", StudentViewSet, basename="student")


urlpatterns = [

   path("login/", web_login, name="web_login"),
path("web-logout/", web_logout, name="web_logout"),

path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
path("register/", RegisterView.as_view(), name="register"),
path("logout/", LogoutView.as_view(), name="logout"),
path("dashboard/", DashboardView.as_view(), name="dashboard"),
path("create/", student_create, name="student_create"),
path("update/<int:pk>/", student_update, name="student_update"),
path("delete/<int:pk>/", student_delete, name="student_delete"),
]