#!/usr/bin/env python3
"""
Setup Script: Create an Authentic, Official 50-Question 9th-Grade Yemeni History Exam for Sana'a
with 4 Ministerial Models (A, B, C, D) and Balanced Answer Keys (A/B/C/D & T/F).

Structure per model:
- 50 Questions Total:
  * 20 Questions True/False (1-20)
  * 30 Questions Multiple Choice (21-50, 4 options each)
- 4 Official Ministerial Models:
  * Model A (النموذج أ)
  * Model B (النموذج ب)
  * Model C (النموذج ج)
  * Model D (النموذج د)
- Balanced Answer Key Distribution for MCQ:
  * ~8 Questions correct answer A (أ)
  * ~8 Questions correct answer B (ب)
  * ~7 Questions correct answer C (ج)
  * ~7 Questions correct answer D (د)
- 40 Registered Students from Sana'a schools distributed across Models A, B, C, D.
"""

import os
import sys
import datetime
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from django.apps import apps

# Models
AcademicYear = apps.get_model('academic', 'AcademicYear')
SchoolStage = apps.get_model('academic', 'SchoolStage')
SchoolLevel = apps.get_model('academic', 'SchoolLevel')
SchoolClassTrack = apps.get_model('academic', 'SchoolClassTrack')
Subject = apps.get_model('academic', 'Subject')
SchoolSubject = apps.get_model('academic', 'SchoolSubject')
SchoolClassSubject = apps.get_model('academic', 'SchoolClassSubject')
Unit = apps.get_model('academic', 'Unit')
Lesson = apps.get_model('academic', 'Lesson')
Student = apps.get_model('academic', 'Student')
AcademicOrganization = apps.get_model('academic', 'Organization')

Question = apps.get_model('bank', 'Question')
Answer = apps.get_model('bank', 'Answer')

Exam = apps.get_model('exams', 'Exam')
ExamVersion = apps.get_model('exams', 'ExamVersion')
ExamQuestionOrder = apps.get_model('exams', 'ExamQuestionOrder')
ExamSchedule = apps.get_model('exams', 'ExamSchedule')
StudentExamRegistration = apps.get_model('exams', 'StudentExamRegistration')

Governorate = apps.get_model('common', 'Governorate')
Directorate = apps.get_model('common', 'Directorate')
Country = apps.get_model('common', 'Country')
User = apps.get_model('usermanager', 'User')


@transaction.atomic
def run():
    print("=" * 75)
    print("بدء إنشاء وتحديث الاختبار الوزاري لمادة التاريخ - الصف التاسع - أمانة العاصمة")
    print("المواصفات: 50 سؤالاً (20 صح/خطأ + 30 خيارات) | 4 نماذج (أ، ب، ج، د) | إجابات متوازنة")
    print("=" * 75)

    admin_user = User.objects.filter(id=1).first() or User.objects.first()

    # 1. السنة الدراسية
    academic_year, _ = AcademicYear.objects.get_or_create(
        hijri_year="1446",
        gregorian_year="2024-2025",
        defaults={"is_current": True, "is_active": True}
    )
    academic_year.is_current = True
    academic_year.is_active = True
    academic_year.save()

    # 2. النطاق الجغرافي
    yemen = Country.objects.first()
    sanaa_gov = Governorate.objects.filter(id=1).first() or Governorate.objects.filter(name_ar__icontains="الامانه").first()
    tahrir_dir = Directorate.objects.filter(id=7).first() or Directorate.objects.filter(name_ar__icontains="التحرير").first()

    # 3. المرحلة والصف والمسار
    grade9_level = SchoolLevel.objects.get(id=9)
    class_track = SchoolClassTrack.objects.filter(level_id=9).first()

    # 4. المادة الوزارية
    school_subject = SchoolSubject.objects.filter(id=9).first() or SchoolSubject.objects.filter(name_ar="التاريخ").first()
    history_subject, _ = Subject.objects.get_or_create(
        name_ar="التاريخ",
        defaults={
            "name_en": "History",
            "subject_code": "HIST-09",
            "is_ministerial": True,
            "is_active": True,
            "credit_hours": 3,
        }
    )
    history_subject.is_ministerial = True
    history_subject.save()

    class_subject, _ = SchoolClassSubject.objects.get_or_create(
        class_track=class_track,
        subject=history_subject,
        defaults={"school_subject": school_subject, "max_score": 100.0, "min_score": 50.0, "is_active": True}
    )

    # 5. الوحدات الدراسية والدروس
    units_def = [
        ("الوحدة الأولى: حضارات اليمن القديمة ونظام الري", [
            "مملكة سبأ وبناء سد مأرب التاريخي",
            "مملكة معين والتجارة العالمية والخط المسند",
            "مملكة حمير وتوحيد أرجاء اليمن (شمر يهرعش)",
            "مملكة قتبان وحضرموت والموانئ القديمة"
        ]),
        ("الوحدة الثانية: اليمن في العصر الإسلامي المبارك", [
            "دخول أهل اليمن في الإسلام طوعاً وإرسال معاذ بن جبل والإمام علي",
            "دور القبائل والجيوش اليمنية في الفتوحات الإسلامية الكبرى",
            "بناء الجوامع التاريخية في صنعاء والجند وزبيد"
        ]),
        ("الوحدة الثالثة: الدول اليمنية المستقلة في العصر الإسلامي", [
            "الدولة الزيادية والدولة اليعفرية في هضبة اليمن",
            "الدولة الصليحية وحكم السيدة الحرة أروى بنت أحمد",
            "الدولة الرسولية وعصر النهضة العلمية والمعمارية في تعز",
            "الدولة الطاهرية وعمارتها في رداع وجبن"
        ]),
        ("الوحدة الرابعة: كفاح الشعب اليمني ضد الغزو والاستعمار", [
            "صمود أهل اليمن وعدن ضد الحملات والغزو البرتغالي",
            "المقاومة الوطنية اليمنية بقيادة المطهر بن شرف الدين ضد العثمانيين",
            "مقاومة الاحتلال البريطاني في جنوب اليمن"
        ])
    ]

    all_lessons = []
    for u_order, (u_name, lessons) in enumerate(units_def, start=1):
        unit_obj, _ = Unit.objects.get_or_create(
            name_ar=u_name,
            class_subject=class_subject,
            defaults={"order": u_order, "is_active": True}
        )
        for l_order, l_name in enumerate(lessons, start=1):
            lesson_obj, _ = Lesson.objects.get_or_create(
                name_ar=l_name,
                unit=unit_obj,
                subject=history_subject,
                defaults={"order": l_order, "is_active": True}
            )
            all_lessons.append(lesson_obj)

    print(f"[1] تم تجهيز المنهج الوزاري: 4 وحدات و {len(all_lessons)} دروس رسمية")

    # 6. بنك الأسئلة: 50 سؤالاً حقيقياً ودقيقاً
    # -------------------------------------------------------------
    # القسم الأول: 20 سؤال صح / خطأ (12 صح و 8 خطأ، متوازنة)
    # -------------------------------------------------------------
    tf_data = [
        (1, "تأسست مملكة سبأ في مأرب واعتمد اقتصادها على الزراعة المروية والتجارة عبر طريق البخور.", True, all_lessons[0], "Remember"),
        (2, "اتخذت الدولة المعينية من مدينة ظفار في يريم عاصمة رئيسية لها منذ نشأتها الأولى.", False, all_lessons[1], "Remember"),
        (3, "قاد المكرب السبئي (كرب إيل وتر) حملات عسكرية وحد بها أرجاء اليمن ولقب نفسه بـ (ملك سبأ وذي ريدان).", True, all_lessons[0], "Understand"),
        (4, "انهار سد مأرب القديم فجأة بسبب زلزال بحري ضرب السواحل اليمنية.", False, all_lessons[0], "Understand"),
        (5, "كانت مملكة قتبان تسيطر على وادي بيحان وتتحكم في ممرات القوافل التجارية ونظم الأسواق.", True, all_lessons[3], "Understand"),
        (6, "دخل أهل اليمن الإسلام بعد معارك عنيفة وحروب طويلة خاضها المسلمون لفتح مدنهم.", False, all_lessons[4], "Remember"),
        (7, "اتخذت الدولة الصليحية في عهد الملكة أروى بنت أحمد الصليحي من مدينة جبلة عاصمة لحكمها.", True, all_lessons[8], "Remember"),
        (8, "انتصرت الحملة البرتغالية على مدينة عدن عام 1513م بفضل التحالف مع العثمانيين.", False, all_lessons[11], "Understand"),
        (9, "تعتبر الدولة الرسولية أطول وأزهى الدول الإسلامية المستقلة حكماً لليمن وعاصمتها مدينة تعز.", True, all_lessons[9], "Understand"),
        (10, "اتخذ الإمام المطهر بن شرف الدين من حصن ثلا وقلعة كوكبان مراكز حصينة للمقاومة الوطنية ضد العثمانيين.", True, all_lessons[12], "Apply"),
        (11, "شيدت الدولة الطاهرية مدرسة العامرية الشهيرة بمدينة رداع كتحفة معمارية إسلامية بارزة.", True, all_lessons[10], "Remember"),
        (12, "كان يطلق على حكام سبأ الأوائل في العصر الأول لقب (ملوك) ثم تحول إلى لقب (مكارب).", False, all_lessons[0], "Understand"),
        (13, "أرسل الرسول صلى الله عليه وسلم الصحابي معاذ بن جبل معلماً وقاضياً لأهل اليمن وأسس جامع الجند بتعز.", True, all_lessons[4], "Remember"),
        (14, "استسلمت قبائل حمير للغزو الحبشي دون أي مقاومة تذكر بقيادة ذي نواس.", False, all_lessons[2], "Understand"),
        (15, "هاجرت قبائل يمنية شهيرة كالأوس والخزرج إلى يثرب (المدينة المنورة) إثر تدهور سد مأرب وسيل العرم.", True, all_lessons[0], "Understand"),
        (16, "اقتصر دور اليمنيين في الفتوحات الإسلامية على الإمداد المالي دون المشاركة الميدانية في الجيوش.", False, all_lessons[5], "Understand"),
        (17, "اتخذت الدولة الزيادية من مدينة زبيد أول عاصمة لها في تهامة خلال العصر العباسي.", True, all_lessons[7], "Remember"),
        (18, "بني الجامع الكبير بصنعاء بعد وفاة الرسول صلى الله عليه وسلم بقرنين بأمر من هارون الرشيد.", False, all_lessons[6], "Remember"),
        (19, "كان لنقود الدولة الرسولية رواج تجاري واسع في موانئ البحر الأحمر والمحيط الهندي.", True, all_lessons[9], "Analyze"),
        (20, "احتل الاستعمار البريطاني مدينة وميناء عدن في 19 يناير 1839م بحجة حادثة السفينة دريا دولت.", True, all_lessons[13], "Remember"),
    ]

    # -------------------------------------------------------------
    # القسم الثاني: 30 سؤال اختيار من متعدد (خيارات أ، ب، ج، د)
    # موزعة بدقة متساوية عبر الخيارات (أ=8, ب=8, ج=7, د=7)
    # -------------------------------------------------------------
    mcq_data = [
        # --- أسئلة إجابتها الصحيحة: أ (A) ---
        (21, "السد التاريخي الشهير الذي شيده السبئيون لحجز مياه السيول بين جبلي البلق الأيمن والأيسر هو:",
         all_lessons[0], "Remember", [
             ("سد مأرب العظيم", True),
             ("سد الخانق بصعدة", False),
             ("سد رصابة بذمار", False),
             ("سد مرخة بشبوة", False),
         ]),
        (22, "الصحابي الجليل الذي أرسله النبي صلى الله عليه وسلم قاضياً ومعلماً لأهل اليمن وأسس جامع الجند هو:",
         all_lessons[4], "Remember", [
             ("معاذ بن جبل الأنصاري", True),
             ("أبو موسى الأشعري", False),
             ("عمار بن ياسر", False),
             ("سلمان الفارسي", False),
         ]),
        (23, "أول ملك حميري لقب بـ (ملك سبأ وذي ريدان وحضرموت ويمنات) موحداً لجميع أقاليم اليمن القديم هو:",
         all_lessons[2], "Analyze", [
             ("شمر يهرعش", True),
             ("أسعد الكامل (أبو كرب)", False),
             ("كرب إيل وتر", False),
             ("ذو رعين", False),
         ]),
        (24, "تتكون الأبجدية الأصلية لخط المسند اليمني القديم من:",
         all_lessons[1], "Remember", [
             ("29 حرفاً مسندياً", True),
             ("22 حرفاً", False),
             ("28 حرفاً", False),
             ("26 حرفاً", False),
         ]),
        (25, "الميناء التاريخي الذي اشتهر عالمياً بتصدير أفخر أنواع البن اليمني إلى كافة بقاع الأرض هو:",
         all_lessons[9], "Remember", [
             ("ميناء المخا (موكا)", True),
             ("ميناء نشطون", False),
             ("ميناء بلحاف", False),
             ("ميناء الصليف", False),
         ]),
        (26, "المعبد السبئي الدائري العظيم في مأرب المخصص للإله (المقه) ويعرف بـ (محرم بلقيس) هو:",
         all_lessons[0], "Understand", [
             ("معبد أوام", True),
             ("معبد برآن", False),
             ("معبد نكرح", False),
             ("معبد وعال", False),
         ]),
        (27, "تقع مدينة جبلة التاريخية التي جعلتها الملكة أروى بنت أحمد الصليحي عاصمة لحكمها في محافظة:",
         all_lessons[8], "Remember", [
             ("محافظة إب", True),
             ("محافظة تعز", False),
             ("محافظة لحج", False),
             ("محافظة ريمة", False),
         ]),
        (28, "القبيلة اليمنية العريقة التي ينتمي إليها الصحابي الجليل عمار بن ياسر أول شهداء الإسلام والداه هي:",
         all_lessons[5], "Understand", [
             ("قبيلة عنس (مذحج)", True),
             ("قبيلة همدان", False),
             ("قبيلة الأزد", False),
             ("قبيلة كندة", False),
         ]),

        # --- أسئلة إجابتها الصحيحة: ب (B) ---
        (29, "العاصمة التاريخية لمملكة معين التي اشتهرت بنشاطها التجاري الواسع في الجوف هي:",
         all_lessons[1], "Remember", [
             ("ظفار", False),
             ("قرناو", True),
             ("صرواح", False),
             ("تمنع", False),
         ]),
        (30, "الحاكمة اليمنية البارزة التي لقبت بـ (السيدة الحرة) وشهد اليمن في عهدها نهضة زراعية وعمرانية كبرى هي:",
         all_lessons[8], "Remember", [
             ("الملكة بلقيس", False),
             ("الملكة أروى بنت أحمد الصليحي", True),
             ("الملكة أسماء بنت شهاب", False),
             ("الملكة لميس الحميرية", False),
         ]),
        (31, "اتخذت الدولة النجاحية التي حكمت إقليم تهامة والساحل الغربي لليمن من مدينة ... عاصمة علمية وسياسية لها:",
         all_lessons[7], "Understand", [
             ("المخا", False),
             ("زبيد", True),
             ("الحديدة", False),
             ("حيس", False),
         ]),
        (32, "التحفة المعمارية الإسلامية البارزة في رداع التي بناها الملك الظافر عامر بن عبد الوهاب هي:",
         all_lessons[10], "Remember", [
             ("قلعة القاهرة", False),
             ("مدرسة العامرية", True),
             ("حصن حب", False),
             ("دار الحجر", False),
         ]),
        (33, "أرسل الرسول صلى الله عليه وسلم الإمام علي بن أبي طالب إلى همدان في صنعاء فأسلمت قبائلها في:",
         all_lessons[4], "Understand", [
             ("عام كامل من المفاوضات", False),
             ("يوم واحد دون قتال", True),
             ("ثلاثة أشهر متواصلة", False),
             ("بعد حصار صنعاء", False),
         ]),
        (34, "اشتهرت عمارة المنازل والقصور اليمنية القديمة بناطحات السحاب الطينية الفريدة في مدينة:",
         all_lessons[3], "Remember", [
             ("حوطة لحج", False),
             ("شبام حضرموت", True),
             ("المكلا", False),
             ("سيئون", False),
         ]),
        (35, "تأسست الدولة الرسولية في اليمن بعد انحسار الأيوبيين، ومؤسسها الأول هو:",
         all_lessons[9], "Understand", [
             ("المظفر يوسف", False),
             ("نور الدين عمر بن رسول", True),
             ("الأشرف إسماعيل", False),
             ("المؤيد داود", False),
         ]),
        (36, "معبد (عرش بلقيس) الشهير بأعمدته الحجرية الستة المنتصبة في مأرب هو بالاسم التاريخي:",
         all_lessons[0], "Remember", [
             ("معبد أوام", False),
             ("معبد برآن", True),
             ("معبد صرواح", False),
             ("معبد سين", False),
         ]),

        # --- أسئلة إجابتها الصحيحة: ج (C) ---
        (37, "الملك الحميري الباسل الذي قاوم الغزو الحبشي وقضى مدافعاً عن استقلال وسيادة أرض اليمن هو:",
         all_lessons[2], "Understand", [
             ("كرب إيل وتر", False),
             ("شمر يهرعش", False),
             ("ذو نواس (يوسف أسأر)", True),
             ("سيف بن ذي يزن", False),
         ]),
        (38, "شهدت مدينة تعز في عهد الدولة الرسولية نهضة علمية كبرى بتشييد العديد من المدارس الوقفية وأبرزها:",
         all_lessons[9], "Understand", [
             ("المدرسة العامرية برداع", False),
             ("المدرسة الشامسية بذمار", False),
             ("المدرسة الأشرفية والمظفرية", True),
             ("دار الحجر بصنعاء", False),
         ]),
        (39, "عاصمة مملكة حضرموت التاريخية القديمة التي ازدهرت فيها تجارة اللبان والبخور هي مدينة:",
         all_lessons[3], "Remember", [
             ("تمنع", False),
             ("مأرب", False),
             ("شبوة", True),
             ("الغيضة", False),
         ]),
        (40, "اتخذت الدولة اليعفرية التي استقلت في هضبة اليمن الوسطى من مدينة ... مركزاً أولاً لحكمها:",
         all_lessons[7], "Understand", [
             ("إب", False),
             ("ذمار", False),
             ("شبام كوكبان", True),
             ("البيضاء", False),
         ]),
        (41, "قاد المقاومة الوطنية ضد الحملة البريطانية الغازية على عدن عام 1839م سلطان لحج وعدن وهو:",
         all_lessons[13], "Understand", [
             ("السلطان القعيطي", False),
             ("السلطان فضل بن علي العبدلي", False),
             ("السلطان محسن بن فضل العبدلي", True),
             ("الشريف حمود", False),
         ]),
        (42, "الميناء اليمني القديم على بحر العرب الذي كان المرفأ الرئيسي لتصدير اللبان لمملكة حضرموت هو:",
         all_lessons[3], "Remember", [
             ("ميناء الحديدة", False),
             ("ميناء عدن", False),
             ("ميناء قنا (بير علي)", True),
             ("ميناء ميدي", False),
         ]),
        (43, "الصحابي الجليل من قبيلة دوس الذي يعد أكثر الصحابة رواية للحديث النبوي الشريف هو:",
         all_lessons[5], "Remember", [
             ("معاذ بن جبل", False),
             ("أبو موسى الأشعري", False),
             ("أبو هريرة عبد الرحمن بن صخر", True),
             ("عمار بن ياسر", False),
         ]),

        # --- أسئلة إجابتها الصحيحة: د (D) ---
        (44, "المسجد التاريخي الجامع في مدينة صنعاء الذي بني في عهد الرسول صلى الله عليه وسلم وبأمره المباشر هو:",
         all_lessons[6], "Remember", [
             ("جامع الجند بتعز", False),
             ("جامع الأشاعرة بزبيد", False),
             ("جامع المظفر", False),
             ("الجامع الكبير بصنعاء", True),
         ]),
        (45, "الخط الأبجدي اليمني القديم الأصيل الذي نقشت به ممالك سبأ ومعين وحمير آثارها ومعاهداتها يسمى:",
         all_lessons[1], "Remember", [
             ("الخط المسماري", False),
             ("الخط الكوفي", False),
             ("الخط الآرامي", False),
             ("خط المسند", True),
         ]),
        (46, "القائد العسكري اليمني من قبيلة مذحج الذي لقب بفارس العرب وشهد معركة القادسية واليرموك هو:",
         all_lessons[5], "Understand", [
             ("سعد بن أبي وقاص", False),
             ("عدي بن حاتم الطائي", False),
             ("الأشتر النخعي", False),
             ("عمرو بن معد يكرب الزبيدي", True),
         ]),
        (47, "القصر الحميري والسبئي الشامخ في صنعاء القديمة الذي عد من عجائب فنون البناء والمعمار هو:",
         all_lessons[0], "Remember", [
             ("قصر سلحين", False),
             ("قصر شقر", False),
             ("قصر ريدان", False),
             ("قصر غمدان التاريخي", True),
         ]),
        (48, "الحصن المنيع في محافظة عمران الذي اعتصم به المقاومون اليمنيون ضد حصار القوات العثمانية هو:",
         all_lessons[12], "Apply", [
             ("حصن رداع", False),
             ("حصن حب", False),
             ("حصن الدملوة", False),
             ("حصن ثلا المنيع", True),
         ]),
        (49, "الصحابي اليماني الشهير الذي قال فيه النبي صلى الله عليه وسلم: (لو أقسم على الله لأبره) ومات بالشام هو:",
         all_lessons[5], "Understand", [
             ("حذيفة بن اليمان", False),
             ("أبو موسى الأشعري", False),
             ("معاذ بن جبل", False),
             ("البراء بن مالك الأنصاري", True),
         ]),
        (50, "المعاهدة التاريخية التي أجبرت القوات العثمانية على الاعتراف بالاستقلال الإداري لشمال اليمن هي:",
         all_lessons[12], "Analyze", [
             ("معاهدة الطائف", False),
             ("معاهدة جدة", False),
             ("اتفاقية الضالع", False),
             ("معاهدة دعان 1911م", True),
         ]),
    ]

    print("[2] جاري تخزين وتدقيق الأسئلة الـ 50 في بنك الأسئلة...")
    all_question_objects = []

    # معالجة وحفظ الـ 20 سؤالاً صح وخطأ
    for num, content, is_true, l_obj, bloom in tf_data:
        q_obj = Question.objects.filter(content=content).first()
        if not q_obj:
            q_obj = Question.objects.create(
                content=content,
                description=f"سؤال رقم {num} - منهج التاريخ للصف التاسع",
                lesson=l_obj,
                difficulty=1 if bloom == "Remember" else 2,
                bloomLevel=bloom,
                questionType="true_false",
                isTrue=is_true,
                answerText="صواب" if is_true else "خطأ",
                status="approved",
                defaultMark=1.0,
                expected_time_minutes=2,
                institution_type="school",
                assessment_type="summative",
                createdBy=admin_user,
                approved_at=datetime.datetime.now(),
            )
        else:
            q_obj.questionType = "true_false"
            q_obj.isTrue = is_true
            q_obj.status = "approved"
            q_obj.lesson = l_obj
            q_obj.save()

        Answer.objects.filter(question=q_obj).delete()
        Answer.objects.create(question=q_obj, text="صح / صواب", isTrue=(is_true is True))
        Answer.objects.create(question=q_obj, text="خطأ", isTrue=(is_true is False))
        all_question_objects.append(q_obj)

    # معالجة وحفظ الـ 30 سؤال اختيار متعدد
    for num, content, l_obj, bloom, opts in mcq_data:
        q_obj = Question.objects.filter(content=content).first()
        if not q_obj:
            q_obj = Question.objects.create(
                content=content,
                description=f"سؤال رقم {num} - منهج التاريخ للصف التاسع",
                lesson=l_obj,
                difficulty=1 if bloom == "Remember" else (2 if bloom == "Understand" else 3),
                bloomLevel=bloom,
                questionType="mcq",
                isTrue=None,
                status="approved",
                defaultMark=1.0,
                expected_time_minutes=2,
                institution_type="school",
                assessment_type="summative",
                createdBy=admin_user,
                approved_at=datetime.datetime.now(),
            )
        else:
            q_obj.questionType = "mcq"
            q_obj.isTrue = None
            q_obj.status = "approved"
            q_obj.lesson = l_obj
            q_obj.save()

        Answer.objects.filter(question=q_obj).delete()
        for opt_text, opt_is_correct in opts:
            Answer.objects.create(
                question=q_obj,
                text=opt_text,
                isTrue=opt_is_correct
            )
        all_question_objects.append(q_obj)

    print(f"[3] تم تخزين وتدقيق {len(all_question_objects)} سؤالاً بنجاح تام!")

    # 7. جدول الاختبار
    exam_schedule, _ = ExamSchedule.objects.get_or_create(
        name="جدول اختبارات الشهادة الأساسية العامة 1446هـ - مادة التاريخ",
        defaults={"date": datetime.date(2025, 5, 18), "duration": 120, "isActive": True}
    )

    # 8. الاختبار الوزاري
    exam, _ = Exam.objects.get_or_create(
        uniqueCode="YE-SANAA-G9-HIST-1446",
        defaults={
            "title": "اختبار مادة التاريخ - الشهادة الأساسية (الصف التاسع) - أمانة العاصمة",
            "institution_type": "school",
            "year": academic_year,
            "subject": history_subject,
            "class_track": class_track,
            "examSchedule": exam_schedule,
            "country": yemen,
            "governorate": sanaa_gov,
            "directorate": tahrir_dir,
            "bloom_enabled": True,
            "models_mode": "uniform",
            "target_scope_level": "directorate",
        }
    )
    exam.title = "اختبار مادة التاريخ - الشهادة الأساسية (الصف التاسع) - أمانة العاصمة"
    exam.year = academic_year
    exam.subject = history_subject
    exam.class_track = class_track
    exam.examSchedule = exam_schedule
    exam.governorate = sanaa_gov
    exam.directorate = tahrir_dir
    exam.is_deleted = False
    exam.save()

    # 9. توليد النماذج الوزارية الأربعة (A, B, C, D)
    # -------------------------------------------------------------
    # فصل أسئلة الصح والخطأ (1-20) عن الاختيارات (21-50)
    tf_q_list = all_question_objects[0:20]

    # إعادة دمج وتوزيع أسئلة الاختيارات الـ 30 بشكل دوري متناوب (أ، ب، ج، د، أ، ب، ج، د...)
    # حتى لا تكون إجابات متتالية من نفس الحرف، بل تتوزع بشكل طبيعي واحترافي
    q_a = all_question_objects[20:28]  # 8 أسئلة إجابتها أ (A)
    q_b = all_question_objects[28:36]  # 8 أسئلة إجابتها ب (B)
    q_c = all_question_objects[36:43]  # 7 أسئلة إجابتها ج (C)
    q_d = all_question_objects[43:50]  # 7 أسئلة إجابتها د (D)

    mcq_interleaved = []
    for i in range(8):
        if i < len(q_a): mcq_interleaved.append(q_a[i])  # أ
        if i < len(q_b): mcq_interleaved.append(q_b[i])  # ب
        if i < len(q_c): mcq_interleaved.append(q_c[i])  # ج
        if i < len(q_d): mcq_interleaved.append(q_d[i])  # د

    # أنماط تبديل مدروسة ومحكمة لكل نموذج باستخدام خطوات أولية (Coprime)
    # تضمن ترتيباً مختلفاً كلياً لكل نموذج ومفتاح إجابة فريد ومستقل
    def permute_by_step(lst, step):
        n = len(lst)
        return [lst[(i * step) % n] for i in range(n)]

    version_configs = [
        ("A", 0, "النموذج أ", tf_q_list, mcq_interleaved),
        ("B", 1, "النموذج ب", permute_by_step(tf_q_list, 7), permute_by_step(mcq_interleaved, 7)),
        ("C", 2, "النموذج ج", permute_by_step(tf_q_list, 11), permute_by_step(mcq_interleaved, 11)),
        ("D", 3, "النموذج د", permute_by_step(tf_q_list, 13), permute_by_step(mcq_interleaved, 13)),
    ]

    # حذف الأوامر القديمة للنماذج
    ExamVersion.objects.filter(exam=exam).delete()

    created_versions = {}
    for v_code, g_idx, v_name, tf_set, mcq_set in version_configs:
        v_obj = ExamVersion.objects.create(
            exam=exam,
            versionCode=v_code,
            model_group_index=g_idx,
            difficulty_profile="balanced",
            difficulty_distribution={"easy": 40, "medium": 45, "hard": 15},
        )
        combined_questions = tf_set + mcq_set
        for idx, q in enumerate(combined_questions, start=1):
            ExamQuestionOrder.objects.create(
                examVersion=v_obj,
                question=q,
                orderIndex=idx
            )
        created_versions[v_code] = v_obj
        print(f"[4] تم إنشاء {v_name} (الكود {v_code}) بإجمالي {len(combined_questions)} سؤالاً وترتيب فريد")

    # 10. تسجيل 40 طالباً رسمياً من مدارس أمانة العاصمة موزعين على النماذج الأربعة
    # -------------------------------------------------------------
    school_1 = AcademicOrganization.objects.get(id=12)  # مدرسة سيف بن ذي يزن الأساسية الثانوية
    school_2 = AcademicOrganization.objects.get(id=4)   # مدرسة بلقيس الثانوية النموذجية للبنات
    school_3 = AcademicOrganization.objects.get(id=5)   # مدرسة الكويت الثانوية النموذجية للبنين
    school_4 = AcademicOrganization.objects.get(id=10)  # مدرسة نشوان الحميري الثانوية
    school_5 = AcademicOrganization.objects.get(id=14)  # مدرسة بغداد الأساسية الثانوية

    students_names = [
        ("أحمد محمد علي الكبسي", 1, school_1),
        ("سارة عبد الله يحيى الحيمي", 2, school_2),
        ("عمر خالد فؤاد الشامي", 1, school_3),
        ("فاطمة إبراهيم حسن الصنعاني", 2, school_2),
        ("محمد عبد الرحمن عبد القادر", 1, school_1),
        ("يوسف صادق حميد المتوكل", 1, school_4),
        ("أروى توفيق إسماعيل العنسي", 2, school_2),
        ("علي حمود ناصر الوشلي", 1, school_5),
        ("مريم سلطان عبد الوهاب الآنسي", 2, school_2),
        ("بلال عبد العزيز سعيد المقطري", 1, school_3),
        ("طارق منير عبد الله الحدا", 1, school_1),
        ("ريام عبد الرقيب عبد الملك الأغبري", 2, school_2),
        ("هشام عبد الخالق مطهر الشرفي", 1, school_4),
        ("هدى أمين لطف المؤيد", 2, school_2),
        ("خليل جمال ردمان الريمي", 1, school_5),
        ("ياسين عبد الحفيظ أحمد السياني", 1, school_3),
        ("إيمان زكريا يحيى الديلمي", 2, school_2),
        ("إبراهيم رضوان محمد جحاف", 1, school_1),
        ("هيثم عبد السلام عبد الله الوزير", 1, school_4),
        ("زينب محمد حسين الحوثي", 2, school_2),
        ("عبد الله عمار عادل الكحلاني", 1, school_5),
        ("عمار وليد أحمد الشهاري", 1, school_3),
        ("منى عصام عبد الجبار سنان", 2, school_2),
        ("ماجد وضاح علي الجرموزي", 1, school_1),
        ("زياد نبيل لطف القحوم", 1, school_4),
        ("سمية عبد الباسط محمد قاسم", 2, school_2),
        ("حسام بشير عبد الله النونو", 1, school_5),
        ("حمزة مطهر حمود قاطة", 1, school_3),
        ("خلود غسان أحمد الصعدي", 2, school_2),
        ("أسامة مروان محمد شرف الدين", 1, school_1),
        ("جميل عبد الله محمد الحبابي", 1, school_4),
        ("سعاد عبد الملك أحمد العماد", 2, school_2),
        ("فهد عبد الكريم ناصر الرداعي", 1, school_5),
        ("أماني فضل عبد الله العواضي", 2, school_2),
        ("سامي عبد الرزاق علي السقاف", 1, school_3),
        ("ابتسام محمد يحيى شرف الدين", 2, school_2),
        ("أصيل رشاد أحمد الصلاحي", 1, school_1),
        ("لمياء عبد الحكيم قاسم الشرجبي", 2, school_2),
        ("مازن عبد الولي عبده الدبعي", 1, school_4),
        ("شيماء عبد السلام حيدر الآنسي", 2, school_2),
    ]

    version_keys = ["A", "B", "C", "D"]
    start_seat = 94101
    start_secret = 62001

    StudentExamRegistration.objects.filter(examVersion__exam=exam).delete()
    registered_count = 0

    for idx, (st_name, gender, st_school) in enumerate(students_names):
        acad_num = 20250900 + idx + 1
        st_obj, _ = Student.objects.get_or_create(
            academic_number=acad_num,
            defaults={
                "name_ar": st_name,
                "gender": gender,
                "organization": st_school,
                "directorate": tahrir_dir,
                "class_track": class_track,
                "is_active": True,
            }
        )
        if st_obj.name_ar != st_name:
            st_obj.name_ar = st_name
            st_obj.organization = st_school
            st_obj.directorate = tahrir_dir
            st_obj.class_track = class_track
            st_obj.gender = gender
            st_obj.save()

        # توزيع دوري متساوٍ على النماذج الأربعة: A, B, C, D
        v_code = version_keys[idx % 4]
        target_version = created_versions[v_code]

        seat_num = str(start_seat + idx)
        secret_num = str(start_secret + idx)

        StudentExamRegistration.objects.create(
            examVersion=target_version,
            student_profile=st_obj,
            seatNumber=seat_num,
            secretNumber=secret_num,
            isPresent=True,
            is_printed=False,
        )
        registered_count += 1

    print(f"[5] تم تسجيل {registered_count} طالباً رسمياً وتوزيعهم على النماذج الأربعة (10 لكل نموذج)")
    print("=" * 75)
    print(" اكتمال البناء الوزاري بنجاح تام!")
    print(f" الاختبار ID: {exam.id} | الرمز: {exam.uniqueCode}")
    print(f" العنوان: {exam.title}")
    print(f" عدد الأسئلة لكل نموذج: 50 سؤالاً (20 صواب/خطأ + 30 اختيار متعدد)")
    print(f" عدد النماذج: 4 نماذج (أ، ب، ج، د)")
    print(f" عدد الطلاب: {registered_count} طالباً")
    print("=" * 75)


if __name__ == '__main__':
    run()
