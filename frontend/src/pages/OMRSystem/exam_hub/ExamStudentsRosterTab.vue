<template>
  <div class="exam-students-roster-tab">
    <!-- Quick Actions & Info Bar -->
    <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
      <div class="d-flex align-center gap-2">
        <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
          <v-icon size="20">mdi-account-group-outline</v-icon>
        </v-avatar>
        <div>
          <div class="text-subtitle-2 font-weight-black text-on-surface">كشف الطلاب المقيدين للاختبار</div>
          <div class="text-caption text-medium-emphasis">إدارة أرقام الجلوس والنماذج المسندة ومعاينة أوراق التظليل</div>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <custom-btn
          type="show"
          icon="file-document-multiple-outline"
          label="معاينة وتوليد أوراق التظليل للجميع"
          color="primary"
          variant="tonal"
          class="font-weight-bold"
          :disabled="!totalStudentsCount"
          :click="() => $emit('switch-to-template', 'all_students')"
        />
        <custom-btn
          type="show"
          icon="format-list-numbered"
          label="طباعة كشف المناداة والجلوس"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
          :disabled="!totalStudentsCount"
          :click="printRosterList"
        />
        <custom-btn
          v-if="!totalStudentsCount"
          type="create"
          icon="account-multiple-plus"
          label="تسجيل الطلاب المقيدين في الاختبار"
          color="primary"
          variant="tonal"
          class="font-weight-bold"
          :loading="seedingStudents"
          :click="() => $emit('seed-students')"
        />
      </div>
    </div>

    <!-- Unified Filter Fields for Students (Backend Filtering) -->
    <filter-fields label="خيارات تصفية كشف الطلاب والبيانات الامتحانية" class="main-card border-0 pa-5 rounded-2xl mb-4">
      <v-row dense class="align-center">
        <!-- Search Query -->
        <v-col cols="12" md="5">
          <v-text-field
            v-model="studentSearchQuery"
            label="اسم الطالب أو رقم الجلوس أو الرقم السري"
            placeholder="بحث بالاسم، رقم الجلوس، أو الرقم السري..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="onStudentSearchInput"
            @keydown.enter="applyStudentFilters"
          />
        </v-col>

        <!-- Model Code -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterModelCode"
            :items="modelFilterOptions"
            item-title="title"
            item-value="value"
            label="النموذج الامتحاني"
            prepend-inner-icon="mdi-format-list-bulleted-type"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="applyStudentFilters"
          />
        </v-col>

        <!-- School Name -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterSchoolName"
            :items="schoolFilterOptions"
            item-title="title"
            item-value="value"
            :label="institutionLabel"
            prepend-inner-icon="mdi-school-outline"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="applyStudentFilters"
          />
        </v-col>

        <!-- Action: Reset -->
        <v-col cols="12" md="1" class="d-flex align-center">
          <custom-btn
            type="cancel_filter"
            :click="resetStudentFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6 w-100"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Students Unified Custom Data Table (Server-side Paginated) -->
    <div class="main-card rounded-2xl overflow-hidden mb-4">
      <custom-data-table
        v-bind="{
          items: studentTableItems,
          headers: studentHeaders,
          loading: loadingStudents,
        }"
        :getData="fetchExamStudents"
        :customLoading="loadingStudents"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :showSelect="false"
        :actions="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Seat Number -->
          <template v-if="key === 'seat_number'">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold font-mono unified-table-chip">
              {{ item.seat_number }}
            </v-chip>
          </template>

          <!-- Secret Number -->
          <template v-else-if="key === 'secret_number'">
            <span class="font-mono font-weight-bold text-caption text-medium-emphasis">
              {{ item.secret_number || '—' }}
            </span>
          </template>

          <!-- Student Name -->
          <template v-else-if="key === 'student_name'">
            <div class="d-flex align-center gap-2 py-1">
              <v-avatar size="30" color="primary" variant="tonal" class="rounded-lg">
                <v-icon size="16">mdi-account-outline</v-icon>
              </v-avatar>
              <span class="font-weight-bold text-body-2">{{ item.student_name }}</span>
            </div>
          </template>

          <!-- School Info -->
          <template v-else-if="key === 'school_info'">
            <div class="text-caption">
              <div class="font-weight-bold text-on-surface">{{ item.school_name || '—' }}</div>
              <div class="text-medium-emphasis" v-if="item.governorate || item.directorate">{{ item.governorate }} - {{ item.directorate }}</div>
            </div>
          </template>

          <!-- Model Code -->
          <template v-else-if="key === 'model_code'">
            <v-chip
              size="small"
              variant="tonal"
              :color="item.model_code === 'A' ? 'primary' : item.model_code === 'B' ? 'info' : 'secondary'"
              class="font-weight-bold unified-table-chip"
            >
              النموذج {{ item.model_code }}
            </v-chip>
          </template>

          <!-- Barcode Value -->
          <template v-else-if="key === 'barcode_val'">
            <span class="font-mono text-caption text-medium-emphasis border px-2 py-0.5 rounded bg-grey-lighten-4">
              {{ item.seat_number }}
            </span>
          </template>

          <!-- Attendance -->
          <template v-else-if="key === 'is_present'">
            <v-icon v-if="item.is_present" size="18" color="success">mdi-check-circle</v-icon>
            <v-icon v-else size="18" color="medium-emphasis">mdi-minus-circle-outline</v-icon>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                is-icon
                icon="card-text-outline"
                color="primary"
                label="معاينة وتوليد ورقة التظليل"
                :click="() => $emit('select-student-for-sheet', item)"
              />
              <custom-btn
                is-icon
                icon="printer"
                color="secondary"
                label="طباعة ورقة هذا الطالب"
                :click="() => $emit('print-student-sheet', item)"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/omr/client.js'

const props = defineProps({
  activeExam: { type: Object, default: () => ({}) },
  examDetails: { type: Object, default: () => ({}) },
  seedingStudents: { type: Boolean, default: false },
})

const emit = defineEmits([
  'switch-to-template',
  'seed-students',
  'select-student-for-sheet',
  'print-student-sheet',
])

const loadingStudents = ref(false)
const totalStudentsCount = ref(0)
const availableSchools = ref([])
const studentTableData = ref({ results: [], pagination: {} })

const studentSearchQuery = ref('')
const filterModelCode = ref('all')
const filterSchoolName = ref('all')

const institutionLabel = computed(() => {
  const t = props.activeExam?.institution_type
  if (t === 'university') return 'الكلية / القسم'
  if (t === 'institute') return 'المعهد / التخصص'
  return 'المدرسة / المركز'
})

const modelFilterOptions = computed(() => {
  const opts = [{ title: 'كافة النماذج', value: 'all' }]
  if (props.examDetails?.versions && Array.isArray(props.examDetails.versions)) {
    props.examDetails.versions.forEach(v => {
      opts.push({ title: `النموذج ${v.versionCode}`, value: v.versionCode })
    })
  }
  return opts
})

const schoolFilterOptions = computed(() => {
  const opts = [{ title: 'كافة المراكز / المدارس', value: 'all' }]
  if (availableSchools.value && availableSchools.value.length) {
    availableSchools.value.forEach(s => {
      opts.push({ title: s, value: s })
    })
  } else if (props.examDetails?.registered_students && Array.isArray(props.examDetails.registered_students)) {
    const set = new Set()
    props.examDetails.registered_students.forEach(st => {
      if (st.school_name) set.add(st.school_name)
    })
    set.forEach(s => opts.push({ title: s, value: s }))
  }
  return opts
})

const studentHeaders = ref([
  { title: 'رقم الجلوس', key: 'seat_number', sortable: false, width: '110px' },
  { title: 'الرقم السري', key: 'secret_number', sortable: false, width: '100px' },
  { title: 'اسم الطالب', key: 'student_name', sortable: false },
  { title: institutionLabel.value, key: 'school_info', sortable: false },
  { title: 'النموذج', key: 'model_code', sortable: false, width: '100px' },
  { title: 'الباركود', key: 'barcode_val', sortable: false, width: '100px' },
  { title: 'حالة الحضور', key: 'is_present', sortable: false, width: '90px' },
  { title: 'الإجراءات', key: 'actions', sortable: false, width: '110px' },
])

const studentTableItems = computed(() => {
  return studentTableData.value
})

const filteredStudents = computed(() => {
  let list = props.examDetails?.registered_students || []
  if (filterModelCode.value && filterModelCode.value !== 'all') {
    list = list.filter(st => st.model_code === filterModelCode.value)
  }
  if (filterSchoolName.value && filterSchoolName.value !== 'all') {
    list = list.filter(st => st.school_name === filterSchoolName.value)
  }
  if (studentSearchQuery.value && studentSearchQuery.value.trim()) {
    const q = studentSearchQuery.value.trim().toLowerCase()
    list = list.filter(st =>
      (st.student_name && st.student_name.toLowerCase().includes(q)) ||
      (st.seat_number && String(st.seat_number).toLowerCase().includes(q)) ||
      (st.secret_number && String(st.secret_number).toLowerCase().includes(q))
    )
  }
  return list
})

let searchDebounceTimer = null
const onStudentSearchInput = () => {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer)
  searchDebounceTimer = setTimeout(() => {
    fetchExamStudents({ page: 1 })
  }, 400)
}

const applyStudentFilters = () => {
  fetchExamStudents({ page: 1 })
}

const resetStudentFilters = () => {
  studentSearchQuery.value = ''
  filterModelCode.value = 'all'
  filterSchoolName.value = 'all'
  fetchExamStudents({ page: 1 })
}

const fetchExamStudents = async (tableParams = null) => {
  if (!props.activeExam?.id) return
  loadingStudents.value = true
  try {
    let queryParams = {}
    if (tableParams && tableParams.params) {
      queryParams = { ...tableParams.params }
    } else if (tableParams && typeof tableParams === 'object' && ('page' in tableParams || 'page_size' in tableParams || 'perPage' in tableParams)) {
      queryParams = { ...tableParams }
    } else {
      queryParams = { page: 1, page_size: 10 }
    }

    if (studentSearchQuery.value && studentSearchQuery.value.trim()) {
      queryParams.search = studentSearchQuery.value.trim()
    }
    if (filterModelCode.value && filterModelCode.value !== 'all') {
      queryParams.version = filterModelCode.value
    }
    if (filterSchoolName.value && filterSchoolName.value !== 'all') {
      queryParams.school = filterSchoolName.value
    }

    const resp = await api.get(`/api/omr/exam-linking/${props.activeExam.id}/students/`, { params: queryParams })
    const data = resp.data || {}
    const results = data.results || data.students || []
    const pagination = data.pagination || {
      count: data.count || results.length,
      current_page: queryParams.page || 1,
      num_pages: Math.ceil((data.count || results.length) / (queryParams.page_size || queryParams.perPage || 10)) || 1,
      page_size: queryParams.page_size || queryParams.perPage || 10,
      total: data.count || results.length,
    }

    studentTableData.value = {
      ...data,
      results,
      pagination,
    }
    totalStudentsCount.value = pagination.count || data.count || 0

    if (data.schools && Array.isArray(data.schools) && data.schools.length) {
      availableSchools.value = data.schools
    }
  } catch (err) {
    console.error('Failed to load exam students from backend:', err)
  } finally {
    loadingStudents.value = false
  }
}

const printRosterList = () => {
  if (!props.examDetails?.registered_students?.length && !studentTableData.value?.results?.length) return

  const students = filteredStudents.value.length ? filteredStudents.value : (props.examDetails?.registered_students || studentTableData.value.results)
  const exam = props.activeExam

  const iframe = document.createElement('iframe')
  iframe.style.position = 'fixed'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document
  if (!doc) return

  const rows = students.map((s, idx) => `
    <tr>
      <td style="text-align:center; padding: 6px; border: 1px solid #000;">${idx + 1}</td>
      <td style="text-align:center; padding: 6px; border: 1px solid #000; font-weight:bold; font-family:monospace;">${s.seat_number}</td>
      <td style="text-align:center; padding: 6px; border: 1px solid #000; font-family:monospace;">${s.secret_number || '-'}</td>
      <td style="padding: 6px 10px; border: 1px solid #000; font-weight:bold;">${s.student_name}</td>
      <td style="padding: 6px; border: 1px solid #000;">${s.school_name || ''}</td>
      <td style="text-align:center; padding: 6px; border: 1px solid #000; font-weight:bold;">${s.model_code || 'A'}</td>
      <td style="border: 1px solid #000; width: 120px;"></td>
    </tr>
  `).join('')

  doc.open()
  doc.write(`
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <title>كشف مناداة وجلوس الطلاب</title>
      <style>
        @page { size: A4 portrait; margin: 12mm; }
        body { font-family: 'Cairo', Arial, sans-serif; direction: rtl; margin: 0; padding: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
        th { background: #f0f0f0; border: 1px solid #000; padding: 8px; font-weight: bold; }
        .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
      </style>
    </head>
    <body>
      <div class="header">
        <h2 style="margin: 0 0 5px 0;">${
          exam?.institution_type === 'institute'
            ? 'الجمهورية اليمنية — وزارة التعليم الفني والتدريب المهني'
            : (exam?.institution_type === 'university'
              ? 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'
              : 'الجمهورية اليمنية — وزارة التربية والتعليم')
        }</h2>
        <h3 style="margin: 0 0 5px 0;">كشف مناداة وتوقيع حضور الطلاب للاختبارات</h3>
        <p style="margin: 0; font-size: 14px;"><strong>الاختبار:</strong> ${exam?.title || ''} (${exam?.uniqueCode || ''}) | <strong>المادة:</strong> ${exam?.subject_name || ''} | <strong>العام:</strong> ${exam?.year_name || ''}</p>
      </div>
      <table>
        <thead>
          <tr>
            <th style="width: 40px;">#</th>
            <th style="width: 90px;">رقم الجلوس</th>
            <th style="width: 80px;">الرقم السري</th>
            <th>اسم الطالب الرباعي</th>
            <th>${institutionLabel.value}</th>
            <th style="width: 70px;">النموذج</th>
            <th style="width: 120px;">توقيع الطالب</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    </body>
    </html>
  `)
  doc.close()

  setTimeout(() => {
    iframe.contentWindow?.focus()
    iframe.contentWindow?.print()
    setTimeout(() => {
      if (document.body.contains(iframe)) document.body.removeChild(iframe)
    }, 3000)
  }, 400)
}

onMounted(() => {
  if (props.activeExam?.id) {
    fetchExamStudents({ page: 1 })
  }
})

defineExpose({
  fetchExamStudents,
  printRosterList,
  totalStudentsCount,
})
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
.font-mono {
  font-family: monospace, monospace;
}
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
</style>
