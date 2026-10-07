from django.urls import path, include
from rest_framework.routers import DefaultRouter

from templates_engine.apis.ExamTemplateMVS import ExamTemplateMVS
from templates_engine.apis.TemplateVersionMVS import TemplateVersionMVS

router = DefaultRouter()

router.register(r'exam-templates', ExamTemplateMVS, basename='exam-template')
router.register(r'template-versions', TemplateVersionMVS, basename='template-version')

urlpatterns = [
    path('generate-and-save/', ExamTemplateMVS.as_view({'post': 'generate_and_save'})),
    path('generate/', ExamTemplateMVS.as_view({'post': 'generate'})),
    path('configs/', ExamTemplateMVS.as_view({'get': 'list_configs'})),
    path('config/<str:config_name>/', ExamTemplateMVS.as_view({'get': 'get_config'})),
    path('<int:pk>/', ExamTemplateMVS.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('', ExamTemplateMVS.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('', include(router.urls)),
]
