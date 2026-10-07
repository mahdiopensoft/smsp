<template>
  <div class="qb-authors-report-v4">
    <!-- Filters Section -->
    <filter-fields :label="'معايير التصفية والتقرير'" class="mb-4">
      <template #fields>
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            class="mb-6"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 🏫 School Filters -->
        <template v-if="filterInstitutionType === 'school'">
          <auto-list
            v-model="filter_fields.stage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="onStageChange"
          />

          <auto-list
            v-model="filter_fields.class_track"
            name="ClassTrackByStage"
            :param="filter_fields.stage"
            placeholder="الصف والمسار"
            :add="false"
            cols="2"
            :disabled="!filter_fields.stage"
          />
        </template>

        <!-- 🎓 University Filters -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filter_fields.college"
            name="College"
            placeholder="الكلية الجامعية"
            cols="2"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="filter_fields.department"
            name="DepartmentByCollege"
            :param="filter_fields.college"
            placeholder="القسم الأكاديمي"
            cols="2"
            :add="false"
            :disabled="!filter_fields.college"
            @update:model-value="filter_fields.specialization = null"
          />
          <auto-list
            v-model="filter_fields.specialization"
            name="Specialization"
            :param="filter_fields.department"
            placeholder="التخصص والبرنامج"
            cols="2"
            :add="false"
            :disabled="!filter_fields.department"
          />
          <auto-list
            v-model="filter_fields.semesterSubject"
            name="SemesterSubject"
            :param="filter_fields.specialization"
            placeholder="مقرر الفصل الجامعي"
            cols="2"
            :add="false"
          />
        </template>

        <!-- Subject Filter (Schools only) -->
        <auto-list
          v-if="filterInstitutionType !== 'university'"
          v-model="filter_fields.subject"
          name="Subject"
          placeholder="المادة الدراسية"
          :add="false"
          cols="2"
        />

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="filter_fields.search"
            placeholder="بحث باسم المؤلف أو المعلم..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <v-col cols="auto">
          <custom-btn type="filter" :loading="loading" :click="applyFilters" />
        </v-col>
        <v-col cols="auto">
          <custom-btn
            color="primary"
            variant="tonal"
            :click="resetFilters"
            class="font-weight-bold rounded-lg px-6"
            label="إعادة ضبط"
            icon="mdi-refresh"
          />
        </v-col>
      </template>
    </filter-fields>

    <!-- Authors Table -->
    <CustomCard class="glass-card rounded-xl overflow-hidden" elevation="0">
      <custom-data-table
        ref="table"
        v-bind="{
          items: filteredAuthors,
          headers,
        }"
        hover
        class="bg-transparent"
        :items-per-page="15"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :customLoading="loading"
      >
        <!-- Rank -->
        <template v-slot:item.rank="{ index }">
          <v-avatar
            :color="index === 0 ? 'amber-lighten-4' : index === 1 ? 'blue-grey-lighten-4' : index === 2 ? 'brown-lighten-4' : 'grey-lighten-4'"
            size="32"
            class="font-weight-bold text-caption"
            :class="index === 0 ? 'text-amber-darken-4' : index === 1 ? 'text-blue-grey-darken-2' : index === 2 ? 'text-brown-darken-3' : 'text-grey-darken-2'"
          >
            {{ index + 1 }}
          </v-avatar>
        </template>

        <!-- Author Name -->
        <template v-slot:item.name="{ item }">
          <div class="d-flex align-center py-2">
            <v-avatar color="primary" size="38" variant="tonal" class="me-3 font-weight-bold">
              <span>{{ item.name ? item.name.charAt(0) : 'م' }}</span>
            </v-avatar>
            <div>
              <div class="font-weight-bold text-body-1">{{ item.name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.email || item.role || 'مؤلف معتمد' }}</div>
            </div>
          </div>
        </template>

        <!-- Academic Info -->
        <template v-slot:item.academicInfo="{ item }">
          <div>
            <div class="d-flex align-center gap-1 flex-wrap">
              <v-chip
                size="x-small"
                :color="item.institutionType === 'university' ? 'deep-purple' : 'teal'"
                variant="tonal"
                class="font-weight-bold"
              >
                {{ item.institutionType === 'university' ? '🎓 جامعي' : '🏫 مدرسي' }}
              </v-chip>
              <span class="font-weight-bold text-primary">{{ item.subjectName }}</span>
            </div>
            <div class="text-caption text-medium-emphasis">{{ item.levelName }} - {{ item.branchName }}</div>
          </div>
        </template>

        <!-- Total Questions -->
        <template v-slot:item.total="{ item }">
          <v-chip color="primary" variant="tonal" size="small" class="font-weight-bold px-3">
            {{ item.total }} سؤال
          </v-chip>
        </template>

        <!-- Approved Questions -->
        <template v-slot:item.approved="{ item }">
          <div class="font-weight-bold text-success d-flex align-center">
            <v-icon size="16" class="me-1">mdi-check-circle</v-icon>
            {{ item.approved }}
          </div>
        </template>

        <!-- Pending Questions -->
        <template v-slot:item.pending="{ item }">
          <div class="font-weight-bold text-warning d-flex align-center">
            <v-icon size="16" class="me-1">mdi-clock-outline</v-icon>
            {{ item.pending }}
          </div>
        </template>

        <!-- Rejected Questions -->
        <template v-slot:item.rejected="{ item }">
          <div class="font-weight-bold text-error d-flex align-center">
            <v-icon size="16" class="me-1">mdi-close-circle</v-icon>
            {{ item.rejected }}
          </div>
        </template>

        <!-- Approval Rate -->
        <template v-slot:item.approvalRate="{ item }">
          <div class="d-flex align-center">
            <v-progress-linear
              :model-value="item.approvalRate"
              :color="getApprovalColor(item.approvalRate)"
              height="8"
              rounded
              style="width: 70px;"
              class="me-3"
            />
            <span :class="'font-weight-bold text-' + getApprovalColor(item.approvalRate)">
              {{ item.approvalRate }}%
            </span>
          </div>
        </template>

        <!-- Last Activity -->
        <template v-slot:item.lastActivity="{ item }">
          <v-chip size="small" variant="tonal" class="text-medium-emphasis">
            {{ item.lastActivity || 'مؤخراً' }}
          </v-chip>
        </template>
      </custom-data-table>
    </CustomCard>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const authorsList = ref([])

// ──────────────────────────────────────────────────
// INSTITUTION & FILTERS STATE
// ──────────────────────────────────────────────────
const filterInstitutionType = ref('all')
const institutionTypeOptions = [
  { text: "الكل (مدارس وجامعات)", value: "all" },
  { text: "🏫 مدارس فقط", value: "school" },
  { text: "🎓 جامعات فقط", value: "university" },
]

const filter_fields = ref({
  stage: null,
  class_track: null,
  college: null,
  department: null,
  specialization: null,
  semesterSubject: null,
  subject: null,
  search: '',
})

const onInstitutionTypeChange = () => {
  filter_fields.value.stage = null
  filter_fields.value.class_track = null
  filter_fields.value.college = null
  filter_fields.value.department = null
  filter_fields.value.specialization = null
  filter_fields.value.semesterSubject = null
  filter_fields.value.subject = null
  applyFilters()
}

const onStageChange = () => {
  filter_fields.value.class_track = null
}

const onCollegeChange = () => {
  filter_fields.value.department = null
  filter_fields.value.specialization = null
  filter_fields.value.semesterSubject = null
}

const applyFilters = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      params.institution_type = filterInstitutionType.value
    }
    if (filter_fields.value.stage) params.stage = filter_fields.value.stage
    if (filter_fields.value.class_track) params.class_track = filter_fields.value.class_track
    if (filter_fields.value.college) params.college = filter_fields.value.college
    if (filter_fields.value.department) params.department = filter_fields.value.department
    if (filter_fields.value.specialization) params.specialization = filter_fields.value.specialization
    if (filter_fields.value.semesterSubject) params.semester_subject = filter_fields.value.semesterSubject
    if (filter_fields.value.subject) params.subject = filter_fields.value.subject
    if (filter_fields.value.search) params.search = filter_fields.value.search

    const res = await reportsService.getAuthorsReport(params)
    authorsList.value = res.results || (Array.isArray(res) ? res : [])
  } catch (err) {
    console.error('Error loading authors report data:', err)
  } finally {
    loading.value = false
  }
}

const resetFilters = async () => {
  filterInstitutionType.value = 'all'
  filter_fields.value = {
    stage: null,
    class_track: null,
    college: null,
    department: null,
    specialization: null,
    semesterSubject: null,
    subject: null,
    search: '',
  }
  await applyFilters()
}

// Filtered Authors for Table
const filteredAuthors = computed(() => {
  return authorsList.value
})

// Table Headers (Dynamic by Institution Type)
const headers = computed(() => {
  const isUniv = filterInstitutionType.value === 'university'
  return [
    { title: '#', key: 'rank', sortable: false, width: '60px' },
    { title: 'المؤلف / المعلم', key: 'name', sortable: true },
    { title: isUniv ? 'المقرر والتخصص' : 'المادة والصف', key: 'academicInfo', sortable: false },
    { title: 'إجمالي الأسئلة', key: 'total', sortable: true },
    { title: 'معتمدة', key: 'approved', sortable: true },
    { title: 'قيد المراجعة', key: 'pending', sortable: true },
    { title: 'مرفوضة', key: 'rejected', sortable: true },
    { title: 'معدل الاعتماد', key: 'approvalRate', sortable: true },
    { title: 'آخر نشاط', key: 'lastActivity', sortable: true },
  ]
})

// Rate color helper
const getApprovalColor = (rate) => {
  if (rate >= 80) return 'success'
  if (rate >= 60) return 'warning'
  return 'error'
}

// Backend Data Fetching
onMounted(async () => {
  await applyFilters()
})
</script>

<style scoped>
.qb-authors-report-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.glass-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
</style>
