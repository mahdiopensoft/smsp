<template>
  <div class="exam-students-roster-tab">
    <!-- Unified Filter Fields for Students (Backend Filtering) -->
    <filter-fields label="خيارات تصفية كشف الطلاب والبيانات الامتحانية" class="main-card border-0 pa-4 rounded-2xl mb-4">
      <template #fields>

        <!-- Model Code -->
        <auto-list
          v-model="filterModelCode"
          name="ExamHubModel"
          :objects="modelFilterOptions"
          cols="3"
          :add="false"
          :clearable="false"
        />

        <!-- School Name -->
        <auto-list
          v-model="filterSchoolName"
          name="ExamHubSchool"
          :objects="schoolFilterOptions"
          cols="3"
          :label="institutionLabel"
          :add="false"
          :clearable="false"
        />

        <!-- Actions -->
        <v-col cols="auto" class="d-flex align-center gap-2 mb-6">
          <custom-btn
            type="show"
            label="عرض"
            color="primary"
            class="font-weight-bold px-5"
            :click="applyStudentFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetStudentFilters"
            variant="tonal"
            color="error"
            label="إلغاء الفلترة"
            class="font-weight-bold"
          />
        </v-col>
      </template>
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
      
        :actionList="(item) => ([ { label: 'معاينة وتوليد ورقة التظليل', icon: 'card-text-outline', color: 'primary', onClick: () => $emit('select-student-for-sheet', item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
        <template v-slot:item-slot="{ item, key }">
          <!-- Seat Number -->
          <template v-if="key === 'seat_number'">
            <span class="font-weight-bold font-mono text-primary">{{ item.seat_number }}</span>
          </template>

          <!-- Secret Number -->
          <template v-else-if="key === 'secret_number'">
            <span class="font-mono font-weight-bold text-caption text-medium-emphasis">
              {{ item.secret_number || '—' }}
            </span>
          </template>

          <!-- Student Name -->
          <template v-else-if="key === 'student_name'">
            <span class="font-weight-bold text-body-2">{{ item.student_name }}</span>
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
            <span class="font-mono font-weight-bold text-body-2">النموذج {{ item.model_code }}</span>
          </template>

          <!-- Barcode Value -->
          <template v-else-if="key === 'barcode_val'">
            <span class="font-mono text-caption text-medium-emphasis">{{ item.seat_number }}</span>
          </template>

          <!-- Attendance -->
          <template v-else-if="key === 'is_present'">
            <v-chip size="x-small" :color="item.is_present ? 'success' : 'grey'" variant="tonal" class="font-weight-bold">
              {{ item.is_present ? 'حاضر' : 'غائب' }}
            </v-chip>
          </template>

          <!-- Actions -->
          
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
    return studentTableData.value
  } catch (err) {
    console.error('Failed to load exam students from backend:', err)
  } finally {
    loadingStudents.value = false
  }
}

onMounted(() => {
  if (props.activeExam?.id) {
    fetchExamStudents({ page: 1 })
  }
})

defineExpose({
  fetchExamStudents,
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
