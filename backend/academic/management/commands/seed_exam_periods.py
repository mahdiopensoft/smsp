from django.core.management.base import BaseCommand
from academic.models.common.ExamPeriod import ExamPeriod

class Command(BaseCommand):
    help = 'Seeds the database with default Exam Periods'

    def handle(self, *args, **kwargs):
        periods = [
            {
                "id": 1,
                "name_ar": "اختبار نصف الفصل الدراسي الأول",
                "name_en": "First Semester Midterm",
                "target_terms": [1],
                "order": 1
            },
            {
                "id": 2,
                "name_ar": "اختبار نهاية الفصل الدراسي الأول",
                "name_en": "First Semester Final",
                "target_terms": [1],
                "order": 2
            },
            {
                "id": 3,
                "name_ar": "اختبار نصف الفصل الدراسي الثاني",
                "name_en": "Second Semester Midterm",
                "target_terms": [2],
                "order": 3
            },
            {
                "id": 4,
                "name_ar": "اختبار نهاية العام الدراسي",
                "name_en": "End of Year Final",
                "target_terms": [1, 2],
                "order": 4
            }
        ]

        for p_data in periods:
            period, created = ExamPeriod.objects.update_or_create(
                id=p_data["id"],
                defaults={
                    "name_ar": p_data["name_ar"],
                    "name_en": p_data["name_en"],
                    "target_terms": p_data["target_terms"],
                    "order": p_data["order"],
                    "is_active": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Exam Period: {period.name_ar}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated Exam Period: {period.name_ar}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded all Exam Periods!'))
