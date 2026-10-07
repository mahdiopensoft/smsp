from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.db import transaction

from exams.models.ExamDistribution import ExamDistribution
from exams.models.ExamSchoolDispatchStatus import ExamSchoolDispatchStatus
from exams.serializers.ExamDistribution import ExamDistributionSerializer, ExamSchoolDispatchStatusSerializer
from OpenSoftCoreV41.common.models.Branch import Organization

class ExamDistributionMVS(AllMVS):
    """
    Dedicated ModelViewSet for Exam Distribution & Scheduled Export Wizard.
    Endpoint: /api/exams/distributions/
    Used by: ExamDispatchView.vue
    """
    queryset = ExamDistribution.objects.filter(is_deleted=False).select_related(
        'exam__subject', 'exam__year'
    ).prefetch_related('organizations', 'school_statuses__school')
    serializer_class = ExamDistributionSerializer

    @action(detail=False, methods=['get', 'post'], url_path='resolve-hierarchy', permission_classes=[AllowAny], pagination_class=None)
    def resolve_hierarchy(self, request):
        """
        يقوم بفك الاستهداف الهرمي وتحويل (الوزارة أو المحافظات أو المديريات)
        إلى قائمة فعلية بجميع المدارس المستهدفة (company_level = 50).
        يعرض كافة المدارس (30 مدرسة) دفعة واحدة دون أي بجنشن (Unpaginated).
        """
        target_level = request.data.get('target_level') if hasattr(request, 'data') and request.data else None
        if not target_level:
            target_level = request.query_params.get('target_level', 'ministry')

        raw_org_ids = request.data.get('selected_org_ids') if hasattr(request, 'data') and request.data else None
        if not raw_org_ids:
            raw_org_ids = request.query_params.getlist('selected_org_ids') or []

        if isinstance(raw_org_ids, str):
            selected_org_ids = [int(x) for x in raw_org_ids.split(',') if x.strip().isdigit()]
        elif isinstance(raw_org_ids, list):
            selected_org_ids = [int(x) for x in raw_org_ids if str(x).isdigit()]
        else:
            selected_org_ids = []

        exam_id = request.data.get('exam_id') if hasattr(request, 'data') and request.data else None
        if not exam_id:
            exam_id = request.query_params.get('exam_id')

        schools_qs = Organization.objects.filter(is_deleted=False, company_level=50)

        if target_level == 'ministry':
            # يشمل جميع المدارس بالكامل في الجمهورية
            final_schools = schools_qs
        elif target_level == 'governorate':
            # جلب المدارس التابعة للمحافظات المختارة
            final_schools = schools_qs.filter(
                fk_governorate_id__in=selected_org_ids
            ) | schools_qs.filter(
                fk_parent_organization__fk_governorate_id__in=selected_org_ids
            ) | schools_qs.filter(
                fk_parent_organization__fk_parent_organization_id__in=selected_org_ids
            )
        elif target_level == 'directorate':
            # جلب المدارس التابعة للمديريات المختارة
            final_schools = schools_qs.filter(
                fk_directorate_id__in=selected_org_ids
            ) | schools_qs.filter(
                fk_parent_organization_id__in=selected_org_ids
            )
        elif target_level == 'school':
            # مدارس محددة بعينها
            final_schools = schools_qs.filter(id__in=selected_org_ids)
        else:
            final_schools = schools_qs.filter(id__in=selected_org_ids)

        # في حال كان للاختبار نطاق استهداف جغرافي مسبق، يتم تصفية المدارس حصراً ضمن نطاق الاختبار
        if exam_id:
            from exams.models.ExamTargetScope import ExamTargetScope
            target_scopes = ExamTargetScope.objects.filter(exam_id=exam_id, is_deleted=False)
            if target_scopes.exists():
                from django.db.models import Q
                gov_ids = list(target_scopes.filter(scope_level='governorate', governorate__isnull=False).values_list('governorate_id', flat=True))
                dir_ids = list(target_scopes.filter(scope_level='directorate', directorate__isnull=False).values_list('directorate_id', flat=True))
                school_ids = list(target_scopes.filter(scope_level='school', organization__isnull=False).values_list('organization_id', flat=True))

                scope_q = Q()
                if gov_ids:
                    scope_q |= Q(fk_governorate_id__in=gov_ids) | Q(fk_parent_organization__fk_governorate_id__in=gov_ids)
                if dir_ids:
                    scope_q |= Q(fk_directorate_id__in=dir_ids) | Q(fk_parent_organization_id__in=dir_ids)
                if school_ids:
                    scope_q |= Q(id__in=school_ids)

                if scope_q:
                    final_schools = final_schools.filter(scope_q)

        final_schools = final_schools.distinct().select_related('fk_governorate', 'fk_directorate').order_by('branch_no', 'id')

        data = [
            {
                "id": s.id,
                "name_ar": s.name_ar,
                "name_en": s.name_en or s.name_ar,
                "branch_no": s.branch_no,
                "governorate": s.fk_governorate.name_ar if s.fk_governorate else '-',
                "directorate": s.fk_directorate.name_ar if s.fk_directorate else '-',
            }
            for s in final_schools
        ]

        return Response({
            "success": True,
            "target_level": target_level,
            "total_schools": len(data),
            "count": len(data),
            "schools": data,
            "results": data
        })

    @action(detail=False, methods=['post'], url_path='create-dispatch')
    def create_dispatch(self, request):
        """
        إنشاء مهمة توزيع وجدولة تصدير وتوليد سجلات المتابعة لجميع المدارس المستهدفة.
        """
        data = request.data
        exam_id = data.get('exam_id') or data.get('exam')
        title = data.get('title') or 'توزيع اختبار جديد'
        target_level = data.get('target_level', 'school')
        target_system = data.get('target_system', 'school')
        delivery_mode = data.get('delivery_mode', 'printed_omr')
        
        dispatch_at = data.get('dispatch_at') or timezone.now()
        accessible_from = data.get('accessible_from') or timezone.now()
        exam_start_at = data.get('exam_start_at') or timezone.now()
        exam_end_at = data.get('exam_end_at') or timezone.now()
        
        is_encrypted = data.get('is_encrypted', True)
        auto_unlock = data.get('auto_unlock', True)
        notes = data.get('notes', '')

        selected_school_ids = data.get('selected_school_ids', [])

        if not exam_id:
            return Response({"success": False, "message": "يجب تحديد الاختبار المراد توزيعه"}, status=status.HTTP_400_BAD_REQUEST)

        # التحقق الأمني والنظامي: منع ازدواجية وتكرار تصدير الاختبار إذا كانت هناك مهمة توزيع نشطة قائمة بالفعل
        active_statuses = [
            ExamDistribution.Status.SCHEDULED,
            ExamDistribution.Status.DISPATCHED,
            ExamDistribution.Status.ACCESSIBLE,
            ExamDistribution.Status.IN_PROGRESS
        ]
        active_existing_dist = ExamDistribution.objects.filter(
            exam_id=exam_id,
            is_deleted=False,
            status__in=active_statuses
        ).first()

        if active_existing_dist:
            return Response({
                "success": False,
                "message": (
                    f"لا يمكن تصدير هذا الاختبار مجدداً؛ توجد مهمة توزيع نشطة قائمة بالفعل لنفس الاختبار "
                    f"(مهمة رقم #{active_existing_dist.id}: {active_existing_dist.title}) "
                    f"بحالة ({active_existing_dist.get_status_display()}). "
                    f"يرجى متابعة المهمة النشطة الحالية أو إلغاؤها أولاً قبل إعادة التصدير."
                ),
                "existing_distribution_id": active_existing_dist.id,
                "existing_status": active_existing_dist.status
            }, status=status.HTTP_400_BAD_REQUEST)

        # إذا لم يتم تمرير المدارس مباشرة، يتم فك الهيكلية
        if not selected_school_ids:
            res = self.resolve_hierarchy(request)
            selected_school_ids = [s["id"] for s in res.data.get("schools", [])]

        # التحقق من تقيد المدارس بنطاق استهداف الاختبار الجغرافي إن وجد
        from exams.models.ExamTargetScope import ExamTargetScope
        target_scopes = ExamTargetScope.objects.filter(exam_id=exam_id, is_deleted=False)
        if target_scopes.exists():
            from django.db.models import Q
            gov_ids = list(target_scopes.filter(scope_level='governorate', governorate__isnull=False).values_list('governorate_id', flat=True))
            dir_ids = list(target_scopes.filter(scope_level='directorate', directorate__isnull=False).values_list('directorate_id', flat=True))
            school_ids = list(target_scopes.filter(scope_level='school', organization__isnull=False).values_list('organization_id', flat=True))

            scope_q = Q()
            if gov_ids:
                scope_q |= Q(fk_governorate_id__in=gov_ids) | Q(fk_parent_organization__fk_governorate_id__in=gov_ids)
            if dir_ids:
                scope_q |= Q(fk_directorate_id__in=dir_ids) | Q(fk_parent_organization_id__in=dir_ids)
            if school_ids:
                scope_q |= Q(id__in=school_ids)

            if scope_q:
                allowed_school_ids = set(Organization.objects.filter(is_deleted=False, company_level=50).filter(scope_q).values_list('id', flat=True))
                selected_school_ids = [s_id for s_id in selected_school_ids if s_id in allowed_school_ids]

        if not selected_school_ids:
            return Response({"success": False, "message": "لم يتم العثور على أي مدارس مطابقة للاستهداف المحدد ضمن النطاق الجغرافي للاختبار"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. إنشاء سجل التوزيع
                dist = ExamDistribution.objects.create(
                    exam_id=exam_id,
                    title=title,
                    target_level=target_level,
                    target_system=target_system,
                    delivery_mode=delivery_mode,
                    dispatch_at=dispatch_at,
                    accessible_from=accessible_from,
                    exam_start_at=exam_start_at,
                    exam_end_at=exam_end_at,
                    is_encrypted=is_encrypted,
                    auto_unlock=auto_unlock,
                    notes=notes,
                    status=ExamDistribution.Status.SCHEDULED
                )

                # 2. ربط المدارس المستهدفة
                dist.organizations.set(selected_school_ids)

                # 3. إنشاء سجلات المتابعة للمدارس
                statuses_to_create = [
                    ExamSchoolDispatchStatus(
                        distribution=dist,
                        school_id=school_id,
                        is_received=False,
                        is_accessible=False
                    )
                    for school_id in selected_school_ids
                ]
                ExamSchoolDispatchStatus.objects.bulk_create(statuses_to_create)

                serializer = self.get_serializer(dist)
                return Response({
                    "success": True,
                    "message": f"تمت جدولة مهمة التوزيع بنجاح إلى {len(selected_school_ids)} مدرسة",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": f"فشل إنشاء مهمة التوزيع: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='live-status')
    def live_status(self, request, pk=None):
        """
        إحصائيات المتابعة الحية لتسليم الاختبار للمدارس.
        """
        dist = self.get_object()
        now = timezone.now()

        # فحص تلقائي لحالة التوزيع بناءً على التوقيت
        if dist.status != ExamDistribution.Status.CANCELLED:
            if now >= dist.exam_end_at:
                dist.status = ExamDistribution.Status.COMPLETED
            elif now >= dist.exam_start_at:
                dist.status = ExamDistribution.Status.IN_PROGRESS
            elif now >= dist.accessible_from:
                dist.status = ExamDistribution.Status.ACCESSIBLE
            elif now >= dist.dispatch_at:
                dist.status = ExamDistribution.Status.DISPATCHED
            dist.save(update_fields=['status'])

        statuses = dist.school_statuses.select_related('school__fk_governorate', 'school__fk_directorate')
        total_schools = statuses.count()
        received_count = statuses.filter(is_received=True).count()
        accessible_count = statuses.filter(is_accessible=True).count()
        printed_sheets_total = sum(s.printed_sheets_count for s in statuses)
        attended_students_total = sum(s.students_attended_count for s in statuses)

        schools_data = ExamSchoolDispatchStatusSerializer(statuses, many=True).data

        return Response({
            "success": True,
            "distribution_id": dist.id,
            "title": dist.title,
            "status": dist.status,
            "timing": {
                "dispatch_at": dist.dispatch_at,
                "accessible_from": dist.accessible_from,
                "exam_start_at": dist.exam_start_at,
                "exam_end_at": dist.exam_end_at,
                "is_accessible_now": (now >= dist.accessible_from),
                "is_exam_started": (now >= dist.exam_start_at),
                "is_exam_ended": (now >= dist.exam_end_at),
            },
            "kpis": {
                "total_schools": total_schools,
                "received_schools": received_count,
                "received_percentage": round((received_count / (total_schools or 1)) * 100, 1),
                "accessible_schools": accessible_count,
                "total_printed_sheets": printed_sheets_total,
                "total_attended_students": attended_students_total,
            },
            "schools": schools_data
        })

    @action(detail=True, methods=['post'], url_path='cancel-dispatch')
    def cancel_dispatch(self, request, pk=None):
        """
        إلغاء مهمة التوزيع وحجب الحزم فوراً عن المدارس
        """
        dist = self.get_object()
        if dist.status == ExamDistribution.Status.COMPLETED:
            return Response({"success": False, "message": "لا يمكن إلغاء مهمة توزيع مكتملة بالفعل"}, status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get('reason', '')
        dist.status = ExamDistribution.Status.CANCELLED
        if reason:
            dist.notes = f"{dist.notes or ''}\n[سبب الإلغاء: {reason}]".strip()
        dist.save(update_fields=['status', 'notes'])
        return Response({
            "success": True,
            "message": "تم إلغاء مهمة التوزيع بنجاح وحجب الحزم عن كافة الأنظمة الفرعية",
            "status": dist.status
        })

    @action(detail=True, methods=['post'], url_path='force-unlock')
    def force_unlock(self, request, pk=None):
        """
        فك حجب الأسئلة وإتاحتها للطباعة فوراً في حالات الطوارئ دون انتظار الموعد المجدول
        """
        dist = self.get_object()
        if dist.status == ExamDistribution.Status.CANCELLED:
            return Response({"success": False, "message": "لا يمكن فك حجب مهمة توزيع ملغاة"}, status=status.HTTP_400_BAD_REQUEST)
        now = timezone.now()
        dist.accessible_from = now
        dist.is_encrypted = False
        if dist.status in [ExamDistribution.Status.SCHEDULED, ExamDistribution.Status.DISPATCHED]:
            dist.status = ExamDistribution.Status.ACCESSIBLE
        dist.save(update_fields=['accessible_from', 'is_encrypted', 'status'])

        # تحديث حالة المدارس المستلمة لتصبح مفتوحة فوراً
        dist.school_statuses.filter(is_received=True, is_accessible=False).update(
            is_accessible=True,
            accessible_at=now
        )
        return Response({
            "success": True,
            "message": "تم فك حجب الأسئلة بنجاح وإتاحتها للطباعة في كافة المدارس فوراً",
            "status": dist.status,
            "accessible_from": dist.accessible_from
        })

    @action(detail=True, methods=['get'], url_path='download-package')
    def download_package(self, request, pk=None):
        """
        توليد وتنزيل حزمة الاختبار الكاملة للتوزيع كـ JSON للكنترول المركزي أو التوزيع اليدوي (Offline Export).
        """
        dist = self.get_object()
        now = timezone.now()
        exam = dist.exam

        models_data = []
        versions = exam.versions.filter(is_deleted=False).prefetch_related(
            'question_orders__question__options'
        ).order_by('versionCode')

        for ver in versions:
            questions_list = []
            answer_key = {}
            for qo in ver.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                q = qo.question
                if not q:
                    continue
                options_data = []
                correct_opt_char = 'A'
                all_opts = list(q.options.filter(is_deleted=False))
                for opt_idx, opt in enumerate(all_opts):
                    opt_char = chr(65 + opt_idx)
                    options_data.append({
                        "option_char": opt_char,
                        "text": opt.text,
                        "is_true": opt.isTrue
                    })
                    if opt.isTrue:
                        correct_opt_char = opt_char

                if q.questionType == 'True/False' and q.isTrue is not None:
                    correct_opt_char = 'A' if q.isTrue else 'B'

                answer_key[str(qo.orderIndex)] = correct_opt_char
                questions_list.append({
                    "order_index": qo.orderIndex,
                    "question_id": q.id,
                    "type": q.questionType,
                    "content": q.content,
                    "default_mark": q.defaultMark,
                    "options": options_data
                })

            models_data.append({
                "version_code": ver.versionCode,
                "total_questions": len(questions_list),
                "questions": questions_list,
                "answer_key": answer_key
            })

        package_data = {
            "distribution_id": dist.id,
            "dispatch_title": dist.title,
            "exam_id": exam.id,
            "unique_code": exam.uniqueCode,
            "subject": exam.subject.name_ar if exam.subject else 'عام',
            "academic_year": str(exam.year) if exam.year else '-',
            "delivery_mode": dist.delivery_mode,
            "delivery_mode_display": dist.get_delivery_mode_display(),
            "timing": {
                "dispatch_at": dist.dispatch_at.isoformat() if dist.dispatch_at else None,
                "accessible_from": dist.accessible_from.isoformat() if dist.accessible_from else None,
                "exam_start_at": dist.exam_start_at.isoformat() if dist.exam_start_at else None,
                "exam_end_at": dist.exam_end_at.isoformat() if dist.exam_end_at else None,
                "exported_at": now.isoformat()
            },
            "targeted_schools_count": dist.organizations.count(),
            "models": models_data,
            "omr_specs": {
                "template": "A4_STANDARD_40Q",
                "paper_size": "A4",
                "dpi": 300
            },
            "notes": dist.notes
        }
        return Response({
            "success": True,
            "package": package_data
        })

    @action(detail=True, methods=['post'], url_path='simulate-school-sync')
    def simulate_school_sync(self, request, pk=None):
        """
        محاكاة تفاعلية لسحب حزمة وتأكيد استلام وطباعة أوراق OMR من مدرسة مستهدفة
        لأغراض العرض والتأكد الميداني في واجهة المتابعة الحية.
        """
        dist = self.get_object()
        school_id = request.data.get('school_id')
        if not school_id:
            return Response({"success": False, "message": "يجب تحديد المدرسة المراد محاكاتها"}, status=status.HTTP_400_BAD_REQUEST)

        dispatch_status = dist.school_statuses.filter(school_id=school_id).first()
        if not dispatch_status:
            return Response({"success": False, "message": "المدرسة غير مدرجة ضمن هذا التوزيع"}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        action_type = request.data.get('action_type', 'full_sync')

        if action_type in ['pull', 'full_sync']:
            dispatch_status.is_received = True
            dispatch_status.received_at = now
            dispatch_status.is_accessible = (now >= dist.accessible_from) or (not dist.is_encrypted)
            if dispatch_status.is_accessible:
                dispatch_status.accessible_at = now

        if action_type in ['ack', 'full_sync']:
            printed_booklets = int(request.data.get('printed_booklets', 120))
            printed_sheets = int(request.data.get('printed_sheets', 120))
            attended_students = int(request.data.get('attended_students', 115))

            dispatch_status.printed_booklets_count = printed_booklets
            dispatch_status.printed_sheets_count = printed_sheets
            dispatch_status.students_attended_count = attended_students

            if request.data.get('sync_results'):
                dispatch_status.results_synced_back = True
                dispatch_status.synced_back_at = now

        dispatch_status.save()

        return Response({
            "success": True,
            "message": f"تمت محاكاة التفاعل بنجاح للمدرسة ({dispatch_status.school.name_ar})",
            "school_status": ExamSchoolDispatchStatusSerializer(dispatch_status).data
        })

    @action(detail=False, methods=['get'], url_path='export-package', permission_classes=[AllowAny])
    def export_package(self, request):
        """
        الـ API المخصص للأنظمة التعليمية المستقلة (نظام المدارس SMS ونظام الجامعات UMS)
        لسحب حزم الاختبارات المجدولة.
        GET /api/exams/distributions/export-package/?branch_no=50001
        """
        branch_no = request.query_params.get('branch_no')
        school_id = request.query_params.get('school_id')

        if not branch_no and not school_id:
            return Response({
                "success": False,
                "message": "يجب تحديد رقم الفرع (branch_no) أو معرف المدرسة (school_id)"
            }, status=status.HTTP_400_BAD_REQUEST)

        school = None
        if branch_no:
            school = Organization.objects.filter(branch_no=branch_no, is_deleted=False).first()
        elif school_id:
            school = Organization.objects.filter(id=school_id, is_deleted=False).first()

        if not school:
            return Response({
                "success": False,
                "message": "المدرسة أو الجهة المستهدفة غير مسجلة في النظام"
            }, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()

        active_distributions = ExamDistribution.objects.filter(
            organizations=school,
            dispatch_at__lte=now,
            is_deleted=False
        ).exclude(
            status=ExamDistribution.Status.CANCELLED
        ).select_related('exam__subject', 'exam__year').order_by('exam_start_at')

        dist_id = request.query_params.get('distribution_id') or request.query_params.get('dist_id')
        if dist_id:
            active_distributions = active_distributions.filter(id=dist_id)

        if not active_distributions.exists():
            return Response({
                "success": True,
                "school": {
                    "id": school.id,
                    "name_ar": school.name_ar,
                    "branch_no": school.branch_no
                },
                "total_available_exams": 0,
                "packages": [],
                "message": "لا توجد اختبارات مجدولة للتسليم حالياً لهذه المدرسة"
            })

        packages = []

        for dist in active_distributions:
            exam = dist.exam
            is_accessible = (now >= dist.accessible_from) or (not dist.is_encrypted)

            # تحديث أو تسجيل حالة الاستلام للمدرسة تلقائياً
            dispatch_status, _ = ExamSchoolDispatchStatus.objects.get_or_create(
                distribution=dist,
                school=school,
                defaults={
                    "is_received": True,
                    "received_at": now,
                    "is_accessible": is_accessible,
                    "accessible_at": now if is_accessible else None
                }
            )
            if not dispatch_status.is_received:
                dispatch_status.is_received = True
                dispatch_status.received_at = now
            if is_accessible and not dispatch_status.is_accessible:
                dispatch_status.is_accessible = True
                dispatch_status.accessible_at = now
            dispatch_status.save(update_fields=['is_received', 'received_at', 'is_accessible', 'accessible_at'])

            # تجهيز النماذج A, B, C...
            models_data = []
            versions = exam.versions.filter(is_deleted=False).prefetch_related(
                'question_orders__question__options'
            ).order_by('versionCode')

            for ver in versions:
                ver_dict = {
                    "version_code": ver.versionCode,
                    "total_questions": ver.question_orders.filter(is_deleted=False).count(),
                }

                if is_accessible:
                    questions_list = []
                    answer_key = {}

                    for qo in ver.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                        q = qo.question
                        if not q:
                            continue

                        options_data = []
                        correct_opt_char = 'A'
                        all_opts = list(q.options.filter(is_deleted=False))

                        for opt_idx, opt in enumerate(all_opts):
                            opt_char = chr(65 + opt_idx)
                            options_data.append({
                                "option_char": opt_char,
                                "text": opt.text,
                                "is_true": opt.isTrue
                            })
                            if opt.isTrue:
                                correct_opt_char = opt_char

                        if q.questionType == 'True/False' and q.isTrue is not None:
                            correct_opt_char = 'A' if q.isTrue else 'B'

                        answer_key[str(qo.orderIndex)] = correct_opt_char

                        questions_list.append({
                            "order_index": qo.orderIndex,
                            "question_id": q.id,
                            "type": q.questionType,
                            "content": q.content,
                            "default_mark": q.defaultMark,
                            "options": options_data
                        })

                    ver_dict["questions"] = questions_list
                    ver_dict["answer_key"] = answer_key
                else:
                    ver_dict["questions"] = []
                    ver_dict["lock_status"] = "محجوب مؤقتاً لدواعي السرية والأمان"
                    ver_dict["unlocks_at"] = dist.accessible_from

                models_data.append(ver_dict)

            pkg = {
                "distribution_id": dist.id,
                "dispatch_title": dist.title,
                "exam_id": exam.id,
                "unique_code": exam.uniqueCode,
                "subject": exam.subject.name_ar if exam.subject else 'عام',
                "academic_year": str(exam.year) if exam.year else '-',
                "delivery_mode": dist.delivery_mode,
                "delivery_mode_display": dist.get_delivery_mode_display(),
                "timing": {
                    "dispatch_at": dist.dispatch_at,
                    "accessible_from": dist.accessible_from,
                    "exam_start_at": dist.exam_start_at,
                    "exam_end_at": dist.exam_end_at,
                    "duration_minutes": getattr(getattr(exam, 'examSchedule', None), 'duration', 120) or 120,
                    "is_accessible_now": is_accessible,
                    "time_until_accessible_seconds": max(0, int((dist.accessible_from - now).total_seconds())) if not is_accessible else 0
                },
                "security": {
                    "is_encrypted": dist.is_encrypted,
                    "auto_unlock": dist.auto_unlock,
                    "is_locked": not is_accessible
                },
                "models": models_data,
                "omr_specs": {
                    "template": "A4_STANDARD_40Q",
                    "paper_size": "A4",
                    "dpi": 300
                },
                "notes": dist.notes
            }
            packages.append(pkg)

        return Response({
            "success": True,
            "school": {
                "id": school.id,
                "name_ar": school.name_ar,
                "branch_no": school.branch_no
            },
            "total_available_exams": len(packages),
            "packages": packages
        })

    @action(detail=False, methods=['post'], url_path='export-ack', permission_classes=[AllowAny])
    def export_ack(self, request):
        """
        إشعار التأكيد واستقبال تحديثات الطباعة والتنفيذ من نظام المدرسة المستقل
        POST /api/exams/distributions/export-ack/
        """
        dist_id = request.data.get('distribution_id')
        branch_no = request.data.get('branch_no')
        school_id = request.data.get('school_id')

        if not dist_id:
            return Response({"success": False, "message": "يجب تمرير معرف التوزيع (distribution_id)"}, status=status.HTTP_400_BAD_REQUEST)

        school = None
        if branch_no:
            school = Organization.objects.filter(branch_no=branch_no, is_deleted=False).first()
        elif school_id:
            school = Organization.objects.filter(id=school_id, is_deleted=False).first()

        if not school:
            return Response({"success": False, "message": "المدرسة غير موجودة"}, status=status.HTTP_404_NOT_FOUND)

        dispatch_status = ExamSchoolDispatchStatus.objects.filter(
            distribution_id=dist_id,
            school=school
        ).first()

        if not dispatch_status:
            return Response({"success": False, "message": "سجل التوزيع غير موجود لهذه المدرسة"}, status=status.HTTP_404_NOT_FOUND)

        if 'printed_booklets_count' in request.data:
            dispatch_status.printed_booklets_count = int(request.data['printed_booklets_count'])
        if 'printed_sheets_count' in request.data:
            dispatch_status.printed_sheets_count = int(request.data['printed_sheets_count'])
        if 'students_attended_count' in request.data:
            dispatch_status.students_attended_count = int(request.data['students_attended_count'])
        if 'results_synced_back' in request.data:
            dispatch_status.results_synced_back = bool(request.data['results_synced_back'])
            if dispatch_status.results_synced_back:
                dispatch_status.synced_back_at = timezone.now()

        dispatch_status.is_received = True
        dispatch_status.save()

        return Response({
            "success": True,
            "message": "تم تحديث حالة التنفيذ والطباعة للمدرسة بنجاح",
            "data": {
                "school": school.name_ar,
                "printed_sheets": dispatch_status.printed_sheets_count,
                "attended_students": dispatch_status.students_attended_count,
                "results_synced_back": dispatch_status.results_synced_back
            }
        })
