<template>
  <div class="exam-booklet-tab">
    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- 1. شريط التحقق من اكتمال وجاهزية بيانات الاختبار أولاً (Data Audit & Readiness) -->
    <!-- ════════════════════════════════════════════════════════════════ -->
    <div class="mb-3">
      <!-- WARNING / INCOMPLETE STATE: يظهر أولاً إذا كان هناك أي نقص في البيانات -->
      <v-alert
        v-if="auditFindings.hasIssues"
        type="warning"
        variant="tonal"
        class="rounded-2xl border-warning mb-0"
        icon="mdi-alert-circle-outline"
      >
        <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-2">
          <div class="d-flex align-center gap-2">
            <span class="text-subtitle-2 font-weight-black text-warning-darken-3">
              تنبيه: تم رصد نواقص في بيانات هذا الاختبار قبل الطباعة الرسمية
            </span>
            <v-chip size="x-small" color="warning" variant="flat" class="font-weight-black">
              {{ auditFindings.issues.length }} ملاحظات
            </v-chip>
          </div>
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-btn
              v-if="auditFindings.issues.some(i => i.actionTab === 'roster')"
              size="x-small"
              color="warning"
              variant="flat"
              class="font-weight-bold"
              prepend-icon="mdi-account-plus"
              @click="$emit('switch-tab', 'roster')"
            >
              الانتقال لكشف الطلاب
            </v-btn>
            <v-btn
              v-if="auditFindings.issues.some(i => i.actionTab === 'keys')"
              size="x-small"
              color="secondary"
              variant="flat"
              class="font-weight-bold"
              prepend-icon="mdi-key-variant"
              @click="$emit('switch-tab', 'keys')"
            >
              معاينة مفاتيح الحل
            </v-btn>
          </div>
        </div>
        <v-divider class="my-2 opacity-20" />
        <div class="d-flex flex-column gap-1">
          <div
            v-for="(issue, idx) in auditFindings.issues"
            :key="`issue-${idx}`"
            class="d-flex align-center gap-2 text-caption font-weight-bold"
          >
            <v-icon size="14" color="warning">mdi-alert-outline</v-icon>
            <span class="font-weight-black text-warning-darken-4">{{ issue.title }}:</span>
            <span class="text-medium-emphasis">{{ issue.desc }}</span>
          </div>
        </div>
      </v-alert>

      <!-- VERIFIED & COMPLETE STATE: شريط هادئ ورسمي بدون زحام أو ألوان متضاربة -->
      <div
        v-else
        class="bg-white border rounded-xl px-4 py-2.5 d-flex align-center justify-space-between flex-wrap gap-2 text-caption elevation-1"
      >
        <div class="d-flex align-center gap-2 flex-wrap">
          <v-icon color="success" size="18">mdi-check-decagram-outline</v-icon>
          <span class="font-weight-bold text-success-darken-2">بيانات الاختبار معتمدة ومكتملة:</span>
          <span class="text-medium-emphasis">
            {{ examDetails?.versions?.length || 1 }} نماذج •
            {{ currentVersionObj?.questions?.length || 0 }} سؤالاً بالنموذج •
            {{ totalRegisteredCount }} طالب مسجل
            <template v-if="uniqueSchoolsCount"> • {{ uniqueSchoolsCount }} {{ labels.pluralEntities }}</template>
            <template v-if="effectiveGovernorate"> • {{ effectiveGovernorate }}</template>
          </span>
        </div>
        <v-chip size="x-small" color="success" variant="tonal" class="font-weight-bold" prepend-icon="mdi-shield-check">
          جاهز للطباعة والتصحيح
        </v-chip>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- 2. شريط التصفية الموحد (Unified Filter Fields): متكيف للمدارس والجامعات والمعاهد -->
    <!-- ════════════════════════════════════════════════════════════════ -->
    <filter-fields :label="filterCardLabel" class="main-card border-0 pa-5 rounded-2xl mb-4">
      <v-row dense class="align-center">
        <!-- Level 1: المحافظة / النطاق الجغرافي أو الجامعي -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterGovernorate"
            :items="governorateOptions"
            item-title="title"
            item-value="value"
            :label="labels.level1"
            :placeholder="labels.level1Placeholder"
            :prepend-inner-icon="labels.level1Icon"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            clearable
            @update:model-value="() => { filterDirectorate = null; filterSchool = null; selectedStudentId = null; }"
          />
        </v-col>

        <!-- Level 2: المديرية / القسم الأكاديمي / الفرع المهني -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterDirectorate"
            :items="directorateOptions"
            item-title="title"
            item-value="value"
            :label="labels.level2"
            :placeholder="labels.level2Placeholder"
            :prepend-inner-icon="labels.level2Icon"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            clearable
            @update:model-value="() => { filterSchool = null; selectedStudentId = null; }"
          />
        </v-col>

        <!-- Level 3: المدرسة / الكلية / المعهد والمركز الامتحاني -->
        <v-col cols="12" sm="8" md="4">
          <v-select
            v-model="filterSchool"
            :items="schoolOptions"
            item-title="title"
            item-value="value"
            :label="labels.level3"
            :placeholder="labels.level3Placeholder"
            :prepend-inner-icon="labels.level3Icon"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            clearable
            @update:model-value="() => { selectedStudentId = null; }"
          >
            <template #item="{ props: sProps, item: sItem }">
              <v-list-item
                v-bind="sProps"
                :title="sItem.raw.title"
                :subtitle="`كود المركز: ${sItem.raw.id || '—'} | الطلاب المسجلون: ${sItem.raw.count} طالب`"
              />
            </template>
          </v-select>
        </v-col>

        <!-- زر تفريغ التصفية الموحد -->
        <v-col cols="12" sm="4" md="2" class="d-flex align-center">
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ التصفية"
            class="font-weight-bold mb-6 w-100"
            :disabled="!filterSchool && !filterDirectorate && !filterGovernorate"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Header Control Bar for Booklet -->
    <div class="main-card rounded-2xl pa-4 mb-4 border bg-white">
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
        <div class="d-flex align-center gap-3 flex-wrap flex-grow-1">
          <!-- Target Mode Toggle: Official General vs Student Preview -->
          <v-btn-toggle
            v-model="paperTargetMode"
            mandatory
            density="compact"
            color="primary"
            variant="outlined"
            rounded="lg"
          >
            <v-btn value="general_official" class="font-weight-bold px-3" prepend-icon="mdi-file-document-outline">
              كراسة أسئلة عامة (طباعة رسمية)
            </v-btn>
            <v-btn value="student_specific" class="font-weight-bold px-3" prepend-icon="mdi-account">
              معاينة مخصصة لطالب
            </v-btn>
          </v-btn-toggle>

          <!-- Student Picker when student_specific is selected -->
          <div v-if="paperTargetMode === 'student_specific'" style="min-width: 260px; max-width: 380px;" class="flex-grow-1">
            <v-autocomplete
              v-model="selectedStudentId"
              :items="filteredStudents"
              item-title="student_name"
              item-value="id"
              :placeholder="filteredStudents.length ? 'ابحث عن الطالب بالاسم أو رقم الجلوس...' : `لا يوجد طلاب ضمن ${labels.entityName} المختارة`"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              prepend-inner-icon="mdi-account-search"
            >
              <template #item="{ props: iProps, item }">
                <v-list-item
                  v-bind="iProps"
                  :title="item.raw.student_name"
                  :subtitle="`جلوس: ${item.raw.seat_number} | نموذج: ${item.raw.model_code} | ${labels.activePrefix}: ${item.raw.school_name || 'المركز'}`"
                />
              </template>
            </v-autocomplete>
          </div>

          <!-- Version Dropdown Selector (يدعم من نموذج واحد حتى 50 نموذج بسلاسة فائقة وبدون ازدحام) -->
          <div style="min-width: 200px; max-width: 250px;">
            <v-select
              :model-value="activeVersionTab"
              :items="versionSelectItems"
              item-title="title"
              item-value="value"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              prepend-inner-icon="mdi-format-list-bulleted-type"
              label="النموذج المعروض"
              @update:model-value="(val) => $emit('update:activeVersionTab', val)"
            />
          </div>

          <!-- Paper Layout Toggle (A4 vs A3) -->
          <v-btn-toggle
            v-model="selectedQuestionPaperLayout"
            mandatory
            density="compact"
            color="secondary"
            variant="outlined"
            rounded="lg"
          >
            <v-btn value="a4" class="font-weight-bold px-3" prepend-icon="mdi-file-outline">
              مقاس A4 (النمط الوزاري المعتمد)
            </v-btn>
            <v-btn value="a3" class="font-weight-bold px-3" prepend-icon="mdi-file-document-outline">
              مقاس كبير A3 (ورقة واحدة عمودين)
            </v-btn>
          </v-btn-toggle>
        </div>

        <div class="d-flex align-center gap-2">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-black px-5"
            prepend-icon="mdi-printer"
            @click="() => printQuestionsAndSheets('questions_only')"
          >
            طباعة ورقة الأسئلة الرسمية
          </v-btn>
          <v-btn
            color="secondary"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold px-4"
            prepend-icon="mdi-package-variant-closed"
            @click="() => printQuestionsAndSheets('package')"
          >
            طباعة الحزمة المتكاملة (أسئلة + تظليل)
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Official Question Paper Component Frame -->
    <div class="overflow-auto bg-grey-lighten-4 pa-4 rounded-2xl border d-flex justify-center mb-6">
      <YemeniOfficialQuestionPaper
        :exam-title="customStageTitle || activeExam?.title || ''"
        :exam-subject="activeExam?.subject_name || ''"
        :stage-title="customStageTitle || (activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || ''))"
        :exam-year="customExamYear || activeExam?.year_name || ''"
        :governorate="effectiveGovernorate"
        :directorate="effectiveDirectorate"
        :center-name="effectiveCenterName"
        :center-code="effectiveCenterCode"
        :exam-time="activeExam?.time_allowed || activeExam?.exam_time || ''"
        :day-name="activeExam?.day_name || ''"
        :exam-date="activeExam?.exam_date || ''"
        :envelope-no="effectiveEnvelopeNo"
        :student-name="activeStudent ? activeStudent.student_name : ''"
        :seat-number="activeStudent ? activeStudent.seat_number : ''"
        :secret-number="activeStudent ? (activeStudent.secret_number || '') : ''"
        :student-photo="activeStudent ? (activeStudent.student_photo || activeStudent.photo || '') : ''"
        :is-blank-mode="!activeStudent"
        :model-code="currentVersionObj?.versionCode || 'A'"
        :questions="currentVersionObj?.questions || []"
        :default-layout="selectedQuestionPaperLayout"
        :hide-toolbar="true"
        :show-diagnostics="false"
      />
    </div>

    <!-- ── Official Question Paper (A3 Large Sheet) Preview Modal ── -->
    <v-dialog v-model="showQuestionPaperDialog" max-width="1340" scrollable>
      <v-card class="pa-4 rounded-2xl">
        <div class="d-flex align-center justify-space-between pb-3 border-b mb-3">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-newspaper-variant-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-subtitle-1 font-weight-black mb-0">معاينة ورقة الأسئلة الرسمية المعتمدة (النمط الوزاري الموحد A4)</h3>
              <span class="text-caption text-medium-emphasis">مطابقة تماماً للنسخة الرسمية الوزارية الصادرة عن لجنة المطبعة السرية المركزية</span>
            </div>
          </div>
          <v-btn icon size="small" variant="text" @click="showQuestionPaperDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div v-if="showQuestionPaperDialog" class="overflow-auto bg-grey-lighten-4 pa-4 rounded-xl d-flex justify-center" style="max-height: 80vh;">
          <YemeniOfficialQuestionPaper
            :exam-title="activeExam?.title || ''"
            :exam-subject="activeExam?.subject_name || ''"
            :stage-title="activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || '')"
            :exam-year="activeExam?.year_name || ''"
            :governorate="effectiveGovernorate"
            :directorate="effectiveDirectorate"
            :center-name="effectiveCenterName"
            :center-code="effectiveCenterCode"
            :exam-time="activeExam?.time_allowed || activeExam?.exam_time || ''"
            :day-name="activeExam?.day_name || ''"
            :exam-date="activeExam?.exam_date || ''"
            :envelope-no="effectiveEnvelopeNo"
            :student-name="activeStudent ? activeStudent.student_name : ''"
            :seat-number="activeStudent ? activeStudent.seat_number : ''"
            :secret-number="activeStudent ? (activeStudent.secret_number || '') : ''"
            :student-photo="activeStudent ? (activeStudent.student_photo || activeStudent.photo || '') : ''"
            :is-blank-mode="!activeStudent"
            :model-code="currentVersionObj?.versionCode || '1'"
            :questions="currentVersionObj?.questions || []"
            :default-layout="'a4'"
            :hide-toolbar="true"
            :show-diagnostics="false"
          />
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import { printExamPackage } from '../utils/omrPrint'

const props = defineProps({
  activeExam: { type: Object, default: () => ({}) },
  examDetails: { type: Object, default: () => ({}) },
  activeVersionTab: { type: Number, default: 0 },
  sheetGenerationMode: { type: String, default: 'all_students' },
  activeSheetStudent: { type: Object, default: null },
  customStageTitle: { type: String, default: '' },
  customExamYear: { type: String, default: '' },
  customCenterName: { type: String, default: '' },
  customGovernorate: { type: String, default: '' },
  customDirectorate: { type: String, default: '' },
  selectedSheetLayout: { type: String, default: 'compact_a5' },
  getOmrElement: { type: Function, default: null },
})

const emit = defineEmits(['update:activeVersionTab', 'switch-tab', 'seed-students'])

const paperTargetMode = ref('general_official')
const selectedStudentId = ref(null)
const selectedQuestionPaperLayout = ref('a4')
const showQuestionPaperDialog = ref(false)

// ── Multi-Institution Type Adaptation (المدارس / الجامعات / المعاهد) ──
const institutionType = computed(() => {
  return props.activeExam?.institution_type || props.examDetails?.institution_type || props.examDetails?.exam?.institution_type || 'school'
})

const labels = computed(() => {
  const type = institutionType.value
  if (type === 'university') {
    return {
      entityName: 'الكلية / القسم',
      pluralEntities: 'كليات مشمولة',
      activePrefix: 'الكلية/القاعة',
      level1: 'المحافظة / النطاق الأكاديمي',
      level1Placeholder: 'اختر المحافظة / النطاق',
      level1Icon: 'mdi-map-marker-radius',
      level2: 'الكلية / القسم الأكاديمي',
      level2Placeholder: 'اختر الكلية / القسم',
      level2Icon: 'mdi-domain',
      level3: 'القاعة / المركز الامتحاني',
      level3Placeholder: 'اختر القاعة أو المركز الجامعي',
      level3Icon: 'mdi-town-hall',
      filterTitle: 'تصفية نطاق الكليات والجامعات وقاعات الاختبار',
    }
  } else if (type === 'institute') {
    return {
      entityName: 'المعهد / المركز التدريبي',
      pluralEntities: 'معاهد مشمولة',
      activePrefix: 'المعهد',
      level1: 'المحافظة / النطاق التدريبي',
      level1Placeholder: 'اختر المحافظة / النطاق',
      level1Icon: 'mdi-map-marker-radius',
      level2: 'المديرية / المسار والتخصص',
      level2Placeholder: 'اختر المديرية أو المسار المهني',
      level2Icon: 'mdi-office-building-cog',
      level3: 'المعهد / المركز التقني والتدريبي',
      level3Placeholder: 'اختر المعهد أو المركز التدريبي',
      level3Icon: 'mdi-wrench-clock',
      filterTitle: 'تصفية نطاق المعاهد والمراكز المهنية والتقنية',
    }
  }
  // Default: School
  return {
    entityName: 'المدرسة / المركز الامتحاني',
    pluralEntities: 'مدارس مشمولة',
    activePrefix: 'المدرسة',
    level1: 'المحافظة',
    level1Placeholder: 'اختر المحافظة',
    level1Icon: 'mdi-map-marker',
    level2: 'المديرية',
    level2Placeholder: 'اختر المديرية',
    level2Icon: 'mdi-city-variant-outline',
    level3: 'المدرسة / المركز الامتحاني',
    level3Placeholder: 'اختر المدرسة أو المركز الامتحاني',
    level3Icon: 'mdi-school-outline',
    filterTitle: 'تصفية النطاق الجغرافي والمدارس والمراكز الامتحانية',
  }
})

const filterCardLabel = computed(() => labels.value.filterTitle)

// ── Geographic & School Cascading Filters (المحافظة -> المديرية -> المدرسة) ──
const filterGovernorate = ref(null)
const filterDirectorate = ref(null)
const filterSchool = ref(null)

const governorateOptions = computed(() => {
  const set = new Set()
  if (props.activeExam?.governorate) set.add(props.activeExam.governorate)
  const students = props.examDetails?.registered_students || []
  students.forEach(s => {
    if (s.governorate) set.add(s.governorate)
  })
  return Array.from(set).map(g => ({ title: g, value: g }))
})

const directorateOptions = computed(() => {
  const set = new Set()
  if (!filterGovernorate.value || filterGovernorate.value === props.activeExam?.governorate) {
    if (props.activeExam?.directorate) set.add(props.activeExam.directorate)
  }
  const students = props.examDetails?.registered_students || []
  students.forEach(s => {
    if (!filterGovernorate.value || s.governorate === filterGovernorate.value) {
      if (s.directorate) set.add(s.directorate)
    }
  })
  return Array.from(set).map(d => ({ title: d, value: d }))
})

const schoolOptions = computed(() => {
  const map = new Map()
  const students = props.examDetails?.registered_students || []
  students.forEach(s => {
    const matchGov = !filterGovernorate.value || s.governorate === filterGovernorate.value
    const matchDir = !filterDirectorate.value || s.directorate === filterDirectorate.value
    if (matchGov && matchDir && s.school_name) {
      if (!map.has(s.school_name)) {
        map.set(s.school_name, {
          title: s.school_name,
          value: s.school_name,
          id: s.school_id,
          count: 1
        })
      } else {
        map.get(s.school_name).count++
      }
    }
  })
  return Array.from(map.values())
})

const filteredStudents = computed(() => {
  let list = props.examDetails?.registered_students || []
  if (filterGovernorate.value) {
    list = list.filter(s => s.governorate === filterGovernorate.value)
  }
  if (filterDirectorate.value) {
    list = list.filter(s => s.directorate === filterDirectorate.value)
  }
  if (filterSchool.value) {
    list = list.filter(s => s.school_name === filterSchool.value)
  }
  return list
})

const resetFilters = () => {
  filterGovernorate.value = null
  filterDirectorate.value = null
  filterSchool.value = null
  selectedStudentId.value = null
}

const effectiveGovernorate = computed(() => {
  return filterGovernorate.value ||
         props.customGovernorate ||
         activeStudent.value?.governorate ||
         props.activeExam?.governorate ||
         ''
})

const effectiveDirectorate = computed(() => {
  return filterDirectorate.value ||
         props.customDirectorate ||
         activeStudent.value?.directorate ||
         props.activeExam?.directorate ||
         ''
})

const totalRegisteredCount = computed(() => {
  return props.examDetails?.registered_students_count ??
         props.examDetails?.registered_students?.length ??
         props.activeExam?.registered_students_count ??
         0
})

const uniqueSchoolsCount = computed(() => {
  const students = props.examDetails?.registered_students || []
  const schools = new Set()
  students.forEach(s => {
    if (s.school_name) schools.add(s.school_name)
  })
  if (schools.size > 0) return schools.size
  return props.activeExam?.unique_schools_count || (props.activeExam?.school_name ? 1 : 0)
})

const auditFindings = computed(() => {
  const issues = []

  // 1. Models / Versions Check
  const versions = props.examDetails?.versions || []
  if (!versions.length) {
    issues.push({
      type: 'error',
      title: 'نماذج الاختبار غير متوفرة',
      desc: 'لم يتم العثور على نماذج أسئلة مولدة لهذا الاختبار في قاعدة البيانات.',
      actionTab: 'keys'
    })
  }

  // 2. Questions in current model
  const currentQuestions = currentVersionObj.value?.questions || []
  if (versions.length > 0 && currentQuestions.length === 0) {
    issues.push({
      type: 'error',
      title: `النموذج (${currentVersionObj.value?.versionCode || 'المحدد'}) خالٍ من الأسئلة`,
      desc: 'لم يتم إضافة أو ربط أي أسئلة في هذا النموذج بعد.',
      actionTab: 'keys'
    })
  }

  // 3. Registered Students Check
  const students = props.examDetails?.registered_students || []
  const totalCount = totalRegisteredCount.value
  if (totalCount === 0) {
    issues.push({
      type: 'warning',
      title: 'لم يتم تسجيل الطلاب في الاختبار',
      desc: 'الاختبار يفتقر لكشف الطلاب وأرقام الجلوس (لا يمكن طباعة أوراق مخصصة للطلاب حتى يتم تسجيلهم).',
      actionTab: 'roster'
    })
  } else {
    const missingSeatNo = students.filter(s => !s.seat_number).length
    if (missingSeatNo > 0) {
      issues.push({
        type: 'warning',
        title: 'أرقام جلوس غير مكتملة',
        desc: `يوجد ${missingSeatNo} طالب بدون رقم جلوس محدد.`,
        actionTab: 'roster'
      })
    }
  }

  // 4. Directorate & Governorate Check
  const gov = props.customGovernorate || props.activeExam?.governorate || students[0]?.governorate
  const dir = props.customDirectorate || props.activeExam?.directorate || students[0]?.directorate
  if (!gov && !dir) {
    issues.push({
      type: 'info',
      title: 'النطاق الجغرافي غير مكتمل',
      desc: 'لم يتم تحديد المحافظة أو المديرية في ترويسة الاختبار.',
      actionTab: 'questions'
    })
  }

  // 5. Answer Keys Check
  if (versions.length > 0) {
    const versionsWithoutKey = versions.filter(v => !v.answerKey || Object.keys(v.answerKey).length === 0)
    if (versionsWithoutKey.length > 0) {
      issues.push({
        type: 'warning',
        title: 'مفاتيح الإجابة بحاجة للاعتماد',
        desc: `توجد ${versionsWithoutKey.length} نماذج تفتقر لمفاتيح الإجابة قبل التصحيح الضوئي.`,
        actionTab: 'keys'
      })
    }
  }

  return {
    hasIssues: issues.length > 0,
    issues
  }
})

const activeStudent = computed(() => {
  if (paperTargetMode.value !== 'student_specific') return null
  const list = filteredStudents.value
  if (selectedStudentId.value) {
    const found = list.find(s => s.id === selectedStudentId.value)
    if (found) return found
  }
  return list[0] || null
})

const effectiveCenterName = computed(() => {
  if (props.customCenterName) return props.customCenterName
  if (activeStudent.value?.school_name) return activeStudent.value.school_name
  if (filterSchool.value) return filterSchool.value
  return props.activeExam?.center_name ||
         props.activeExam?.school_name ||
         filteredStudents.value[0]?.school_name ||
         props.examDetails?.registered_students?.[0]?.school_name ||
         (effectiveDirectorate.value ? `المركز الامتحاني - ${effectiveDirectorate.value}` : '') ||
         'المركز الامتحاني الرئيسي'
})

const effectiveCenterCode = computed(() => {
  if (activeStudent.value?.school_id) return activeStudent.value.school_id
  if (filterSchool.value) {
    const sch = schoolOptions.value.find(s => s.value === filterSchool.value)
    if (sch?.id) return sch.id
  }
  return props.activeExam?.center_code ||
         filteredStudents.value[0]?.school_id ||
         props.examDetails?.registered_students?.[0]?.school_id ||
         props.activeExam?.id ||
         '11'
})

const effectiveEnvelopeNo = computed(() => {
  return props.activeExam?.envelope_no || '1'
})

const currentVersionObj = computed(() => {
  if (!props.examDetails?.versions?.length) return null
  return props.examDetails.versions[props.activeVersionTab] || props.examDetails.versions[0]
})

const versionSelectItems = computed(() => {
  if (!props.examDetails?.versions?.length) return []
  return props.examDetails.versions.map((v, idx) => ({
    title: `النموذج ${v.versionCode} (${v.questions?.length || v.questionsCount || 0} سؤال)`,
    value: idx
  }))
})

const printQuestionsAndSheets = async (mode = 'package') => {
  await nextTick()
  const targetVersion = currentVersionObj.value || props.examDetails?.versions?.[0]

  if (!targetVersion || !targetVersion.questions || !targetVersion.questions.length) {
    console.warn('No questions found to print.')
    return
  }

  const activeVCode = targetVersion.versionCode || 'A'

  await printExamPackage({
    title: mode === 'package'
      ? `حزمة_اختبار_${props.activeExam?.subject_name || 'الاختبار'}_النموذج_${activeVCode}`
      : `كراسة_أسئلة_${props.activeExam?.subject_name || 'الاختبار'}_النموذج_${activeVCode}`,
    examTitle: props.customStageTitle || props.activeExam?.title || '',
    subjectName: props.activeExam?.subject_name || '',
    stageName: props.customStageTitle || (props.activeExam?.stage_name ? `اختبار ${props.activeExam.stage_name}` : ''),
    yearName: (props.customExamYear || (props.activeExam?.year_name && String(props.activeExam.year_name).length > 2 && props.activeExam.year_name !== '1') ? props.activeExam.year_name : ''),
    governorate: effectiveGovernorate.value,
    directorate: effectiveDirectorate.value,
    centerName: effectiveCenterName.value,
    centerCode: effectiveCenterCode.value,
    dayName: props.activeExam?.day_name || '',
    examDate: props.activeExam?.exam_date || '',
    envelopeNo: effectiveEnvelopeNo.value,
    timeAllowed: props.activeExam?.time_allowed || props.activeExam?.exam_time || '',
    versionCode: activeVCode,
    studentName: activeStudent.value ? activeStudent.value.student_name : '',
    seatNumber: activeStudent.value ? activeStudent.value.seat_number : '',
    secretNumber: activeStudent.value ? (activeStudent.value.secret_number || '') : '',
    studentPhoto: activeStudent.value ? (activeStudent.value.student_photo || '') : '',
    schoolName: effectiveCenterName.value,
    institutionType: props.activeExam?.institution_type || 'school',
    questions: targetVersion.questions,
    omrElement: props.getOmrElement ? props.getOmrElement() : null,
    mode: mode,
    isA3: selectedQuestionPaperLayout.value === 'a3',
    isA5: props.selectedSheetLayout === 'compact_a5'
  })
}

defineExpose({
  openQuestionPaperModal: () => { showQuestionPaperDialog.value = true },
  printQuestionsAndSheets,
})
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
</style>
