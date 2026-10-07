from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.common.Organization import Organization
from academic.serializers.common.Organization import OrganizationSerializer

class OrganizationMVS(AllMVS):
    queryset = Organization.objects.select_related('parent').all()
    serializer_class = OrganizationSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
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

        gov_id = self.request.query_params.get('governorate') or self.request.query_params.get('governorate_id')
        dir_id = self.request.query_params.get('directorate') or self.request.query_params.get('directorate_id')

        if gov_id or dir_id:
            try:
                from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
                core_qs = CoreOrg.objects.filter(is_deleted=False)
                if gov_id:
                    core_qs = core_qs.filter(fk_governorate_id=gov_id)
                if dir_id:
                    core_qs = core_qs.filter(fk_directorate_id=dir_id)

                matching_names = list(core_qs.values_list('name_ar', flat=True))
                if matching_names:
                    qs = qs.filter(name_ar__in=matching_names)
                else:
                    # إذا لم توجد مدارس في هذه المديرية أو المحافظة
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
