from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.AcademicYear import AcademicYear
from academic.serializers.common.AcademicYear import AcademicYearSerializer

class AcademicYearMVS(AllMVS):
    queryset = AcademicYear.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = AcademicYearSerializer
    select_serializer_fields = ['id', 'name', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_current': ['exact'],
        'hijri_year': ['exact', 'icontains'],
        'gregorian_year': ['exact', 'icontains'],
    }

    @action(detail=True, methods=['post'], url_path='set-current')
    def set_current(self, request, pk=None):
        instance = self.get_object()
        with transaction.atomic():
            AcademicYear.objects.filter(is_current=True, is_deleted=False).exclude(id=instance.id).update(is_current=False)
            instance.is_current = True
            instance.is_active = True
            instance.save()
        return Response({
            'success': True,
            'message': f"تم تفعيل العام الدراسي {instance} كعام دراسي حالي وإغلاق الأعوام الأخرى بنجاح.",
            'data': self.get_serializer(instance).data
        }, status=status.HTTP_200_OK)
