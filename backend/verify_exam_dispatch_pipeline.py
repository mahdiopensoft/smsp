"""
سند فحص وتأكيد سيناريو تصدير وتوزيع الاختبارات المجدول للمدارس (SMS)
التحقق من:
1. إعدادات التسليم: طباعة كراسات + أوراق إجابة OMR
2. الحجب التلقائي للأسئلة قبل موعد الإتاحة
3. الفتح التلقائي للأسئلة بمجرد حلول موعد الإتاحة (auto_unlock)
4. إشعار استلام وطباعة أوراق OMR من المدرسة وتحديث لوحة المتابعة الحية
"""
import os
import sys
import django

# إعداد بيئة جانغو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIRequestFactory

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.ExamDistribution import ExamDistribution
from exams.models.ExamSchoolDispatchStatus import ExamSchoolDispatchStatus
from exams.apis.ExamDistributionMVS import ExamDistributionMVS
from OpenSoftCoreV41.common.models.Branch import Organization

def run_verification():
    print("========================================================================")
    print("🚀 بدء اختبار سيناريو توزيع وتصدير الاختبارات للمدارس المستقلة (SMS)")
    print("========================================================================")

    # 1. التأكد من وجود مدرسة في الهيكلية
    school = Organization.objects.filter(is_deleted=False, company_level=50).first()
    if not school:
        print("⚠️ لم يتم العثور على أي مدرسة ذات (company_level=50). يرجى تشغيل seed_yemen_educational_hierarchy.py أولاً.")
        return

    print(f"🏫 المدرسة المختارة للاختبار: {school.name_ar} (رقم الفرع: {school.branch_no})")

    # 2. التأكد من وجود اختبار معتمد
    exam = Exam.objects.filter(is_deleted=False, versions__isnull=False).distinct().first() or Exam.objects.filter(is_deleted=False).first()
    if not exam:
        print("⚠️ لم يتم العثور على أي اختبار في جدول exams_exam.")
        return

    # التأكد من وجود نموذج للاختبار
    created_test_version = False
    if not exam.versions.filter(is_deleted=False).exists():
        ExamVersion.objects.create(exam=exam, versionCode='A')
        created_test_version = True

    print(f"📝 الاختبار المعتمد: {exam.title} (الرمز: {exam.uniqueCode})")

    now = timezone.now()
    factory = APIRequestFactory()

    # 3. إنشاء مهمة توزيع تجريبية (موعد الإتاحة في المستقبل: مغلق ومحجوب)
    print("\n--- [المرحلة 1: إنشاء مهمة توزيع مجدولة] ---")
    dist = ExamDistribution.objects.create(
        exam=exam,
        title=f"اختبار تجريبي لنظام SMS - {exam.title}",
        target_level=ExamDistribution.TargetLevel.SCHOOL,
        target_system=ExamDistribution.TargetSystem.SCHOOL,
        delivery_mode=ExamDistribution.DeliveryMode.PRINTED_OMR,
        dispatch_at=now - timedelta(minutes=10), # تم إرسال الحزمة
        accessible_from=now + timedelta(hours=1), # تفتح الأسئلة بعد ساعة (مغلقة حالياً)
        exam_start_at=now + timedelta(hours=2),
        exam_end_at=now + timedelta(hours=4),
        is_encrypted=True,
        auto_unlock=True,
        notes="يرجى استخدام ورق أبيض عالي الجودة لطباعة أوراق إجابة OMR",
        status=ExamDistribution.Status.SCHEDULED
    )
    dist.organizations.add(school)
    ExamSchoolDispatchStatus.objects.create(
        distribution=dist,
        school=school,
        is_received=False,
        is_accessible=False
    )
    print(f"✅ تم إنشاء التوزيع (ID: {dist.id}) بنمط: {dist.get_delivery_mode_display()}")
    print(f"🔒 موعد فك الحجب والإتاحة التلقائية: {dist.accessible_from}")

    try:
        # 4. محاكاة استدعاء نظام المدرسة قبل موعد الإتاحة
        print("\n--- [المرحلة 2: فحص استدعاء المدرسة قبل موعد الإتاحة (منع التسريب)] ---")
        export_action = ExamDistributionMVS.as_view({'get': 'export_package'})
        req1 = factory.get(f'/api/exams/distributions/export-package/?branch_no={school.branch_no}&distribution_id={dist.id}')
        res1 = export_action(req1)
        res1_data = res1.data

        assert res1.status_code == 200, f"Expected 200, got {res1.status_code}"
        pkg1 = next((p for p in res1_data.get('packages', []) if p.get('distribution_id') == dist.id), None)
        assert pkg1 is not None, f"لم يتم العثور على حزمة مهمة التوزيع (ID: {dist.id}) في استجابة المخدم!"
        assert pkg1['security']['is_locked'] == True, "يجب أن تكون الحزمة مقفلة ومحجوبة الأسئلة!"
        assert pkg1['timing']['is_accessible_now'] == False, "يجب أن تكون غير متاحة الآن"
        
        # التأكد من حجب الأسئلة في النماذج
        for m in pkg1['models']:
            assert len(m['questions']) == 0, "يجب أن تكون قائمة الأسئلة فارغة قبل موعد الإتاحة!"
            assert "محجوب" in m.get('lock_status', ''), "يجب ظهور حالة الحجب المؤقت"

        print("✅ نجح الفحص: الأسئلة محجوبة ومحمية بنجاح لمنع التسريب قبل الموعد المحدد.")
        lock_msg = pkg1['models'][0].get('lock_status') if pkg1['models'] else "محجوب مؤقتاً لدواعي السرية والأمان"
        print(f"ℹ️ نص رسالة القفل: {lock_msg}")

        # 5. محاكاة وصول موعد الإتاحة التلقائي (auto_unlock)
        print("\n--- [المرحلة 3: فحص الفتح التلقائي عند حلول موعد الإتاحة (Auto Unlock)] ---")
        dist.accessible_from = now - timedelta(minutes=5) # حلول الموعد
        dist.save()

        req2 = factory.get(f'/api/exams/distributions/export-package/?branch_no={school.branch_no}&distribution_id={dist.id}')
        res2 = export_action(req2)
        res2_data = res2.data

        assert res2.status_code == 200, f"Expected 200, got {res2.status_code}"
        pkg2 = next((p for p in res2_data.get('packages', []) if p.get('distribution_id') == dist.id), None)
        assert pkg2 is not None, f"لم يتم العثور على حزمة مهمة التوزيع (ID: {dist.id}) في استجابة المخدم!"
        assert pkg2['security']['is_locked'] == False, "يجب أن تفك الحزمة تلقائياً!"
        assert pkg2['timing']['is_accessible_now'] == True, "يجب أن تكون متاحة الآن للطباعة"
        print("✅ نجح الفحص: تم فتح محتوى الأسئلة تلقائياً بمجرد حلول الموعد المحدد.")
        print(f"📄 مواصفات قالب الـ OMR المرفقة: {pkg2.get('omr_specs')}")

        # 6. محاكاة قيام نظام المدرسة بإشعار استلام وطباعة أوراق OMR
        print("\n--- [المرحلة 4: إشعار استلام وطباعة أوراق OMR وحضور الطلاب] ---")
        ack_action = ExamDistributionMVS.as_view({'post': 'export_ack'})
        ack_payload = {
            "distribution_id": dist.id,
            "branch_no": school.branch_no,
            "printed_booklets_count": 120,
            "printed_sheets_count": 120,
            "students_attended_count": 118,
            "results_synced_back": False
        }
        req3 = factory.post('/api/exams/distributions/export-ack/', ack_payload, format='json')
        res3 = ack_action(req3)
        assert res3.status_code == 200, f"Expected 200, got {res3.status_code}"
        print("✅ نجح الفحص: استقبل النظام المركزي إشعار طباعة 120 كراسة و 120 ورقة OMR.")

        # 7. فحص لوحة المتابعة الميدانية الحية (Live Status API)
        print("\n--- [المرحلة 5: فحص لوحة المتابعة الحية للوزارة/الكنترول المركزي] ---")
        live_status_action = ExamDistributionMVS.as_view({'get': 'live_status'})
        req4 = factory.get(f'/api/exams/distributions/{dist.id}/live-status/')
        res4 = live_status_action(req4, pk=dist.id)
        res4_data = res4.data

        assert res4.status_code == 200
        kpis = res4_data['kpis']
        print(f"📊 إجمالي المدارس المستهدفة: {kpis['total_schools']}")
        print(f"📥 المدارس التي استلمت الحزمة: {kpis['received_schools']} ({kpis['received_percentage']}%)")
        print(f"🔓 المدارس التي فكت التشفير: {kpis['accessible_schools']}")
        print(f"🖨️ إجمالي أوراق OMR المطبوعة: {kpis['total_printed_sheets']}")
        print(f"👥 إجمالي الطلاب الحاضرين: {kpis['total_attended_students']}")

        assert kpis['total_printed_sheets'] == 120
        assert kpis['total_attended_students'] == 118
        print("✅ نجحت المتابعة الحية وسجلت طباعة وحضور الطلاب بدقة.")

        # 8. فحص تنزيل الحزمة الكاملة Offline Package
        print("\n--- [المرحلة 6: فحص تنزيل حزمة التصدير الرسمية كـ JSON] ---")
        download_action = ExamDistributionMVS.as_view({'get': 'download_package'})
        req5 = factory.get(f'/api/exams/distributions/{dist.id}/download-package/')
        res5 = download_action(req5, pk=dist.id)
        assert res5.status_code == 200
        assert "package" in res5.data
        assert res5.data['package']['unique_code'] == exam.uniqueCode
        print(f"✅ نجح تنزيل الحزمة: الرمز ({res5.data['package']['unique_code']}) وعدد النماذج ({len(res5.data['package']['models'])}).")

        # 9. فحص محاكي التفاعل الميداني للمدرسة simulate_school_sync
        print("\n--- [المرحلة 7: فحص محاكي تفاعل المدارس (School Simulator)] ---")
        sim_action = ExamDistributionMVS.as_view({'post': 'simulate_school_sync'})
        sim_req = factory.post(f'/api/exams/distributions/{dist.id}/simulate-school-sync/', {
            "school_id": school.id,
            "action_type": "full_sync",
            "printed_booklets": 150,
            "printed_sheets": 150,
            "attended_students": 145,
            "sync_results": True
        }, format='json')
        sim_res = sim_action(sim_req, pk=dist.id)
        assert sim_res.status_code == 200
        assert sim_res.data['school_status']['printed_sheets_count'] == 150
        print("✅ نجح محاكي المدارس وتم تحديث الحضور والطباعة إلى 150.")

        # 10. فحص فك الحجب الفوري Emergency Force Unlock
        print("\n--- [المرحلة 8: فحص فك الحجب الفوري لحالات الطوارئ] ---")
        unlock_action = ExamDistributionMVS.as_view({'post': 'force_unlock'})
        unlock_req = factory.post(f'/api/exams/distributions/{dist.id}/force-unlock/')
        unlock_res = unlock_action(unlock_req, pk=dist.id)
        assert unlock_res.status_code == 200
        print("✅ نجح فك الحجب الفوري لحالات الطوارئ.")

        # 11. فحص منع تكرار وازدواجية تصدير الاختبار النشط Duplicate Export Guard
        print("\n--- [المرحلة 9: فحص منع ازدواجية وتكرار تصدير الاختبار النشط] ---")
        create_action = ExamDistributionMVS.as_view({'post': 'create_dispatch'})
        duplicate_req = factory.post('/api/exams/distributions/create-dispatch/', {
            'exam_id': exam.id,
            'title': f'محاولة تصدير مكررة للاختبار {exam.title}',
            'selected_school_ids': [school.id]
        }, format='json')
        duplicate_res = create_action(duplicate_req)
        assert duplicate_res.status_code == 400, f"Expected 400 Bad Request on duplicate export, got {duplicate_res.status_code}"
        assert duplicate_res.data['success'] == False
        assert "لا يمكن تصدير هذا الاختبار مجدداً" in duplicate_res.data['message']
        print(f"✅ نجح صمام الأمان لمنع التكرار: {duplicate_res.data['message']}")

        # 12. فحص إلغاء مهمة التوزيع Cancel Dispatch
        print("\n--- [المرحلة 10: فحص إلغاء مهمة التوزيع] ---")
        cancel_action = ExamDistributionMVS.as_view({'post': 'cancel_dispatch'})
        cancel_req = factory.post(f'/api/exams/distributions/{dist.id}/cancel-dispatch/', {'reason': 'اختبار تجريبي للإلغاء'}, format='json')
        cancel_res = cancel_action(cancel_req, pk=dist.id)
        assert cancel_res.status_code == 200
        assert cancel_res.data['status'] == 'cancelled'
        print("✅ نجح إلغاء مهمة التوزيع وحجب الأسئلة.")

        print("\n🎉 نجحت جميع مراحل الفحص الميداني الـ 10 بنسبة 100%!")

    finally:
        # تنظيف بيانات الاختبار التجريبي
        ExamSchoolDispatchStatus.objects.filter(distribution=dist).delete()
        dist.hard_delete() if hasattr(dist, 'hard_delete') else dist.delete()
        if created_test_version:
            ExamVersion.objects.filter(exam=exam, versionCode='A').delete()
        print("\n🧹 تم تنظيف السجلات التجريبية بأمان.")

if __name__ == '__main__':
    run_verification()
