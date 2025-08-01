"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from decouple import config
from rest_framework import permissions
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Get swagger setting from environment
swagger = config('SWAGGER', default=True, cast=bool)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogapp/',include('blogapp.urls')),
    path('display/',include('displayapp.urls'))
]

if swagger:
    schema_view = get_schema_view(
        openapi.Info(
            title="Dairy Backend API",
            default_version='v1',
            description="API documentation for Dairy Management System",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@example.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],  # Fixed: Use list instead of tuple
    )
    
    urlpatterns += [
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        re_path(r'^postman/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
