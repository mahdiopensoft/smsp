import pathlib
import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from rest_framework.test import APIClient

from academic.models.common.AcademicYear import AcademicYear
from academic.models.common.Subject import Subject
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from exams.serializers.StudentExamRegistration import StudentExamRegistrationSerializer
from OpenSoftCoreV41.usermanager.models.UserType import UserType

User = get_user_model()


@pytest.mark.django_db(databases=['default', 'screen', 'log'])
class TestSecurityHardening:

    def test_sensitive_and_allmvs_endpoints_require_authentication(self):
        client = APIClient()
        protected_get_endpoints = [
            "/api/exams/exam-versions/all/",
            "/api/exams/exam-versions/",
            "/api/exams/exams/all/",
            "/api/bank/questions/",
            "/api/bank/answers/all/",
            "/api/submissions/submissions/all/",
            "/api/omr/ai-metrics/",
            "/api/exams/distributions/resolve-hierarchy/",
            "/api/academic/organizations/governorates/",
        ]
        for url in protected_get_endpoints:
            resp = client.get(url)
            assert resp.status_code in (401, 403), f"{url} returned {resp.status_code} unauthenticated"

        resp_ack = client.post("/api/exams/distributions/export-ack/", {}, format="json")
        assert resp_ack.status_code in (401, 403)

    def test_exam_version_serializer_excludes_answer_key_snapshot(self):
        user_type, _ = UserType.objects.get_or_create(id=3, defaults={'name_ar': 'موظف', 'name_en': 'Staff'})
        staff_user = User.objects.create(
            username="sec_staff_ver",
            is_staff=True,
            is_active=True,
            fk_user_type=user_type,
        )
        year = AcademicYear.objects.create(hijri_year="1448", gregorian_year="2026", is_current=True)
        subject = Subject.objects.create(name_ar="أمن المعلومات", subject_code="SEC-101")
        exam = Exam.objects.create(title="اختبار الحماية", uniqueCode="EXAM-SEC-01", year=year, subject=subject)
        version = ExamVersion.objects.create(
            exam=exam,
            versionCode="A",
            key_status=ExamVersion.KeyStatus.FROZEN,
            answer_key_snapshot={"questions": {"1": {"correct_choice": "B", "assigned_weight": 2.0}}},
            answer_key_hash="0" * 64,
        )

        client = APIClient()
        client.force_authenticate(user=staff_user)
        resp = client.get("/api/exams/exam-versions/all/")
        assert resp.status_code == 200
        payload = resp.json()
        items = payload.get("data", payload) if isinstance(payload, dict) else payload
        assert any(item["id"] == version.id for item in items)
        for item in items:
            assert "answer_key_snapshot" not in item

    def test_student_registration_serializer_hides_secret_number_for_non_control_users(self):
        student_type, _ = UserType.objects.get_or_create(id=2, defaults={'name_ar': 'طالب', 'name_en': 'Student'})
        staff_type, _ = UserType.objects.get_or_create(id=3, defaults={'name_ar': 'موظف', 'name_en': 'Staff'})

        regular_user = User.objects.create(username="sec_reg_student", is_active=True, fk_user_type=student_type)
        control_user = User.objects.create(
            username="sec_ctrl_officer",
            is_staff=True,
            is_active=True,
            fk_user_type=staff_type,
        )

        year = AcademicYear.objects.create(hijri_year="1448", gregorian_year="2026", is_current=True)
        subject = Subject.objects.create(name_ar="جبر", subject_code="ALG-201")
        exam = Exam.objects.create(title="اختبار الرقم السري", uniqueCode="EXAM-SEC-02", year=year, subject=subject)
        version = ExamVersion.objects.create(exam=exam, versionCode="A")
        reg = StudentExamRegistration.objects.create(
            student=regular_user,
            examVersion=version,
            seatNumber="554433",
            secretNumber="SEC-9876",
        )

        rf = RequestFactory()
        req_regular = rf.get("/")
        req_regular.user = regular_user
        data_regular = StudentExamRegistrationSerializer(reg, context={"request": req_regular}).data
        assert "secretNumber" not in data_regular
        assert data_regular["exam_version_code"] == "نموذج A"

        req_control = rf.get("/")
        req_control.user = control_user
        data_control = StudentExamRegistrationSerializer(reg, context={"request": req_control}).data
        assert data_control["secretNumber"] == "SEC-9876"
        assert data_control["exam_version_code"] == "نموذج A"

    def test_bank_xss_middleware_blocks_xss_and_allows_benign_sql_html(self):
        client = APIClient()

        resp_script = client.post(
            "/api/bank/questions/",
            {"content": "<p>Test <script>alert(1)</script></p>"},
            format="json",
        )
        assert resp_script.status_code == 400

        resp_onerror = client.post(
            "/api/bank/questions/",
            {"content": '<img src=x onerror=alert(1)>'},
            format="json",
        )
        assert resp_onerror.status_code == 400

        resp_benign = client.post(
            "/api/bank/questions/",
            {"content": "<p>ما ناتج <b>SELECT * FROM t;</b> &nbsp; $x^2$</p>"},
            format="json",
        )
        assert resp_benign.status_code in (401, 403)

    def test_sync_setting_contains_no_hardcoded_secrets(self):
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        sync_file = repo_root / "backend" / "config" / "settings" / "sync_setting.py"
        text = sync_file.read_text(encoding="utf-8")
        assert "BEGIN RSA PRIVATE KEY" not in text
        assert "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVkt" not in text
        assert "b30d1f4437513f44" not in text
