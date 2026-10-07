from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404

from exams.models.ExamDistribution import ExamDistribution
from exams.models.ExamSchoolDispatchStatus import ExamSchoolDispatchStatus
from OpenSoftCoreV41.common.models.Branch import Organization
from exams.models.ExamVersion import ExamVersion

class ExamExportPackageAPI(APIView):
    """
    الـ API المخصص للأنظمة التعليمية المستقلة (نظام المدارس SMS ونظام الجامعات UMS)
    لسحب حزم الاختبارات المجدولة وتأكيد الاستلام والطباعة.
    
    الاستدعاء:
      GET /api/exams/export/package/?branch_no=50001
      GET /api/exams/export/package/?school_id=15
    """
    def get(self, request):
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

        # البحث عن التوزيعات المتاحة لهذه المدرسة والتي حان وقت إرسالها (dispatch_at <= now)
        # ولم تنتهِ بعد (exam_end_at >= now)
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
            versions_qs = exam.versions.filter(is_deleted=False)

            # تصفية النماذج بحسب تعيين المناطق الجغرافية للجهة المستهدفة إن وجدت
            if hasattr(exam, 'model_region_assignments') and exam.model_region_assignments.filter(is_deleted=False).exists():
                from django.db.models import Q
                matching_assignments = exam.model_region_assignments.filter(
                    is_deleted=False
                ).filter(
                    Q(scope_level='school', organization=school) |
                    Q(scope_level='directorate', directorate_id=school.fk_directorate_id) |
                    Q(scope_level='directorate', organization_id=school.fk_parent_organization_id) |
                    Q(scope_level='governorate', governorate_id=school.fk_governorate_id) |
                    Q(scope_level='region', region_id=getattr(school, 'fk_region_id', None))
                )
                if matching_assignments.exists():
                    assigned_indices = list(matching_assignments.values_list('model_group_index', flat=True).distinct())
                    if assigned_indices:
                        filtered_versions = versions_qs.filter(model_group_index__in=assigned_indices)
                        if filtered_versions.exists():
                            versions_qs = filtered_versions

            versions = versions_qs.prefetch_related(
                'question_orders__question__options'
            ).order_by('versionCode')

            for ver in versions:
                ver_dict = {
                    "version_code": ver.versionCode,
                    "model_group_index": getattr(ver, 'model_group_index', 0),
                    "difficulty_profile": getattr(ver, 'difficulty_profile', 'mixed'),
                    "difficulty_profile_display": ver.get_difficulty_profile_display() if hasattr(ver, 'get_difficulty_profile_display') else getattr(ver, 'difficulty_profile', 'mixed'),
                    "difficulty_distribution": getattr(ver, 'difficulty_distribution', None),
                    "total_questions": ver.question_orders.filter(is_deleted=False).count(),
                }

                if is_accessible:
                    # تفاصيل الأسئلة والخيارات ومفتاح التصحيح متاحة للطباعة
                    questions_list = []
                    answer_key = {}

                    for qo in ver.question_orders.filter(is_deleted=False).order_by('orderIndex'):
                        q = qo.question
                        if not q:
                            continue

                        # الخيارات
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

                        # في حال أسئلة الصح والخطأ
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
                    # لا تزال الأسئلة محجوبة ومؤمنة حتى موعد الإتاحة
                    ver_dict["questions"] = []
                    ver_dict["lock_status"] = "محجوب مؤقتاً لدواعي السرية والأمان"
                    ver_dict["unlocks_at"] = dist.accessible_from

                models_data.append(ver_dict)

            # تجميع كائن الحزمة الكامل
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


class ExamExportPackageAckAPI(APIView):
    """
    إشعار التأكيد واستقبال تحديثات الطباعة والتنفيذ من نظام المدرسة المستقل
    POST /api/exams/export/package/ack/
    Body:
    {
        "distribution_id": 1,
        "branch_no": "50001",
        "printed_booklets_count": 150,
        "printed_sheets_count": 150,
        "students_attended_count": 148,
        "results_synced_back": false
    }
    """
    def post(self, request):
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
