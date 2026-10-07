from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from portals.coordination_acceptance.models.College import College
from portals.coordination_acceptance.models.Institution import Institution
from portals.coordination_acceptance.models.Section import Section
from config.levels import CompanyLevel
from portals.coordination_acceptance.models.Major import Major
from utils.BranchMixinQuerset import BranchViewSetMixin
from OpenSoftCoreV41.utils.helpers.utils.requires import require_field,require_instance
from OpenSoftCoreV41.utils.helpers.exceptions.response_handler import ResponseHandler
from OpenSoftCoreV41.common.models.Branch import Organization
from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from OpenSoftCoreV41.utils.helpers.exceptions.decorators import handle_exceptions
from OpenSoftCoreV41.screens.choices import TypeOfMainSystemChoices
from rest_framework.permissions import IsAuthenticated
from portals.students.models.student import Student
from portals.students.serializers.StudentSerializer import StudentSerializer
from utils.util import choices_to_case

class GeneralMVS(BranchViewSetMixin, AllMVS):
    queryset = Student.objects.select_related()
    serializer_class = StudentSerializer
    branch_field = 'fk_user__user_organizations__fk_organization'
    permission_classes = [IsAuthenticated]


    @handle_exceptions
    @action(detail=False,methods=['get'],url_path="organizations")
    def organizations(self,request):
        results = Institution.objects.filter(
            fk_branch__company_level=CompanyLevel.COMPANY,
            source_system=request.user.source_system
        ).exclude(fk_branch=request.user.fk_organization.id).values('id','fk_branch__name_ar','fk_branch__id', 'external_id')

        return ResponseHandler.success(data=results)

