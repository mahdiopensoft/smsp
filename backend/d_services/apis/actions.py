

from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction, models
from d_services.models.RequestAttachment import RequestAttachment
from d_services.models.RequestNote import RequestNote

from d_services.utils.exception_handler import (
    handle_exceptions,
    ValidationException,
    PermissionDeniedException,
    ResourceNotFoundException,
    LockedResourceException,
    InvalidStatusException,
    BusinessRuleException,
)
from d_services.models.RequestAction import RequestAction
from d_services.models.StagePermission import StagePermission
from d_services.models.ServiceWorkflowStep import ServiceWorkflowStep
from d_services.models.RequestReturnLog import RequestReturnLog
from d_services.serializers.requests import (
    RequestActionSerializer,
    RequestAttachmentSerializer,
    RequestNoteSerializer
)
from d_services.choices.choices import (
    ServiceStatusChoice,
    StageStatusChoice,
    ReturnReasonChoice,
    LogActionChoice,
)
from config.imports.viewmodel_core import AllMVS
from utils.BranchMixinQuerset import BranchViewSetMixin
from d_services.utils.messages import Messages
from d_services.utils.response_handler import ResponseHandler
from d_services.utils.validation_handler import ValidationHandler
from d_services.utils.logging_manager import LoggingManager
from OpenSoftCoreV41.utils.helpers.utils.requires import require_field,require_instance
from d_services.models.ServiceRequest import ServiceRequest
from d_services.choices.choices import ActionPermissionType
from d_services.choices.choices import WorkflowStageTypeChoice
from d_services.choices.choices import PaymentStatusChoice
from django.db.models import Prefetch
from d_services.models.StageChecklistItem import StageChecklistItem
from d_services.models.Service import Service
# اضافح حقل في ال خطوات 
class RequestActionMVS(BranchViewSetMixin, AllMVS):
    queryset = RequestAction.objects.select_related(
        'fk_request', 'fk_request__fk_service', 'fk_request__fk_organization',
        'fk_workflow_step', 'fk_workflow_step__fk_stage',
        'fk_started_by', 'fk_executed_by', 'fk_completed_by', 
        'fk_approved_by', 'fk_rejected_by', 'fk_moved_to_next_by'
    ).prefetch_related(
        Prefetch('checklist_items', queryset=StageChecklistItem.objects.select_related('fk_checked_by').order_by('order'))
    )
    serializer_class = RequestActionSerializer
    branch_field = 'fk_request__fk_organization'
    # enable_actions = ['all','select','list','second_list','filter','filter_paginate',]
    
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = super().get_queryset()
        
        request_id = require_field(request.query_params,'fk_request',pop=False)
        request_instance = require_instance(ServiceRequest,{"pk":request_id})
        service_instanse = require_instance(Service,{"pk":request_instance.fk_service_id})
        if not ValidationHandler.check_service_permission(user, service_instanse.id, 'READ'):
                return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض طلبات هذه الخدمة'))
        queryset = queryset.filter(fk_request_id=request_id)
        

        organization = getattr(user, 'fk_organization', None)
        queryset = queryset.filter(fk_request__fk_organization=organization)
        

        stage_status = request.query_params.get('stage_status')
        if stage_status:
            queryset = queryset.filter(stage_status=stage_status)
        

        is_current = request.query_params.get('is_current')
        if is_current and is_current.lower() == 'true':
            queryset = queryset.filter(is_current=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return ResponseHandler.success(
            message=_('تم جلب قائمة المراحل بنجاح'),
            data=serializer.data,
            extra={'count': queryset.count()}
        )
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        request_instance = require_instance(ServiceRequest,{"pk":instance.fk_request_id})
        service_instanse = require_instance(Service,{"pk":request_instance.fk_service_id})
        if not ValidationHandler.check_service_permission(user, service_instanse.id, 'READ'):
                return ResponseHandler.forbidden(_('ليس لديك صلاحية عرض طلبات هذه الخدمة'))
        serializer = self.get_serializer(instance)
        return ResponseHandler.success(
            message=_('تم جلب تفاصيل المرحلة بنجاح'),
            data=serializer.data
        )
    
   
    @action(detail=True, methods=['get'], url_path='input-data', url_name='input-data')
    @handle_exceptions
    def get_input_template_data(self, request, pk=None):

        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.INPUT)
        
        if not instance.has_custom_input:
            raise ValidationException(
                message=_('هذه المرحلة لا تحتوي على مدخل خاص'),
                hint=_('لا يوجد قالب مدخل لهذه المرحلة')
            )
        
        response_data = {
            'has_custom_input': instance.has_custom_input,
            'custom_input_template': instance.custom_input_template,
            'input_file': instance.input_file.url if instance.input_file else None,
        }
        
        input_function_name = instance.fk_workflow_step.custom_input_function
        if input_function_name:
            from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
            success, template_data = ExternalMethodHandler.call_function(
                input_function_name, instance, request, function_type=FunctionType.INPUT_DATA
            )
            if success:
                response_data['template_data'] = template_data
        
        return ResponseHandler.success(
            message=_('تم جلب بيانات قالب المدخل بنجاح'),
            data=response_data
        )
    
    @action(detail=True, methods=['get'], url_path='output-data', url_name='output-data')
    @handle_exceptions
    def get_output_template_data(self, request, pk=None):
        """
        جلب بيانات قالب المخرج
        - تنفيذ custom_output_function للحصول على البيانات
        """
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance, ActionPermissionType.OUTPUT)
        
        # التحقق من وجود مخرج خاص
        if not instance.has_custom_output:
            raise ValidationException(
                message=_('هذه المرحلة لا تحتوي على مخرج خاص'),
                hint=_('لا يوجد قالب مخرج لهذه المرحلة')
            )
        
        response_data = {
            'has_custom_output': instance.has_custom_output,
            'custom_output_template': instance.custom_output_template,
            'output_file': instance.output_file.url if instance.output_file else None,
        }
        
        # تنفيذ دالة المخرج إذا كانت موجودة
        output_function_name = instance.fk_workflow_step.custom_output_function
        if output_function_name:
            from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
            
            success, template_data = ExternalMethodHandler.call_function(
                output_function_name, instance, request, function_type=FunctionType.OUTPUT_DATA
            )
            if success:
                response_data['template_data'] = template_data
        
        return ResponseHandler.success(
            message=_('تم جلب بيانات قالب المخرج بنجاح'),
            data=response_data
        )
    
    @action(detail=False, methods=['get'], url_path='my-pending', url_name='my-pending')
    @handle_exceptions
    def my_pending_stages(self, request):
        """
        المراحل المعلقة للمستخدم الحالي
        - يتم جلب المراحل حسب صلاحيات StagePermission للمستخدم
        """
        user = request.user
        
        # جلب خطوات سير العمل التي لديه صلاحية عليها
        permitted_steps = StagePermission.objects.filter(
            fk_user=user
        ).values_list('fk_workflow_step_permission__fk_workflow_step_id', flat=True)
        
        # جلب المراحل المعلقة
        pending_actions = RequestAction.objects.filter(
            fk_workflow_step_id__in=permitted_steps,
            is_current=True,
            stage_status__in=[StageStatusChoice.PENDING, StageStatusChoice.IN_PROGRESS],
        ).select_related(
            'fk_request', 'fk_workflow_step', 'fk_workflow_step__fk_stage'
        )
        
        # تصفية حسب المنظمة
        organization = getattr(user, 'fk_organization', None)
        if organization and not user.is_superuser:
            pending_actions = pending_actions.filter(
                fk_request__fk_organization=organization
            )
        
        serializer = RequestActionSerializer(pending_actions, many=True)
        
        return ResponseHandler.success(
            message=_('تم جلب قائمة المراحل المعلقة بنجاح'),
            data=serializer.data,
            extra={'count': pending_actions.count()}
        )
    
    @action(detail=True, methods=['get'], url_path='checklist', url_name='checklist')
    @handle_exceptions
    def get_checklist(self, request, pk=None):
        """جلب قائمة التحقق للمرحلة"""
        from d_services.models.StageChecklistItem import StageChecklistItem
        
        instance = self.get_object()
        user = request.user
        
        self._validate_stage_permission(user, instance)
        
        checklist_items = StageChecklistItem.objects.filter(
            fk_request_action=instance,
            is_deleted=False
        ).order_by('order').select_related('fk_checked_by')
        
        items_data = []
        for item in checklist_items:
            items_data.append({
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'order': item.order,
                'is_required': item.is_required,
                'is_checked': item.is_checked,
                'checked_at': item.checked_at,
                'checked_by': item.fk_checked_by.username if item.fk_checked_by else None,
            })
        
        # إحصائيات
        total_count = checklist_items.count()
        checked_count = checklist_items.filter(is_checked=True).count()
        required_count = checklist_items.filter(is_required=True).count()
        required_checked = checklist_items.filter(is_required=True, is_checked=True).count()
        
        return ResponseHandler.success(
            message=_('تم جلب قائمة التحقق بنجاح'),
            data={
                'items': items_data,
                'stats': {
                    'total_count': total_count,
                    'checked_count': checked_count,
                    'required_count': required_count,
                    'required_checked': required_checked,
                    'all_required_checked': required_count == required_checked,
                    'completion_percentage': round((checked_count / total_count * 100), 1) if total_count > 0 else 100
                }
            }
        )

class RequestNoteMVS(AllMVS):
    queryset = RequestNote.objects.select_related()
    serializer_class = RequestNoteSerializer
    enable_actions = ["sync-import" ,  "sync-export",  "sync-push","sync-pull"]

class RequestAttachmentMVS(AllMVS):
    queryset = RequestAttachment.objects.select_related()
    serializer_class = RequestAttachmentSerializer
    enable_actions = ["sync-import" ,  "sync-export",  "sync-push","sync-pull"]
