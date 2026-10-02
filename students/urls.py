from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import StudentViewSet,RegisterView , LogoutView, DashboardView


router = DefaultRouter()

router.register("students", StudentViewSet, basename="student")


urlpatterns = [

    path("", include(router.urls)),

    path("token/", TokenObtainPairView.as_view(),name="token_obtain_pair"),

    path("token/refresh/", TokenRefreshView.as_view(),name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    
]