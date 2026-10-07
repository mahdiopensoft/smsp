<template>
  <div class="qb-human-review-v4 pa-4 pa-md-6">
    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-account-eye-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">المراجعة والتدقيق البشري</h1>
          <p class="text-caption text-medium-emphasis mb-0">أوراق الإجابة ذات درجات الثقة المنخفضة أو التظليل الملتبس التي تتطلب تدقيقاً وتحققاً.</p>
        </div>
      </div>

      <div>
        <custom-btn
          label="تحديث البيانات"
          icon="refresh"
          variant="tonal"
          color="primary"
          :loading="loading"
          :click="fetchData"
        />
      </div>
    </div>

    <!-- Stats Cards (Disciplined, Calm Colors) -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <div class="stat-card pa-4 rounded-xl border d-flex align-center justify-space-between">
          <div>
            <div class="text-caption text-medium-emphasis font-weight-bold">تتطلب تدقيق يدوي</div>
            <div class="text-h5 font-weight-black text-warning">{{ stats.pendingReview || 0 }}</div>
          </div>
          <v-avatar color="warning" variant="tonal" rounded="lg"><v-icon size="22">mdi-alert-circle-outline</v-icon></v-avatar>
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <div class="stat-card pa-4 rounded-xl border d-flex align-center justify-space-between">
          <div>
            <div class="text-caption text-medium-emphasis font-weight-bold">أوراق بتظليل ملتبس</div>
            <div class="text-h5 font-weight-black text-error">{{ stats.ambiguousSheets || 0 }}</div>
          </div>
          <v-avatar color="error" variant="tonal" rounded="lg"><v-icon size="22">mdi-help-circle-outline</v-icon></v-avatar>
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <div class="stat-card pa-4 rounded-xl border d-flex align-center justify-space-between">
          <div>
            <div class="text-caption text-medium-emphasis font-weight-bold">أوراق تم التحقق منها</div>
            <div class="text-h5 font-weight-black text-success">{{ stats.verifiedSheets || 0 }}</div>
          </div>
          <v-avatar color="success" variant="tonal" rounded="lg"><v-icon size="22">mdi-check-decagram</v-icon></v-avatar>
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <div class="stat-card pa-4 rounded-xl border d-flex align-center justify-space-between">
          <div>
            <div class="text-caption text-medium-emphasis font-weight-bold">إجمالي الأوراق</div>
            <div class="text-h5 font-weight-black text-primary">{{ stats.totalSheets || 0 }}</div>
          </div>
          <v-avatar color="primary" variant="tonal" rounded="lg"><v-icon size="22">mdi-file-document-multiple-outline</v-icon></v-avatar>
        </div>
      </v-col>
    </v-row>

    <!-- Filters Control Bar (Standard filter-fields) -->
    <filter-fields label="خيارات تصفية أوراق المراجعة والتدقيق" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            class="mb-6"
            label="نوع المؤسسة"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 🏫 School Filters -->
        <template v-if="filterInstitutionType === 'school' || filterInstitutionType === 'all'">
          <auto-list
            v-if="filterInstitutionType === 'school'"
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-if="filterInstitutionType === 'school'"
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            cols="3"
            :add="false"
            :disabled="!filterStage"
          />
        </template>

        <!-- 🎓 University Filters -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filterCollege"
            name="College"
            placeholder="الكلية الجامعية"
            cols="3"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="filterDepartment"
            name="DepartmentByCollege"
            :param="filterCollege"
            placeholder="القسم الأكاديمي"
            cols="3"
            :add="false"
            :disabled="!filterCollege"
            @update:model-value="filterSpecialization = null"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            placeholder="التخصص والبرنامج"
            cols="3"
            :add="false"
            :disabled="!filterDepartment"
          />
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي"
            cols="3"
            :add="false"
          />
        </template>

        <!-- Common Subject Filter (Hidden in university mode) -->
        <auto-list
          v-if="filterInstitutionType !== 'university'"
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="3"
          :add="false"
        />

        <!-- Exam Filter -->
        <auto-list
          v-model="filterExam"
          name="Exam"
          :param="examFilterParam"
          placeholder="الاختبار"
          cols="3"
          :add="false"
        />

        <!-- Status Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterStatus"
            :items="statusOptions"
            item-title="title"
            item-value="value"
            label="حالة المراجعة"
            placeholder="حالة المراجعة"
            prepend-inner-icon="mdi-list-status"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            label="اسم الطالب أو رقم القيد"
            placeholder="بحث برقم السجل أو الطالب..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Action Buttons (Standard style matching /levels) -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="fetchData"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Unified Data Table (matching standard /levels) -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table
        v-bind="{
          items: tableItems,
          getData,
          headers,
        }"
        :customLoading="loading"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Student Info -->
          <template v-if="key === 'student_info'">
            <div class="py-1">
              <div class="font-weight-bold text-body-2 text-on-surface">
                {{ item.student_name || ('ورقة #' + item.id) }}
              </div>
              <div v-if="item.seat_number" class="text-caption text-medium-emphasis mt-1">
                {{ item.institution_type === 'university' ? 'رقم القيد:' : 'رقم الجلوس:' }}
                <span class="font-weight-bold text-on-surface ms-1">{{ item.seat_number }}</span>
              </div>
            </div>
          </template>

          <!-- Exam -->
          <template v-else-if="key === 'exam_title'">
            <div class="py-1">
              <div class="text-body-2 font-weight-medium text-truncate" style="max-width: 250px;">
                {{ item.exam_title || 'اختبار عام' }}
              </div>
              <div class="text-caption text-medium-emphasis mt-1">
                {{ item.institution_type === 'university' ? 'جامعي' : 'مدرسي' }}
              </div>
            </div>
          </template>

          <!-- Confidence -->
          <template v-else-if="key === 'confidence'">
            <v-chip
              size="small"
              :color="item.confidence >= 0.85 ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              {{ Math.round((item.confidence || 0) * 100) }}%
            </v-chip>
          </template>

          <!-- Ambiguous questions -->
          <template v-else-if="key === 'ambiguous_count'">
            <v-chip
              v-if="item.ambiguous_count > 0"
              size="small"
              color="error"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              <v-icon start size="13">mdi-alert-circle-outline</v-icon>
              {{ item.ambiguous_count }} أسئلة
            </v-chip>
            <span v-else class="text-medium-emphasis text-caption">-</span>
          </template>

          <!-- Score -->
          <template v-else-if="key === 'score'">
            <span class="font-weight-bold text-body-2">
              {{ item.mcq_score != null ? item.mcq_score : 0 }} / {{ item.mcq_max_score != null ? item.mcq_max_score : 0 }}
            </span>
          </template>

          <!-- Status -->
          <template v-else-if="key === 'status'">
            <v-chip
              size="small"
              :color="item.status === 'verified' ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              <v-icon start size="14">{{ item.status === 'verified' ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
              {{ item.status === 'verified' ? 'معتمد' : 'قيد التدقيق' }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                v-if="item.status !== 'verified'"
                type="ok"
                is-icon
                label="اعتماد ومصادقة النتيجة"
                :click="() => approveSheet(item)"
              />
              <custom-btn
                v-else
                type="done"
                is-icon
                label="تم الاعتماد مسبقاً"
                disabled
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance } from 'vue'
import { humanReviewAPI } from '@/services/omr/endpoints.js'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const sheets = ref([])
const stats = ref({ pendingReview: 0, ambiguousSheets: 0, verifiedSheets: 0, totalSheets: 0 })

// Table headers (Clean & Professional, no color overload)
const headers = computed(() => [
  { title: "الطالب ورقم الجلوس / القيد", key: "student_info", sortable: true },
  { title: "الاختبار", key: "exam_title", sortable: true },
  { title: "نسبة الثقة", key: "confidence", sortable: true, align: "center", width: "130px" },
  { title: "الأسئلة الملتبسة", key: "ambiguous_count", sortable: true, align: "center", width: "140px" },
  { title: "الدرجة المقدرة", key: "score", sortable: false, align: "center", width: "130px" },
  { title: "حالة المراجعة", key: "status", sortable: true, align: "center", width: "130px" },
])

// Bound items for custom-data-table
const tableItems = computed(() => ({
  results: sheets.value,
  count: sheets.value.length,
  pagination: {
    count: sheets.value.length,
    total: sheets.value.length,
  },
}))

// Filters
const filterInstitutionType = ref('all')
const institutionTypeOptions = [
  { text: "الكل (مدارس وجامعات)", value: "all" },
  { text: "مدارس فقط", value: "school" },
  { text: "جامعات فقط", value: "university" },
]
const filterCollege = ref(null)
const filterDepartment = ref(null)
const filterSpecialization = ref(null)
const filterSemesterSubject = ref(null)
const filterStage = ref(null)
const filterClassTrack = ref(null)
const filterSubject = ref(null)
const filterExam = ref(null)
const filterStatus = ref(null)
const searchQuery = ref('')

const examFilterParam = computed(() => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  if (filterInstitutionType.value === 'school') {
    if (filterClassTrack.value) p.class_track = filterClassTrack.value
    if (filterStage.value) p.stage = filterStage.value
    if (filterSubject.value) p.subject = filterSubject.value
  } else if (filterInstitutionType.value === 'university') {
    if (filterSemesterSubject.value) p.semester_subject = filterSemesterSubject.value
    if (filterSpecialization.value) p.specialization = filterSpecialization.value
    if (filterDepartment.value) p.department = filterDepartment.value
    if (filterCollege.value) p.college = filterCollege.value
  } else {
    if (filterSubject.value) p.subject = filterSubject.value
  }
  return Object.keys(p).length > 0 ? p : null
})

const statusOptions = [
  { title: 'كافة الحالات', value: null },
  { title: 'تتطلب تدقيق يدوي', value: 'pending' },
  { title: 'معتمدة ومحققة', value: 'verified' },
]

const onInstitutionTypeChange = () => {
  filterStage.value = null
  filterClassTrack.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterSubject.value = null
  filterExam.value = null
  fetchData()
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
}

const onStageChange = () => {
  filterClassTrack.value = null
}

const resetFilters = () => {
  filterInstitutionType.value = 'all'
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterStage.value = null
  filterClassTrack.value = null
  filterSubject.value = null
  filterExam.value = null
  filterStatus.value = null
  searchQuery.value = ''
  fetchData()
}

const getData = async (params = {}) => {
  return await fetchData(params)
}

const fetchData = async () => {
  loading.value = true
  try {
    const queryParams = {
      institution_type: (filterInstitutionType.value && filterInstitutionType.value !== 'all') ? filterInstitutionType.value : undefined,
      college: filterCollege.value || undefined,
      department: filterDepartment.value || undefined,
      specialization: filterSpecialization.value || undefined,
      semester_subject: filterSemesterSubject.value || undefined,
      stage: filterStage.value || undefined,
      class_track: filterClassTrack.value || undefined,
      subject: filterSubject.value || undefined,
      exam: filterExam.value || undefined,
      status: filterStatus.value || undefined,
      search: searchQuery.value || undefined,
    }
    const [statsRes, listRes] = await Promise.all([
      humanReviewAPI.getStats(),
      humanReviewAPI.list(queryParams)
    ])
    stats.value = statsRes?.data || stats.value
    const results = listRes?.data?.results || listRes?.data || []
    sheets.value = Array.isArray(results) ? results : []
    return tableItems.value
  } catch (err) {
    console.error('Failed to load human review data', err)
    return { results: [], count: 0 }
  } finally {
    loading.value = false
  }
}

const approveSheet = async (sheet) => {
  try {
    await humanReviewAPI.approveReview(sheet.id)
    proxy.$alert('success', { message: 'تم اعتماد نتيجة ورقة الإجابة بنجاح' })
    await fetchData()
  } catch (err) {
    proxy.$alert('errorData', { message: 'فشل اعتماد الورقة' })
    console.error(err)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.qb-human-review-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.main-card, .stat-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
</style>
