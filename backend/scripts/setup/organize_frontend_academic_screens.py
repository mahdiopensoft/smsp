"""
═══════════════════════════════════════════════════════════════════════════════
🏛️🏫🏢 سكريبت تنظيم وتقسيم شاشات الفرونت إند وإنشاء شاشات المعاهد
    Organize Frontend Academic Screens (Schools, Universities, Institutes)
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import shutil

# مسارات المشروع
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BACKEND_DIR)
FRONTEND_PAGES_SYSADMIN = os.path.join(BASE_DIR, "frontend", "src", "pages", "SystemAdmin")
ACADEMICS_DIR = os.path.join(FRONTEND_PAGES_SYSADMIN, "Academics")
EXAMS_DIR = os.path.join(FRONTEND_PAGES_SYSADMIN, "Exams")

# المجلدات المستهدفة الجديدة
SCHOOLS_DIR = os.path.join(FRONTEND_PAGES_SYSADMIN, "Schools")
UNIVERSITIES_DIR = os.path.join(FRONTEND_PAGES_SYSADMIN, "Universities")
INSTITUTES_DIR = os.path.join(FRONTEND_PAGES_SYSADMIN, "Institutes")
COMMON_DIR = os.path.join(FRONTEND_PAGES_SYSADMIN, "Common")

# 1. قائمة شاشات المدارس المراد نقلها من Academics إلى Schools
SCHOOL_SCREENS = [
    "EducationalStages",
    "Levels",
    "Tracks",
    "ClassTracks",
    "Subjects",
    "ClassSubjects",
    "Units",
    "Lessons",
    "LearningOutcomes",
    "Students",
]

# 2. قائمة شاشات الجامعات المراد نقلها من Academics و Exams إلى Universities
UNIVERSITY_SCREENS = [
    "Colleges",
    "Departments",
    "Specializations",
    "EducationalLevels",
    "StudySystems",
    "Semesters",
    "SemesterSubjects",
    "GradingSystems",
]

# 3. قوالب الشاشات الجديدة للمعاهد
INSTITUTE_SCREENS_DEF = [
    {
        "folder": "InstituteFields",
        "view": "InstituteFieldsView",
        "add": "AddInstituteFields",
        "tag": "add-institute-fields",
        "url": "api/academic/institutes/fields/",
        "route": "institutes-fields",
        "title": "المجالات المهنية والتقنية",
        "headers": [
            '{"title": "كود المجال", "key": "field_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم المجال (عربي)", "key": "name_ar", "sortable": true}',
            '{"title": "اسم المجال (إنجليزي)", "key": "name_en", "sortable": true}',
            '{"title": "الوصف", "key": "description", "sortable": false}',
            '{"title": "الحالة", "key": "is_active", "width": "110px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteEducationSystems",
        "view": "InstituteEducationSystemsView",
        "add": "AddInstituteEducationSystems",
        "tag": "add-institute-education-systems",
        "url": "api/academic/institutes/education-systems/",
        "route": "institutes-education-systems",
        "title": "أنظمة التعليم والتدريب",
        "headers": [
            '{"title": "كود النظام", "key": "system_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم النظام", "key": "name_ar", "sortable": true}',
            '{"title": "نوع النظام", "key": "system_type_display", "sortable": true}',
            '{"title": "طبيعة الدراسة", "key": "study_nature_display", "sortable": true}',
            '{"title": "مدة الدراسة (سنوات)", "key": "duration_years", "align": "center", "width": "140px"}',
            '{"title": "خاضع للامتحان الوزاري", "key": "has_ministerial_exam", "align": "center", "width": "150px"}',
            '{"title": "الحالة", "key": "is_active", "width": "110px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteSpecializations",
        "view": "InstituteSpecializationsView",
        "add": "AddInstituteSpecializations",
        "tag": "add-institute-specializations",
        "url": "api/academic/institutes/specializations/",
        "route": "institutes-specializations",
        "title": "التخصصات المهنية والتقنية",
        "headers": [
            '{"title": "كود التخصص", "key": "specialization_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم التخصص", "key": "name_ar", "sortable": true}',
            '{"title": "المجال المهني", "key": "field_name", "sortable": true}',
            '{"title": "نظام التعليم", "key": "education_system_name", "sortable": true}',
            '{"title": "عدد المستويات", "key": "number_of_levels", "align": "center", "width": "120px"}',
            '{"title": "الحالة", "key": "is_active", "width": "110px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteAdmissionRequirements",
        "view": "InstituteAdmissionRequirementsView",
        "add": "AddInstituteAdmissionRequirements",
        "tag": "add-institute-admission-requirements",
        "url": "api/academic/institutes/admission-requirements/",
        "route": "institutes-admission-requirements",
        "title": "شروط وضوابط القبول والتسجيل",
        "headers": [
            '{"title": "عنوان الضابط / الشرط", "key": "title", "sortable": true}',
            '{"title": "نظام التعليم", "key": "education_system_name", "sortable": true}',
            '{"title": "التخصص", "key": "specialization_name", "sortable": true}',
            '{"title": "مؤهل القبول المطلوب", "key": "required_qualification", "sortable": true}',
            '{"title": "المسارات المقبولة", "key": "accepted_tracks", "sortable": false}',
            '{"title": "الحالة", "key": "is_active", "width": "110px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteCurricula",
        "view": "InstituteCurriculaView",
        "add": "AddInstituteCurricula",
        "tag": "add-institute-curricula",
        "url": "api/academic/institutes/curricula/",
        "route": "institutes-curricula",
        "title": "الخطط الدراسية للمعاهد",
        "headers": [
            '{"title": "رمز الخطة", "key": "version_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم الخطة الدراسية", "key": "name_ar", "sortable": true}',
            '{"title": "التخصص", "key": "specialization_name", "sortable": true}',
            '{"title": "العام الدراسي", "key": "academic_year_name", "align": "center", "width": "150px"}',
            '{"title": "إجمالي الساعات", "key": "total_credit_hours", "align": "center", "width": "120px"}',
            '{"title": "معتمدة", "key": "is_approved", "align": "center", "width": "100px"}',
            '{"title": "الخطة الحالية", "key": "is_current", "align": "center", "width": "110px"}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteBatches",
        "view": "InstituteBatchesView",
        "add": "AddInstituteBatches",
        "tag": "add-institute-batches",
        "url": "api/academic/institutes/batches/",
        "route": "institutes-batches",
        "title": "الدفعات والأفواج للمعاهد",
        "headers": [
            '{"title": "رقم الدفعة", "key": "batch_number", "width": "110px", "align": "center", "sortable": true}',
            '{"title": "اسم الدفعة / الفوج", "key": "name_ar", "sortable": true}',
            '{"title": "التخصص", "key": "specialization_name", "sortable": true}',
            '{"title": "سنة الالتحاق", "key": "academic_year_name", "align": "center", "width": "140px"}',
            '{"title": "الخطة المعتمدة", "key": "curriculum_name", "sortable": true}',
            '{"title": "متخرجة", "key": "is_graduated", "align": "center", "width": "100px"}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteLevels",
        "view": "InstituteLevelsView",
        "add": "AddInstituteLevels",
        "tag": "add-institute-levels",
        "url": "api/academic/institutes/levels/",
        "route": "institutes-levels",
        "title": "المستويات الدراسية للمعاهد",
        "headers": [
            '{"title": "الترتيب", "key": "order", "width": "100px", "align": "center", "sortable": true}',
            '{"title": "اسم المستوى (عربي)", "key": "name_ar", "sortable": true}',
            '{"title": "اسم المستوى (إنجليزي)", "key": "name_en", "sortable": true}',
            '{"title": "ملاحظات", "key": "note", "sortable": false}',
            '{"title": "الحالة", "key": "is_active", "width": "110px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteSemesters",
        "view": "InstituteSemestersView",
        "add": "AddInstituteSemesters",
        "tag": "add-institute-semesters",
        "url": "api/academic/institutes/semesters/",
        "route": "institutes-semesters",
        "title": "الفصول والفترات الدراسية للمعاهد",
        "headers": [
            '{"title": "الترتيب", "key": "order", "width": "100px", "align": "center", "sortable": true}',
            '{"title": "اسم الفصل / الفترة", "key": "name_ar", "sortable": true}',
            '{"title": "طبيعة الفصل", "key": "semester_nature_display", "align": "center", "width": "160px"}',
            '{"title": "الفصل الحالي", "key": "is_current", "align": "center", "width": "110px"}',
            '{"title": "الحالة", "key": "is_active", "width": "110px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteSubjects",
        "view": "InstituteSubjectsView",
        "add": "AddInstituteSubjects",
        "tag": "add-institute-subjects",
        "url": "api/academic/institutes/subjects/",
        "route": "institutes-subjects",
        "title": "المواد الدراسية للمعاهد",
        "headers": [
            '{"title": "كود المادة", "key": "subject_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم المادة الدراسية", "key": "name_ar", "sortable": true}',
            '{"title": "المجال التابعة له", "key": "field_name", "sortable": true}',
            '{"title": "نوع المادة", "key": "subject_type_display", "align": "center", "width": "120px"}',
            '{"title": "جهة المادة", "key": "subject_entity_display", "align": "center", "width": "130px"}',
            '{"title": "التصنيف الأكاديمي", "key": "academic_category_display", "align": "center", "width": "140px"}',
            '{"title": "الساعات", "key": "credit_hours", "align": "center", "width": "100px"}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteCurriculumSubjects",
        "view": "InstituteCurriculumSubjectsView",
        "add": "AddInstituteCurriculumSubjects",
        "tag": "add-institute-curriculum-subjects",
        "url": "api/academic/institutes/curriculum-subjects/",
        "route": "institutes-curriculum-subjects",
        "title": "مقررات الخطط والفصول الدراسية",
        "headers": [
            '{"title": "الخطة الدراسية", "key": "curriculum_name", "sortable": true}',
            '{"title": "المادة الدراسية", "key": "subject_name", "sortable": true}',
            '{"title": "المستوى", "key": "level_name", "align": "center", "width": "120px"}',
            '{"title": "الفصل", "key": "semester_name", "align": "center", "width": "130px"}',
            '{"title": "جهة عقد الاختبار", "key": "exam_entity_display", "align": "center", "width": "140px"}',
            '{"title": "امتحان وزاري", "key": "is_ministerial_exam", "align": "center", "width": "120px"}',
            '{"title": "العظمى", "key": "max_score", "align": "center", "width": "90px"}',
            '{"title": "الصغرى", "key": "min_score", "align": "center", "width": "90px"}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteShortCourses",
        "view": "InstituteShortCoursesView",
        "add": "AddInstituteShortCourses",
        "tag": "add-institute-short-courses",
        "url": "api/academic/institutes/short-courses/",
        "route": "institutes-short-courses",
        "title": "الدورات التدريبية القصيرة",
        "headers": [
            '{"title": "كود الدورة", "key": "course_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم الدورة التدريبية", "key": "name_ar", "sortable": true}',
            '{"title": "المجال", "key": "field_name", "sortable": true}',
            '{"title": "الجهة المنظمة", "key": "organization_name", "sortable": true}',
            '{"title": "المدة (أسابيع)", "key": "duration_weeks", "align": "center", "width": "120px"}',
            '{"title": "إجمالي الساعات", "key": "total_hours", "align": "center", "width": "120px"}',
            '{"title": "الشهادة", "key": "certificate_type", "sortable": false}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    },
    {
        "folder": "InstituteSpecialTracks",
        "view": "InstituteSpecialTracksView",
        "add": "AddInstituteSpecialTracks",
        "tag": "add-institute-special-tracks",
        "url": "api/academic/institutes/special-tracks/",
        "route": "institutes-special-tracks",
        "title": "تحقيق المهنة والمسارات الخاصة",
        "headers": [
            '{"title": "رمز المسار", "key": "track_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم البرنامج / المسار", "key": "name_ar", "sortable": true}',
            '{"title": "المجال", "key": "field_name", "sortable": true}',
            '{"title": "نظام التعليم", "key": "education_system_name", "sortable": true}',
            '{"title": "المهنة المستهدفة", "key": "target_profession", "sortable": true}',
            '{"title": "الشهادة الممنوحة", "key": "certificate_name", "sortable": false}',
            '{"title": "درجة النجاح", "key": "passing_score", "align": "center", "width": "110px"}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    },
]

def generate_vue_pair(target_dir, cfg):
    os.makedirs(target_dir, exist_ok=True)
    add_file = os.path.join(target_dir, f"{cfg['add']}.vue")
    view_file = os.path.join(target_dir, f"{cfg['view']}.vue")

    add_code = f"""<template>
  <drawer :data="data" :getData="getData" click="{cfg['url']}" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="{cfg['route']}" :attr="{{}}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {{
  name: '{cfg['add']}',
  props: {{
    data: Object,
    items: [Array, Object],
    getData: Function,
  }},
  data() {{
    return {{}};
  }},
}};
</script>
"""

    headers_formatted = ",\n        ".join(cfg['headers'])

    view_code = f"""<template>
  <div>
    <{cfg['tag']} v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Search Field -->
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="searchQuery"
            label="بحث..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @keydown.enter="applyFilters"
          />
        </v-col>

        <!-- Active Status Filter -->
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="filterActive"
            :items="activeOptions"
            item-title="text"
            item-value="value"
            label="حالة التفعيل"
            prepend-inner-icon="mdi-check-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="12" md="4" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold flex-grow-1 mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Data Table -->
    <custom-data-table
      v-bind="{{
        headers,
        items,
        getData,
        create: () => (drawer = true),
        delItem: url,
        editItem,
      }}"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{{ item, key }}">
        <span v-if="key === 'is_active'">
          <v-chip
            :color="item.is_active ? 'success' : 'error'"
            size="small"
            class="font-weight-bold"
          >
            {{{{ item.is_active ? 'مفعل' : 'معطل' }}}}
          </v-chip>
        </span>
        <span v-else-if="key === 'is_approved' || key === 'is_current' || key === 'is_graduated' || key === 'has_ministerial_exam' || key === 'is_ministerial_exam'">
          <v-chip
            :color="item[key] ? 'primary' : 'grey'"
            size="small"
            class="font-weight-bold"
          >
            {{{{ item[key] ? 'نعم' : 'لا' }}}}
          </v-chip>
        </span>
      </template>
    </custom-data-table>
  </div>
</template>

<script>
import shared from "external-components";
import {cfg['add']} from "./{cfg['add']}.vue";

export default {{
  name: '{cfg['view']}',
  components: {{ {cfg['add']} }},
  data() {{
    return {{
      url: "{cfg['url']}",
      data: {{}},
      items: {{}},
      drawer: false,
      searchQuery: "",
      filterActive: null,
      activeOptions: [
        {{ text: "مفعل", value: true }},
        {{ text: "غير مفعل", value: false }},
      ],
    }};
  }},
  computed: {{
    headers() {{
      return [
        {headers_formatted}
      ];
    }},
  }},
  methods: {{
    async getData(params = {{}}) {{
      const queryParams = {{
        ...params,
        search: this.searchQuery || undefined,
        is_active: this.filterActive !== null ? this.filterActive : undefined,
      }};
      try {{
        const response = await shared.getData({{
          path: this.url,
          params: queryParams,
        }});
        this.items = response;
      }} catch (error) {{
        console.error("Error fetching {cfg['route']}:", error);
      }}
    }},
    applyFilters() {{
      this.getData();
    }},
    resetFilters() {{
      this.searchQuery = "";
      this.filterActive = null;
      this.getData();
    }},
    editItem(item) {{
      this.data = {{ ...item }};
      this.drawer = true;
    }},
  }},
}};
</script>

<style scoped>
.gap-2 {{
  gap: 8px;
}}
</style>
"""

    with open(add_file, "w", encoding="utf-8") as f:
        f.write(add_code)
    with open(view_file, "w", encoding="utf-8") as f:
        f.write(view_code)
    print(f"  ✓ تم إنشاء شاشة المعهد: {cfg['title']} ({cfg['view']})")


def run_organization():
    print("🚀 بدء تنظيم وتقسيم شاشات الفرونت إند (المدارس، الجامعات، المعاهد)...\n")

    os.makedirs(SCHOOLS_DIR, exist_ok=True)
    os.makedirs(UNIVERSITIES_DIR, exist_ok=True)
    os.makedirs(INSTITUTES_DIR, exist_ok=True)
    os.makedirs(COMMON_DIR, exist_ok=True)

    # 1. نقل شاشات المدارس
    print("🏫 [1/4] نقل وتنظيم شاشات المدارس إلى: frontend/src/pages/SystemAdmin/Schools/")
    for screen in SCHOOL_SCREENS:
        src = os.path.join(ACADEMICS_DIR, screen)
        dst = os.path.join(SCHOOLS_DIR, screen)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.move(src, dst)
            print(f"  ✓ تم نقل شاشة: {screen} -> Schools/{screen}")
        elif os.path.exists(dst):
            print(f"  - شاشة موجودة بالفعل: Schools/{screen}")

    # إضافة شاشة الشعب المدرسية SchoolSections في Schools إذا لم تكن موجودة
    school_sections_cfg = {
        "folder": "SchoolSections",
        "view": "SchoolSectionsView",
        "add": "AddSchoolSections",
        "tag": "add-school-sections",
        "url": "api/academic/school-sections/",
        "route": "school-sections",
        "title": "الشعب والفصول المدرسية",
        "headers": [
            '{"title": "كود الشعبة", "key": "section_code", "width": "120px", "align": "center", "sortable": true}',
            '{"title": "اسم الشعبة / الفصل", "key": "name_ar", "sortable": true}',
            '{"title": "مسار الصف", "key": "class_track_name", "sortable": true}',
            '{"title": "العام الدراسي", "key": "year_name", "align": "center", "width": "140px"}',
            '{"title": "النوع", "key": "gender", "align": "center", "width": "100px"}',
            '{"title": "السعة", "key": "max_capacity", "align": "center", "width": "100px"}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    }
    generate_vue_pair(os.path.join(SCHOOLS_DIR, "SchoolSections"), school_sections_cfg)

    # 2. نقل شاشات الجامعات
    print("\n🏛️ [2/4] نقل وتنظيم شاشات الجامعات إلى: frontend/src/pages/SystemAdmin/Universities/")
    for screen in UNIVERSITY_SCREENS:
        src = os.path.join(ACADEMICS_DIR, screen)
        dst = os.path.join(UNIVERSITIES_DIR, screen)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.move(src, dst)
            print(f"  ✓ تم نقل شاشة: {screen} -> Universities/{screen}")
        elif os.path.exists(dst):
            print(f"  - شاشة موجودة بالفعل: Universities/{screen}")

    # نقل ExamPeriods من Exams إلى Universities
    exam_periods_src = os.path.join(EXAMS_DIR, "ExamPeriods")
    exam_periods_dst = os.path.join(UNIVERSITIES_DIR, "ExamPeriods")
    if os.path.exists(exam_periods_src) and not os.path.exists(exam_periods_dst):
        shutil.copytree(exam_periods_src, exam_periods_dst)
        print("  ✓ تم نسخ شاشة: ExamPeriods -> Universities/ExamPeriods")

    # إضافة شاشة المقررات الجامعية UniversityCourses في Universities
    univ_courses_cfg = {
        "folder": "UniversityCourses",
        "view": "UniversityCoursesView",
        "add": "AddUniversityCourses",
        "tag": "add-university-courses",
        "url": "api/academic/university-courses/",
        "route": "university-courses",
        "title": "المقررات الجامعية",
        "headers": [
            '{"title": "كود المقرر", "key": "course_code", "width": "130px", "align": "center", "sortable": true}',
            '{"title": "اسم المقرر الأكاديمي", "key": "name_ar", "sortable": true}',
            '{"title": "الكلية", "key": "college_name", "sortable": true}',
            '{"title": "القسم الأكاديمي", "key": "department_name", "sortable": true}',
            '{"title": "الساعات المعتمدة", "key": "credit_hours", "align": "center", "width": "130px"}',
            '{"title": "نوع المتطلب", "key": "course_type", "align": "center", "width": "120px"}',
            '{"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}',
        ]
    }
    generate_vue_pair(os.path.join(UNIVERSITIES_DIR, "UniversityCourses"), univ_courses_cfg)

    # 3. نقل المشتركات (الأعوام الدراسية)
    print("\n📅 [3/4] تنظيم الشاشات العامة والمشتركة إلى: Common/")
    ay_src = os.path.join(ACADEMICS_DIR, "AcademicYears")
    ay_dst = os.path.join(COMMON_DIR, "AcademicYears")
    if os.path.exists(ay_src) and not os.path.exists(ay_dst):
        shutil.move(ay_src, ay_dst)
        print("  ✓ تم نقل: AcademicYears -> Common/AcademicYears")

    # 4. إنشاء شاشات المعاهد الـ 12
    print("\n🏢 [4/4] إنشاء شاشات المعاهد الجديدة في: frontend/src/pages/SystemAdmin/Institutes/")
    for cfg in INSTITUTE_SCREENS_DEF:
        target_dir = os.path.join(INSTITUTES_DIR, cfg["folder"])
        generate_vue_pair(target_dir, cfg)

    # حذف مجلد Academics إذا أصبح فارغاً
    if os.path.exists(ACADEMICS_DIR) and not os.listdir(ACADEMICS_DIR):
        os.rmdir(ACADEMICS_DIR)
        print("\n🗑️ تم تنظيف وحذف مجلد Academics القديم الفارغ بنجاح.")

    print("\n🎉 اكتمل تنظيم وتقسيم كافة شاشات الفرونت إند بنجاح تام!")

    # 5. تشغيل تحديث الشاشات الأكاديمية في جانغو
    print("\n🔄 جاري تحديث الشاشات والـ JSON Fields في قاعدة البيانات...")
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        from update_academic_screens import update_academic_screens
        update_academic_screens()
    except Exception as e:
        print(f"⚠️ ملاحظة عند استدعاء update_academic_screens: {e}")

if __name__ == "__main__":
    run_organization()
