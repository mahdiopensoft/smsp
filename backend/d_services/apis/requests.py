from decimal import Decimal

from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction
from d_services.models.ServiceCallResult import ServiceCallResult

from d_services.utils.exception_handler import (
    handle_exceptions,
    ValidationException,
    ResourceNotFoundException,
    InvalidStatusException,
    BusinessRuleException,
)
from d_services.models.ServiceRequest import ServiceRequest
from d_services.models.RequestInstallment import RequestInstallment
from d_services.models.RequestAction import RequestAction
from d_services.models.RequestAttachment import RequestAttachment
from d_services.models.Service import Service
from d_services.models.OrganizationServiceConfig import OrganizationServiceConfig
from d_services.models.GrantSource import GrantSource
from d_services.serializers.requests import (
    ServiceCallResultSerializer,
    ServiceRequestSerializer,
)
from d_services.choices.choices import (
    ServiceStatusChoice,
    PaymentStatusChoice,
    StageStatusChoice,
    GrantStatusChoice,
    DiscountStatusChoice,
    LogActionChoice,
)
from config.imports.viewmodel_core import AllMVS
from d_services.models.GroupServicePermission import GroupServicePermission
from middleware_system.models.Invoice import PartnerType
from middleware_system.serializers.Invoice import ERPInvoiceSerializer, ERPInvoice
from utils.BranchMixinQuerset import BranchViewSetMixin

from d_services.utils.messages import Messages
from d_services.utils.response_handler import ResponseHandler
from d_services.utils.validation_handler import ValidationHandler
from d_services.utils.calculation_handler import CalculationHandler
from d_services.utils.workflow_handler import WorkflowHandler
from d_services.utils.logging_manager import LoggingManager

from OpenSoftCoreV41.utils.helpers.utils.requires import require_field, require_instance
import json
from OpenSoftCoreV41.utils.helpers.utils.dict import reconstruct_nested_dict
from d_services.choices.choices import ServiceStatusChoice

from django.db.models import Prefetch, Count, Q
from d_services.models.StageChecklistItem import StageChecklistItem
from utils.core.base_api_view import BaseAPIViewWithUserOrg, BaseApiView


class ServiceCallResultMVS(AllMVS):
    queryset = ServiceCallResult.objects.prefetch_related()
    serializer_class = ServiceCallResultSerializer


class ServiceRequestMVS(BaseAPIViewWithUserOrg):
    # Optimized queryset with deep prefetch for N+1 prevention

    queryset = ServiceRequest.objects.select_related(
        "fk_service",
        "fk_organization",
        "fk_requester",
        "fk_grant_source",
        "fk_service_version",
    ).prefetch_related(
        Prefetch(
            "installments", queryset=RequestInstallment.objects.filter(is_deleted=False)
        ),
        Prefetch(
            "attachments",
            queryset=RequestAttachment.objects.filter(is_deleted=False).select_related(
                "fk_uploaded_by"
            ),
        ),
        Prefetch(
            "actions",
            queryset=RequestAction.objects.select_related(
                "fk_workflow_step",
                "fk_workflow_step__fk_stage",
                "fk_started_by",
                "fk_executed_by",
                "fk_completed_by",
                "fk_approved_by",
            )
            .prefetch_related(
                Prefetch(
                    "checklist_items",
                    queryset=StageChecklistItem.objects.select_related(
                        "fk_checked_by"
                    ).order_by("order"),
                )
            )
            .order_by("order"),
        ),
    )
    serializer_class = ServiceRequestSerializer
    branch_field = "fk_organization"
    # enable_actions = ['all','select','list','second_list','filter','filter_paginate',]

    def list(self, request, *args, **kwargs):
        user = request.user
        # queryset = super().get_queryset()
        queryset = super().get_queryset().filter(fk_requester=user)
        # Add notes count annotation to avoid N+1 for notes_count field
        queryset = queryset.annotate(
            notes_count_annotation=Count("notes", filter=Q(notes__is_deleted=False))
        )

        service_id = request.query_params.get("fk_service")
        if service_id:
            if not ValidationHandler.check_service_permission(user, service_id, "READ"):
                return ResponseHandler.forbidden(
                    _("ليس لديك صلاحية عرض طلبات هذه الخدمة")
                )
            queryset = queryset.filter(fk_service_id=service_id)
        else:
            return ResponseHandler.bad_request(_("يجب تحديد رقم الخدمة"))
        organization = getattr(user, "fk_organization", None)
        if organization and not user.is_superuser:
            queryset = queryset.filter(fk_organization=organization)

        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        priority = request.query_params.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        payment_status_filter = request.query_params.get("payment_status")
        if payment_status_filter:
            queryset = queryset.filter(payment_status=payment_status_filter)

        grant_status_filter = request.query_params.get("grant_status")
        if grant_status_filter:
            queryset = queryset.filter(grant_status=grant_status_filter)

        discount_status_filter = request.query_params.get("discount_status")
        if discount_status_filter:
            queryset = queryset.filter(discount_status=discount_status_filter)

        is_locked = request.query_params.get("is_locked")
        if is_locked is not None:
            queryset = queryset.filter(is_locked=is_locked.lower() == "true")

        requester_id = request.query_params.get("fk_requester")
        if requester_id:
            queryset = queryset.filter(fk_requester_id=requester_id)

        request_number = request.query_params.get("request_number")
        if request_number:
            queryset = queryset.filter(request_number__icontains=request_number)

        date_from = request.query_params.get("date_from")
        if date_from:
            queryset = queryset.filter(requested_at__date__gte=date_from)

        date_to = request.query_params.get("date_to")
        if date_to:
            queryset = queryset.filter(requested_at__date__lte=date_to)

        ordering = request.query_params.get("sort_by", "-requested_at")
        queryset = queryset.order_by(ordering)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        import os
        import json

        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(
            user, instance.fk_service_id, "READ"
        ):
            return ResponseHandler.forbidden(_("ليس لديك صلاحية عرض تفاصيل هذا الطلب"))
        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_("ليس لديك صلاحية عرض تفاصيل هذا الطلب"))

        service = instance.fk_service
        serializer = ServiceRequestSerializer(instance)

        # جلب مخططات المكونات من الملفات
        component_base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "apis",
            "component",
        )

        def load_schema_file(folder_name, component_name):
            if not component_name:
                return None
            json_file_path = os.path.join(
                component_base_path, folder_name, f"{component_name}.json"
            )
            if os.path.exists(json_file_path):
                try:
                    with open(json_file_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    return None
            return None

        base_component_schema = load_schema_file(
            "base", service.base_audience_component
        )
        target_component_schema = load_schema_file(
            "target", service.target_audience_component
        )

        # جلب بيانات الإصدار
        current_version = service.versions.filter(is_current=True).first()

        # جلب إعدادات تقرير الطباعة من تكوين المنظمة
        org_config = OrganizationServiceConfig.objects.filter(
            fk_service=service, fk_organization=instance.fk_organization
        ).first()

        return ResponseHandler.success(
            message=Messages.DETAIL_SUCCESS,
            data={
                **serializer.data,
                # بيانات الخدمة
                "fk_service__name": service.name_ar,
                "fk_service__code": service.code,
                "input_template_type": service.input_template_type,
                "output_template_type": service.output_template_type,
                # مكون الجمهور المستهدف
                "target_audience_component": service.target_audience_component,
                "target_audience_schema": target_component_schema,
                # المكون الأساسي
                "base_audience_component": service.base_audience_component,
                "base_audience_schema": base_component_schema,
                # بيانات الإصدار
                "version_name": (
                    current_version.version_name if current_version else None
                ),
                "version_schema": (
                    current_version.fields_schema if current_version else {}
                ),
                "component_type": (
                    current_version.component_type if current_version else None
                ),
                # إعدادات تقرير الطباعة
                "fk_print_report_setting_for_input": (
                    org_config.fk_print_report_setting_for_input_id
                    if org_config
                    else None
                ),
                "fk_print_report_setting_for_output": (
                    org_config.fk_print_report_setting_for_output_id
                    if org_config
                    else None
                ),
                "fk_print_report_setting_for_input__name": (
                    org_config.fk_print_report_setting_for_input.name
                    if org_config and org_config.fk_print_report_setting_for_input
                    else None
                ),
                "fk_print_report_setting_for_output__name": (
                    org_config.fk_print_report_setting_for_output.name
                    if org_config and org_config.fk_print_report_setting_for_output
                    else None
                ),
                "fk_currency__name_ar": (
                    org_config.fk_currency.name_ar
                    if org_config and org_config.fk_currency
                    else None
                ),
                "fk_currency": (
                    org_config.fk_currency.id
                    if org_config and org_config.fk_currency
                    else None
                ),
            },
        )

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        row_data = (
            request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
        )
        data_json = row_data.get("data")
        if data_json:
            if isinstance(data_json, list):
                data_json = data_json[0]
            try:
                data = json.loads(data_json)
            except (json.JSONDecodeError, TypeError):
                return ResponseHandler.bad_request(_("صيغة البيانات غير صحيحة"))
        else:
            data = dict(row_data)

        row_data = reconstruct_nested_dict(row_data)

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_("ليس لديك صلاحية تعديل هذا الطلب"))
        if not ValidationHandler.check_service_permission(
            user, instance.fk_service_id, "UPDATE"
        ):
            return ResponseHandler.forbidden(_("ليس لديك صلاحية تعديل هذا الطلب"))

        if instance.status != ServiceStatusChoice.PENDING:
            return ResponseHandler.bad_request(
                _("لا يمكن تعديل الطلب لأنه ليس في حالة انتظار"),
                details={"current_status": instance.get_status_display()},
                hint=_('يمكن تعديل الطلبات فقط عندما تكون في حالة "انتظار"'),
            )

        if instance.is_locked:
            return ResponseHandler.bad_request(
                _("الطلب مقفول ولا يمكن تعديله"),
                details={
                    "locked_reason": instance.locked_reason or _("غير محدد"),
                    "locked_at": (
                        instance.locked_at.strftime("%Y-%m-%d %H:%M")
                        if instance.locked_at
                        else None
                    ),
                },
                hint=_("تواصل مع مدير النظام لفتح قفل الطلب إذا كنت بحاجة لتعديله"),
            )

        with transaction.atomic():
            allowed_fields = ["version_data", "priority"]
            for field in allowed_fields:
                if field in data:
                    setattr(instance, field, data[field])
            instance.is_from_gate = True
            instance.save()

            attachments_dict = row_data.get("attachments", {})
            sent_attachment_ids = set()

            for key, attachment_data in attachments_dict.items():
                attachment_id = attachment_data.get("id")

                if attachment_id:
                    sent_attachment_ids.add(int(attachment_id))
                    try:
                        existing_attachment = RequestAttachment.objects.get(
                            id=attachment_id, fk_request=instance
                        )
                        if attachment_data.get("name"):
                            existing_attachment.name = attachment_data.get("name")
                        if attachment_data.get("description"):
                            existing_attachment.description = attachment_data.get(
                                "description"
                            )
                        if attachment_data.get("file"):
                            existing_attachment.file = attachment_data.get("file")
                        existing_attachment.save()
                    except RequestAttachment.DoesNotExist:
                        pass
                else:
                    if attachment_data.get("file"):
                        RequestAttachment.objects.create(
                            fk_request=instance,
                            name=attachment_data.get("name", ""),
                            file=attachment_data.get("file"),
                            fk_uploaded_by=user,
                            description=attachment_data.get("description", ""),
                        )

            if attachments_dict:
                instance.attachments.exclude(id__in=sent_attachment_ids).delete()

        return ResponseHandler.success(
            message=Messages.UPDATE_SUCCESS,
            data=ServiceRequestSerializer(instance).data,
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        row_data = (
            request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
        )
        data = require_field(row_data, "data", pop=True)
        data = json.loads(data)
        row_data = reconstruct_nested_dict(row_data)

        target_data = data.get("target_audience_data")
        if not isinstance(target_data, dict):
            target_data = {}
            data["target_audience_data"] = target_data

        base_data = data.get("base_component_data")
        if not isinstance(base_data, dict):
            base_data = {}
            data["base_component_data"] = base_data

        if not target_data.get("fk_student_batch"):
            from portals.students.models.student_academic import StudentAcademic

            academic_record = StudentAcademic.objects.filter(
                fk_student__fk_user=request.user
            ).last()
            if academic_record:
                target_data["fk_student_batch"] = int(academic_record.external_id)
                target_data["fk_student_batch_name"] = (
                    academic_record.fk_student.name_ar
                )

        service_id = data.get("fk_service")
        if not service_id:
            return ResponseHandler.bad_request(_("معرف الخدمة مطلوب"))

        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            return ResponseHandler.not_found(
                _("الخدمة غير موجودة"), hint=_("تأكد من صحة معرف الخدمة المرسل")
            )

        if not ValidationHandler.check_service_permission(user, service_id, "CREATE"):
            return ResponseHandler.forbidden(_("ليس لديك صلاحية إنشاء طلب لهذه الخدمة"))

        if not service.is_active:
            return ResponseHandler.bad_request(
                _("الخدمة غير مفعلة حالياً"),
                details={"service_name": service.name_ar},
                hint=_("تواصل مع مدير النظام لتفعيل الخدمة"),
            )

        # التحقق من وجود خطوات سير عمل للخدمة
        if not service.workflow_steps.all().exists():
            return ResponseHandler.bad_request(
                _("الخدمة لا تحتوي على خطوات سير عمل"),
                details={"service_name": service.name_ar},
                hint=_("تواصل مع مدير النظام لإعداد خطوات سير العمل لهذه الخدمة"),
            )

        if service.start_date and service.start_date > timezone.now().date():
            return ResponseHandler.bad_request(
                _("الخدمة لم تبدأ بعد"),
                details={
                    "service_name": service.name_ar,
                    "start_date": service.start_date.strftime("%Y-%m-%d"),
                },
                hint=_("ستكون الخدمة متاحة ابتداءً من التاريخ المحدد"),
            )

        organization = getattr(user, "fk_organization", None)
        if not organization:
            return ResponseHandler.bad_request(_("المستخدم غير مرتبط بمنظمة"))

        org_config = OrganizationServiceConfig.objects.filter(
            fk_service=service, fk_organization=organization, is_active=True
        ).first()

        if not org_config:
            return ResponseHandler.bad_request(
                _("الخدمة غير متاحة لمنظمتك"),
                details={"service_name": service.name_ar},
                hint=_("تواصل مع مدير النظام لتفعيل الخدمة لمنظمتك"),
            )

        installment_plans = None
        if org_config.is_installment_allowed:
            installment_plans = org_config.installment_plans.order_by("order")
            if not installment_plans.exists():
                return ResponseHandler.bad_request(
                    _("الخدمة تتطلب تقسيط ولكن لم يتم تحديد خطط الأقساط"),
                    hint=_("تواصل مع مدير النظام لإعداد خطط التقسيط لهذه الخدمة"),
                )

        prerequisites_validation = WorkflowHandler.validate_prerequisites(
            service, user, data
        )
        if prerequisites_validation and prerequisites_validation.get("has_errors"):
            return ResponseHandler.bad_request(
                _("لم يتم استيفاء شروط الخدمة"),
                details={
                    "prerequisites_errors": prerequisites_validation.get("errors"),
                    "all_validations": prerequisites_validation.get("all_results"),
                },
            )

        with transaction.atomic():

            # جلب صورة مقدم الطلب باستخدام الدالة المحددة في الخدمة
            from d_services.utils.image_handler import ImageHandler, ERPHandler

            requester_image = ImageHandler.get_image_for_service(service, user, data)
            # اذا كانت الصورة عبارة عن مسار يتم حذف /media لكي لا يتكرر عند تخزين الصورة
            if (
                requester_image
                and isinstance(requester_image, str)
                and requester_image.startswith("/media")
            ):
                requester_image = requester_image.split("/media")[1]
            # جلب بيانات مقدم الطلب (الاسم والوصف)
            requester_info = ImageHandler.get_info_for_service(service, user, data)
            requester_name = requester_info.get("name", "") if requester_info else ""
            requester_description = (
                requester_info.get("description", "") if requester_info else ""
            )
            requester_id = requester_info.get("id", "") if requester_info else None

            existing_request = ServiceRequest.objects.filter(
                fk_service=service,
                fk_organization=organization,
                requester_id=requester_id,
                status__in=[
                    ServiceStatusChoice.APPROVED,
                    ServiceStatusChoice.IN_PROGRESS,
                ],
            ).first()
            if existing_request:
                return ResponseHandler.bad_request(
                    _("يوجد طلب سابق لنفس مقدم الطلب قيد المراجعة"),
                    hint=_("يجب الانتظار حتى يتم الانتهاء من الطلب السابق او إلغائة"),
                )

            request_number = CalculationHandler.generate_request_number(
                organization, org_config
            )
            fees = CalculationHandler.calculate_fees(
                service, org_config, organization, requester_id=requester_id
            )

            # --- ERP defaults: try erp_data_function, fallback to org_config ---
            erp_data = ERPHandler.get_erp_data(service, user, data, org_config)
            # جلب معرفات الجهات المانحة المتاحة للطالب (مقدم الطلب) من البيانات الراجعة من erp_data function
            available_grant_sources_ids = erp_data.get(
                "available_grant_sources_ids", []
            )
            partner_data = erp_data.get("partner_data", {})

            # fee & currency: prefer erp_data result, then CalculationHandler
            fee_amount = erp_data.get("service_fee") or fees.get("total_fee", 0)
            currency_code = erp_data.get("fk_currency")

            # التحقق من وجود الاسم والصورة (إذا كانت مطلوبة)

            if not requester_name:
                return ResponseHandler.bad_request(
                    _("لم يتم العثور على اسم مقدم الطلب"),
                    hint=_("تأكد من اكتمال بيانات المستخدم"),
                )

            current_version = service.versions.filter(is_current=True).first()
            version_id = current_version.id if current_version else None

            service_request = ServiceRequest.objects.create(
                fk_organization=organization,
                fk_service=service,
                fk_service_version_id=version_id,
                fk_requester=user,
                is_from_gate=True,
                source_system=user.source_system or None,
                requester_image=requester_image,
                requester_name=requester_name,
                requester_description=requester_description,
                requester_id=requester_id,
                request_number=request_number,
                target_audience_component=service.target_audience_component,
                target_audience_data=data.get("target_audience_data", {}),
                base_audience_component=service.base_audience_component,
                base_component_data=data.get("base_component_data", {}),
                version_data=data.get("version_data"),
                output_template_type=service.output_template_type,
                input_template_type=service.input_template_type,
                output_data_function=service.output_data_function,
                input_data_function=service.input_data_function,
                status=ServiceStatusChoice.PENDING,
                priority=data.get("priority", "normal"),
                has_approvals=service.requires_approval,
                total_fee=fee_amount,
                discounted_fee=fees["discounted_fee"],
                discounted_fee_reason=fees.get("discounted_fee_reason"),
                amount_paid=fees["amount_paid"],
                remaining_amount=fees["remaining_amount"],
                payment_status=fees["payment_status"],
                partner_data=partner_data,
                currency=currency_code,
                workflow_stages_snapshot=WorkflowHandler.get_workflow_snapshot(service),
                prerequisites_snapshot=WorkflowHandler.get_prerequisites_snapshot(
                    service
                ),
                # ERP integration fields — from erp_data_function or org_config
                is_donor_invoice_allowed=ERPHandler.get_field(
                    erp_data,
                    "is_donor_invoice_allowed",
                    org_config.is_donor_invoice_allowed,
                ),
                available_grant_sources_ids=available_grant_sources_ids,
                is_discount_allowed=ERPHandler.get_field(
                    erp_data, "is_discount_allowed", org_config.is_discount_allowed
                ),
                erp_product_id=ERPHandler.get_field(
                    erp_data, "erp_product_id", org_config.erp_product_id
                ),
                erp_product_name=ERPHandler.get_field(
                    erp_data, "erp_product_name", org_config.erp_product_name
                ),
                erp_product_for_discount_id=ERPHandler.get_field(
                    erp_data,
                    "erp_product_for_discount_id",
                    org_config.erp_product_for_discount_id,
                ),
                erp_product_for_discount_name=ERPHandler.get_field(
                    erp_data,
                    "erp_product_for_discount_name",
                    org_config.erp_product_for_discount_name,
                ),
                erp_product_for_internal_donors_id=ERPHandler.get_field(
                    erp_data,
                    "erp_product_for_internal_donors_id",
                    org_config.erp_product_for_internal_donors_id,
                ),
                erp_product_for_internal_donors_name=ERPHandler.get_field(
                    erp_data,
                    "erp_product_for_internal_donors_name",
                    org_config.erp_product_for_internal_donors_name,
                ),
                erp_project_id=ERPHandler.get_field(
                    erp_data, "erp_project_id", org_config.erp_project_id
                ),
                erp_project_name=ERPHandler.get_field(
                    erp_data, "erp_project_name", org_config.erp_project_name
                ),
                erp_activity_id=ERPHandler.get_field(
                    erp_data, "erp_activity_id", org_config.erp_activity_id
                ),
                erp_activity_name=ERPHandler.get_field(
                    erp_data, "erp_activity_name", org_config.erp_activity_name
                ),
                erp_cost_center_id=ERPHandler.get_field(
                    erp_data, "erp_cost_center_id", org_config.erp_cost_center_id
                ),
                erp_cost_center_name=ERPHandler.get_field(
                    erp_data, "erp_cost_center_name", org_config.erp_cost_center_name
                ),
            )

            WorkflowHandler.save_prerequisites_verification(
                service=service, user=user, data=data, service_request=service_request
            )

            attachments_dict = row_data.get("attachments", {})
            for key, attachment in attachments_dict.items():
                if attachment.get("file"):
                    RequestAttachment.objects.create(
                        fk_request=service_request,
                        name=attachment.get("name", ""),
                        file=attachment.get("file"),
                        fk_uploaded_by=user,
                        description=attachment.get("description", ""),
                    )

            if installment_plans and fees["remaining_amount"] > 0:
                for plan in installment_plans:
                    # نسبة القسط من خطة الاقساط مقابل رسوم الخدمة الاساسية
                    plan_percentage = plan.percentage
                    # plan_amount = plan.amount
                    plan_amount = round(
                        Decimal(service_request.total_fee) * plan_percentage, 2
                    )
                    org_service_config = service_request.org_service_config
                    due_date = timezone.now().date() + timezone.timedelta(
                        days=plan.due_days_from_request or 0
                    )
                    RequestInstallment.objects.create(
                        fk_request=service_request,
                        amount=plan_amount,
                        period=org_service_config.installment_period,
                        order=plan.order,
                        due_date=due_date,
                        payment_status=PaymentStatusChoice.UNPAID,
                    )

            LoggingManager.log_request_create(
                service_request=service_request,
                user=user,
                request=request,
                new_status=ServiceStatusChoice.PENDING,
                notes=f"تم إنشاء طلب جديد برقم {request_number}",
                extra_data={
                    "service_id": service_id,
                    "service_name": service.name_ar,
                    "total_fee": str(fees["total_fee"]),
                    "payment_status": fees["payment_status"],
                },
            )

        return ResponseHandler.created(
            message=Messages.REQUEST_CREATED,
            data=ServiceRequestSerializer(service_request).data,
            extra={"request_number": request_number},
        )

    # ============================================================
    # إدارة المستندات - Document Management
    # ============================================================

    @action(detail=True, methods=["get"], url_path="input-data", url_name="input-data")
    @handle_exceptions
    def get_input_data(self, request, pk=None):
        """جلب بيانات المدخل للطلب"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(
            user, instance.fk_service_id, "GET_INPUT_DATA"
        ):
            return ResponseHandler.forbidden(_("ليس لديك صلاحية جلب بيانات المدخل"))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_("ليس لديك صلاحية الوصول لهذا الطلب"))

        service = instance.fk_service

        func = instance.requests.filter(func=instance.input_data_function)

        response_data = {
            "input_template_type": service.input_template_type,
            "input_document": (
                instance.input_document.url if instance.input_document else None
            ),
            "input_data": getattr(func.first(), "result") if func else None,
        }

        # استدعاء دالة بيانات المدخل إذا وجدت
        # if service.input_data_function:
        #     from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
        #     success, data = ExternalMethodHandler.call_function(
        #         service.input_data_function, instance, request,
        #         function_type=FunctionType.INPUT_DATA
        #     )
        #     if success:
        #         response_data['input_data'] = data

        return ResponseHandler.success(
            message=_("تم جلب بيانات المدخل بنجاح"), data=response_data
        )

    @action(
        detail=True, methods=["get"], url_path="output-data", url_name="output-data"
    )
    @handle_exceptions
    def get_output_data(self, request, pk=None):
        """جلب بيانات المخرج للطلب"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(
            user, instance.fk_service_id, "GET_OUTPUT_DATA"
        ):
            return ResponseHandler.forbidden(_("ليس لديك صلاحية جلب بيانات المخرج"))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_("ليس لديك صلاحية الوصول لهذا الطلب"))

        service = instance.fk_service

        func = instance.requests.filter(func=instance.output_data_function)

        response_data = {
            "output_template_type": service.output_template_type,
            "output_document": (
                instance.output_document.url if instance.output_document else None
            ),
            "output_data": getattr(func.first(), "result") if func else None,
        }

        # استدعاء دالة بيانات المخرج إذا وجدت
        # if service.output_data_function:
        #     from d_services.apis.external_methods import ExternalMethodHandler, FunctionType
        #     success, data = ExternalMethodHandler.call_function(
        #         service.output_data_function, instance, request,
        #         function_type=FunctionType.OUTPUT_DATA
        #     )
        #     if success:
        #         response_data['output_data'] = data

        return ResponseHandler.success(
            message=_("تم جلب بيانات المخرج بنجاح"), data=response_data
        )

    @action(
        detail=True, methods=["post"], url_path="upload-input", url_name="upload-input"
    )
    @handle_exceptions
    def upload_input(self, request, pk=None):
        """رفع ملف المدخل"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(
            user, instance.fk_service_id, "UPLOAD_INPUT"
        ):
            return ResponseHandler.forbidden(_("ليس لديك صلاحية رفع ملف المدخل"))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_("ليس لديك صلاحية الوصول لهذا الطلب"))

        if instance.is_locked:
            return ResponseHandler.forbidden(_("الطلب مقفول ولا يمكن تعديله"))

        input_file = request.FILES.get("input_document")
        if not input_file:
            raise ValidationException(message=_("ملف المدخل مطلوب"))

        instance.input_document = input_file
        instance.save()

        LoggingManager.log_request_action(
            service_request=instance,
            action=LogActionChoice.UPLOAD,
            user=user,
            request=request,
            notes=_("تم رفع ملف المدخل"),
        )

        return ResponseHandler.success(
            message=_("تم رفع ملف المدخل بنجاح"),
            data={"input_document": instance.input_document.url},
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="delete-input",
        url_name="delete-input",
    )
    @handle_exceptions
    def delete_input(self, request, pk=None):
        """حذف ملف المدخل"""
        instance = self.get_object()
        user = request.user

        if not ValidationHandler.check_service_permission(
            user, instance.fk_service_id, "DELETE_INPUT"
        ):
            return ResponseHandler.forbidden(_("ليس لديك صلاحية حذف ملف المدخل"))

        if instance.fk_organization != user.fk_organization:
            return ResponseHandler.forbidden(_("ليس لديك صلاحية الوصول لهذا الطلب"))

        if instance.is_locked:
            return ResponseHandler.forbidden(_("الطلب مقفول ولا يمكن تعديله"))

        if not instance.input_document:
            raise ValidationException(message=_("لا يوجد ملف مدخل للحذف"))

        instance.input_document.delete(save=False)
        instance.input_document = None
        instance.save()

        return ResponseHandler.success(message=_("تم حذف ملف المدخل بنجاح"))
