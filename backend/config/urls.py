from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView
from django.http import JsonResponse
import importlib
import pkgutil

def dynamic_choices_view(request, choice_name):
    import OpenSoftCoreV41
    # البحث عن الكلاس المطلوب في جميع ملفات choices داخل OpenSoftCoreV41
    for importer, modname, ispkg in pkgutil.walk_packages(OpenSoftCoreV41.__path__, OpenSoftCoreV41.__name__ + '.', onerror=lambda n: None):
        if modname.endswith('.choices'):
            try:
                module = importlib.import_module(modname)
                if hasattr(module, choice_name):
                    choice_class = getattr(module, choice_name)
                    choices = [
                        {
                            "id": item[0], 
                            "name": str(item[1]), 
                            "name_ar": str(item[1]), 
                            "name_en": str(item[1])
                        } 
                        for item in choice_class.choices
                    ]
                    return JsonResponse({"data": choices})
            except Exception:
                pass
    return JsonResponse({"error": "Not found"}, status=404)

schema_view = get_schema_view(
    openapi.Info(
        title="User API",
        default_version='v1',
        description="API Documentation using Swagger (OpenAPI) & Django REST Framework",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),



    # Swagger UI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('api/schema-s/',SpectacularAPIView.as_view(),name='schema'),
    path('api/schema/swagger-ui-s/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/schema/redoc-ss/',SpectacularRedocView.as_view(url_name='schema'),name='redoc'),

    path('choices/<str:choice_name>/', dynamic_choices_view),
]

from .imports.viewmodel_core import urlpatterns_core
urlpatterns += urlpatterns_core

from OpenSoftCoreV41.usermanager.apis.SecureTokenRefresh import SecureTokenRefreshView

urlpatterns += [
    path('auth/token/refresh/', SecureTokenRefreshView.as_view(), name='token_refresh_slash'),
    path('api/academic/', include('academic.urls')),
    path('api/bank/', include('bank.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/omr/', include('omr.urls')),
    path('api/submissions/', include('submissions.urls')),
    path('api/templates-engine/', include('templates_engine.urls')),
    path('api/templates/', include('templates_engine.urls')),
    path('api/common/', include('OpenSoftCoreV41.common.urls')),
]

