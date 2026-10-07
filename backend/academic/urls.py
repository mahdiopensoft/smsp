"""
نظام توجيه مسارات التطبيق الأكاديمي (Modular Academic URLs)
يجمع المسارات من الوحدات الفرعية المنظمة:
1. urls_common: المسارات العامة والمشتركة وتقارير المناهج
2. urls_schools: مسارات المدارس والتعليم العام
3. urls_universities: مسارات الجامعات والكليات والمقررات الأكاديمية
4. urls_institutes: مسارات المعاهد ومراكز التدريب المهني (مجهزة للمستقبل)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from academic.urls_common import router_common
from academic.urls_schools import router_schools
from academic.urls_universities import router_universities
from academic.urls_institutes import router_institutes

router = DefaultRouter()

# دمج كافة المسارات الفرعية في الراوتر الرئيسي لضمان التوافقية بنسبة 100%
router.registry.extend(router_common.registry)
router.registry.extend(router_schools.registry)
router.registry.extend(router_universities.registry)
router.registry.extend(router_institutes.registry)

urlpatterns = [
    path('', include(router.urls)),
]
