from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from academic.models.common.Organization import Organization
from academic.serializers.common.Organization import OrganizationSerializer
from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
from django.db.models import Q

class OrganizationMVS(AllMVS):
    queryset = Organization.objects.select_related('parent').all()
    serializer_class = OrganizationSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update',
        'educational_hierarchy', 'educational_governorates', 'educational_directorates'
    ]
    filterset_fields = {
        'institution_type': ['exact'],
        'is_active': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()
        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        gov_raw = self.request.query_params.getlist('governorate') or [self.request.query_params.get('governorate') or self.request.query_params.get('governorate_id') or '']
        gov_ids = [int(p.strip()) for item in gov_raw for p in str(item).split(',') if p.strip().isdigit()]

        dir_raw = self.request.query_params.getlist('directorate') or [self.request.query_params.get('directorate') or self.request.query_params.get('directorate_id') or '']
        dir_ids = [int(p.strip()) for item in dir_raw for p in str(item).split(',') if p.strip().isdigit()]

        # قاعدة النظام الصارمة: عدم عرض المؤسسات إلا بعد الفلترة الجغرافية/الهيكلية
        effective_inst_type = inst_type or 'school'
        if effective_inst_type == 'school':
            if not gov_ids or not dir_ids:
                return qs.none()
        elif effective_inst_type in ['university', 'institute']:
            if not gov_ids:
                return qs.none()
        elif not gov_ids:
            return qs.none()

        if gov_ids or dir_ids:
            try:
                from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
                from django.db.models import Q
                core_qs = CoreOrg.objects.filter(is_deleted=False)
                if gov_ids:
                    g_q = Q(fk_governorate_id__in=gov_ids)
                    for g_int in gov_ids:
                        gov_org = CoreOrg.objects.filter(id=g_int).first()
                        cur_g_q = (
                            Q(fk_parent_organization__fk_parent_organization_id=g_int) |
                            Q(fk_parent_organization_id=g_int) |
                            Q(id=g_int)
                        )
                        if gov_org and getattr(gov_org, 'fk_governorate_id', None):
                            cur_g_q |= Q(fk_governorate_id=gov_org.fk_governorate_id)
                        g_q |= cur_g_q
                    core_qs = core_qs.filter(g_q)

                if dir_ids:
                    d_q = Q(fk_directorate_id__in=dir_ids)
                    for d_int in dir_ids:
                        dir_org = CoreOrg.objects.filter(id=d_int).first()
                        cur_d_q = Q(fk_parent_organization_id=d_int) | Q(id=d_int)
                        if dir_org and getattr(dir_org, 'fk_directorate_id', None):
                            cur_d_q |= Q(fk_directorate_id=dir_org.fk_directorate_id)
                        d_q |= cur_d_q
                    core_qs = core_qs.filter(d_q)

                matching_names = list(core_qs.values_list('name_ar', flat=True))
                if matching_names:
                    qs = qs.filter(name_ar__in=matching_names)
                else:
                    qs = qs.none()
            except Exception:
                pass

        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        return qs.order_by('name_ar')

    @action(detail=False, methods=['get'], url_path='educational-hierarchy', permission_classes=[AllowAny])
    def educational_hierarchy(self, request):
        """
        جلب هيكلية المؤسسات التعليمية (20=وزارة، 30=مكاتب محافظات، 40=إدارات مديريات، 50=مدارس)
        وفق جدول المؤسسات OpenSoftCoreV41.common.models.Branch.Organization
        """
        orgs = CoreOrg.objects.filter(is_deleted=False).values(
            'id', 'name_ar', 'name_en', 'company_level', 'branch_no', 'fk_parent_organization_id'
        ).order_by('company_level', 'branch_no', 'id')

        data = [
            {
                "id": o['id'],
                "name": o['name_ar'],
                "name_ar": o['name_ar'],
                "name_en": o['name_en'] or o['name_ar'],
                "company_level": o['company_level'],
                "branch_no": o['branch_no'],
                "fk_parent_organization": o['fk_parent_organization_id'],
            }
            for o in orgs
        ]
        return Response({
            "success": True,
            "message": "✅ تم جلب هيكلية المؤسسات التعليمية بنجاح",
            "data": data
        })

    @action(detail=False, methods=['get'], url_path='governorates', permission_classes=[AllowAny])
    def educational_governorates(self, request):
        """
        جلب مكاتب التربية والتعليم بالمحافظات (company_level = 30)
        """
        orgs = CoreOrg.objects.filter(is_deleted=False, company_level=30).values(
            'id', 'name_ar', 'name_en', 'company_level', 'branch_no', 'fk_parent_organization_id'
        ).order_by('branch_no', 'id')

        data = [
            {
                "id": o['id'],
                "name": o['name_ar'],
                "name_ar": o['name_ar'],
                "name_en": o['name_en'] or o['name_ar'],
                "company_level": o['company_level'],
                "branch_no": o['branch_no'],
                "fk_parent_organization": o['fk_parent_organization_id'],
            }
            for o in orgs
        ]
        return Response({
            "success": True,
            "data": data
        })

    @action(detail=False, methods=['get'], url_path='directorates', permission_classes=[AllowAny])
    def educational_directorates(self, request):
        """
        جلب إدارات التربية والتعليم بالمديريات (company_level = 40) المفلترة بحسب المحافظة
        """
        gov_id = (
            request.query_params.get('governorate') or
            request.query_params.get('governorate_id') or
            request.query_params.get('fk_governorate')
        )
        qs = CoreOrg.objects.filter(is_deleted=False, company_level=40)
        if gov_id and str(gov_id).strip() not in ['__none__', 'null', 'undefined', '']:
            try:
                g_int = int(gov_id)
                qs = qs.filter(fk_parent_organization_id=g_int)
            except (ValueError, TypeError):
                pass

        orgs = qs.values(
            'id', 'name_ar', 'name_en', 'company_level', 'branch_no', 'fk_parent_organization_id'
        ).order_by('branch_no', 'id')

        data = [
            {
                "id": o['id'],
                "name": o['name_ar'],
                "name_ar": o['name_ar'],
                "name_en": o['name_en'] or o['name_ar'],
                "company_level": o['company_level'],
                "branch_no": o['branch_no'],
                "fk_parent_organization": o['fk_parent_organization_id'],
            }
            for o in orgs
        ]
        return Response({
            "success": True,
            "data": data
        })
