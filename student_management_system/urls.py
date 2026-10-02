from django.contrib import admin
from django.urls import path, include

from students.views import (
    student_list,
    web_login,
    web_logout,
    web_dashboard,
)

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from students.views import student_list, web_logout, web_login, web_register


urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        "admin/",
        admin.site.urls
    ),


    # =========================
    # WEB AUTHENTICATION
    # =========================

    path(
        "login/",
        web_login,
        name="web_login"
    ),

    path(
        "web-logout/",
        web_logout,
        name="web_logout"
    ),


    # =========================
    # WEB DASHBOARD
    # =========================

    path(
        "dashboard/",
        web_dashboard,
        name="web_dashboard"
    ),


    # =========================
    # STUDENT WEB PAGE
    # =========================

    path(
        "",
        student_list,
        name="student_list"
    ),


    # =========================
    # API
    # =========================

    path(
        "api/",
        include("students.urls")
    ),


    # =========================
    # API DOCUMENTATION
    # =========================

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),
    path("register/", web_register, name="web_register"),
]


# =========================
# MEDIA FILES
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )