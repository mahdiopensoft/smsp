<template>
  <div class="qb-curriculum-report-v4">
    <!-- Filters Section -->
    <filter-fields :label="'معايير التصفية والتقرير (مدرسي / جامعي)'" class="mb-4">
      <template #fields>
        <!-- Institution Type Filter -->
        <v-col cols="12" md="2">
          <v-select
            v-model="filter_fields.institution_type"
            :items="[
              { title: '🏫 الكل (مدارس وجامعات)', value: 'all' },
              { title: '🏫 التعليم المدرسي فقط', value: 'school' },
              { title: '🎓 التعليم الجامعي فقط', value: 'university' }
            ]"
            label="نوع المنشأة"
            variant="outlined"
            density="comfortable"
            hide-details
            rounded="lg"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- School Filters (Stage, ClassTrack, Subject) -->
        <template v-if="filter_fields.institution_type !== 'university'">
          <!-- Stage Filter -->
          <auto-list
            v-model="filter_fields.stage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="onStageChange"
          />

          <!-- ClassTrack Filter (الصف والمسار) -->
          <auto-list
            v-model="filter_fields.class_track"
            name="ClassTrackByStage"
            :param="filter_fields.stage"
            placeholder="الصف والمسار"
            :add="false"
            cols="2"
            :disabled="!filter_fields.stage"
          />

          <!-- Subject Filter -->
          <auto-list
            v-model="filter_fields.subject"
            name="Subject"
            placeholder="المادة الدراسية"
            :add="false"
            cols="2"
          />
        </template>

        <!-- University Filters (College, Department, Specialization, SemesterSubject) -->
        <template v-if="filter_fields.institution_type !== 'school'">
          <auto-list
            v-model="filter_fields.college"
            name="College"
            placeholder="الكلية"
            :add="false"
            cols="2"
            @update:model-value="onCollegeChange"
          />

          <auto-list
            v-model="filter_fields.department"
            name="DepartmentByCollege"
            :param="filter_fields.college"
            placeholder="القسم الأكاديمي"
            :add="false"
            cols="2"
            :disabled="!filter_fields.college"
          />

          <auto-list
            v-model="filter_fields.specialization"
            name="Specialization"
            placeholder="التخصص الجامعي"
            :add="false"
            cols="2"
          />

          <auto-list
            v-model="filter_fields.semester_subject"
            name="SemesterSubject"
            placeholder="المقرر الجامعي"
            :add="false"
            cols="2"
          />
        </template>

        <!-- Status Filter -->
        <v-col cols="12" md="2">
          <v-select
            v-model="filter_fields.status"
            :items="statusOptions"
            item-title="text"
            item-value="value"
            label="الحالة"
            variant="outlined"
            density="comfortable"
            bg-color="surface"
            hide-details
            rounded="lg"
          />
        </v-col>

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="filter_fields.search"
            placeholder="بحث باسم الدرس أو الوحدة..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            hide-details
          />
        </v-col>

        <v-col cols="auto" class="d-flex align-center">
          <custom-btn type="filter" :loading="loading" :click="applyFilters" />
        </v-col>
        <v-col cols="auto" class="d-flex align-center">
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

    <!-- Lessons Table -->
    <CustomCard class="glass-card rounded-xl overflow-hidden" elevation="0">
      <custom-data-table
        ref="table"
        v-bind="{
          items: filteredLessons,
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
        <!-- Institution Type -->
        <template v-slot:item.institutionType="{ item }">
          <v-chip
            size="x-small"
            :color="item.institutionType === 'university' ? 'primary' : 'secondary'"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon size="12" start>{{ item.institutionType === 'university' ? 'mdi-school' : 'mdi-domain' }}</v-icon>
            {{ item.institutionType === 'university' ? 'جامعي' : 'مدرسي' }}
          </v-chip>
        </template>

        <!-- Lesson Name -->
        <template v-slot:item.name="{ item }">
          <div class="d-flex align-center py-2">
            <v-avatar size="36" color="primary" variant="tonal" class="me-3 font-weight-bold">
              <v-icon size="18">mdi-book-open-page-variant</v-icon>
            </v-avatar>
            <div>
              <div class="font-weight-bold text-body-1">{{ item.name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.unit }}</div>
            </div>
          </div>
        </template>

        <!-- Subject -->
        <template v-slot:item.subject="{ item }">
          <span class="font-weight-bold text-primary">{{ item.subject }}</span>
        </template>

        <!-- Level & Branch Info -->
        <template v-slot:item.levelInfo="{ item }">
          <div>
            <div class="font-weight-medium">{{ item.levelName }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.branchName }}</div>
          </div>
        </template>

        <!-- Status -->
        <template v-slot:item.status="{ item }">
          <v-chip
            size="small"
            :color="item.isActive ? 'success' : 'error'"
            variant="tonal"
            class="font-weight-bold px-3"
          >
            <v-icon size="14" start>{{ item.isActive ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
            {{ item.isActive ? 'نشط' : 'محذوف' }}
          </v-chip>
        </template>

        <!-- Deactivation Date -->
        <template v-slot:item.deactivationDate="{ item }">
          <span v-if="!item.isActive" class="text-caption text-error font-weight-bold">
            {{ item.deactivationDate || '-' }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Questions Count -->
        <template v-slot:item.questionsCount="{ item }">
          <v-chip :color="!item.isActive ? 'warning' : 'primary'" variant="tonal" size="small" class="font-weight-bold px-3">
            {{ item.questionsCount }} سؤال
          </v-chip>
        </template>

        <!-- Reason -->
        <template v-slot:item.reason="{ item }">
          <span v-if="!item.isActive" class="text-caption text-medium-emphasis">
            {{ item.reason || 'تحديث المنهج' }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Actions -->
        <template v-slot:item.actions="{ item }">
          <custom-btn
            isIcon
            icon="mdi-history"
            color="primary"
            variant="tonal"
            size="small"
            :click="() => viewHistory(item)"
          >
            <v-tooltip activator="parent" location="top">سجل التغييرات</v-tooltip>
          </custom-btn>
        </template>
      </custom-data-table>
    </CustomCard>

    <!-- History Dialog -->
    <CustomDialog v-model="historyDialog" title="سجل تغييرات الدرس" max-width="500">
      <template #default>
        <div v-if="selectedLesson" class="pa-6 bg-surface">
          <v-card variant="outlined" color="info" class="mb-6 pa-4 rounded-lg bg-info-lighten-5">
            <div class="d-flex align-center">
              <v-icon color="info" class="me-3">mdi-book-open-blank-variant</v-icon>
              <div class="font-weight-bold text-info-darken-2">{{ selectedLesson.name }}</div>
            </div>
          </v-card>

          <div v-if="historyLoading" class="d-flex justify-center py-10">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>

          <div v-else-if="lessonHistory.length === 0" class="text-center py-8 text-medium-emphasis">
            <v-icon size="48" class="mb-3 opacity-50">mdi-history</v-icon>
            <div>لا يوجد سجل تغييرات متاح لهذا الدرس</div>
          </div>

          <v-timeline v-else density="compact" side="end">
            <v-timeline-item
              v-for="entry in lessonHistory"
              :key="entry.id"
              :dot-color="entry.color"
              size="small"
            >
              <template v-slot:opposite>
                <span class="text-caption text-medium-emphasis font-weight-bold">{{ entry.dateString }}</span>
              </template>
              <v-card elevation="0" :class="`border border-${entry.color}-lighten-4 bg-${entry.color}-lighten-5 rounded-lg pa-3`">
                <div :class="`font-weight-bold text-${entry.color}`">{{ entry.actionText }}</div>
                <div class="text-caption text-medium-emphasis mt-1 d-flex align-center">
                  <v-icon size="14" class="me-1">mdi-account-circle-outline</v-icon>
                  {{ entry.actor_name }}
                </div>
              </v-card>
            </v-timeline-item>
          </v-timeline>
        </div>
      </template>
      <template #actions>
        <custom-btn
          type="add"
          label="إغلاق"
          color="primary"
          variant="text"
          size="large"
          class="font-weight-bold px-6 rounded-lg"
          :click="() => historyDialog = false"
        />
      </template>
    </CustomDialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import { academicService } from '@/services/academicService'
import { reportsService } from '@/services/reportsService'

const store = useDataStore()
const loading = ref(false)
const historyDialog = ref(false)
const selectedLesson = ref(null)
const historyLoading = ref(false)
const lessonHistory = ref([])
const lessonsList = ref([])

// ──────────────────────────────────────────────────
// FILTERS STATE
// ──────────────────────────────────────────────────
const filter_fields = ref({
  institution_type: 'all',
  stage: null,
  class_track: null,
  subject: null,
  college: null,
  department: null,
  specialization: null,
  semester_subject: null,
  status: 'all',
  search: '',
})

const onInstitutionTypeChange = () => {
  filter_fields.value.stage = null
  filter_fields.value.class_track = null
  filter_fields.value.subject = null
  filter_fields.value.college = null
  filter_fields.value.department = null
  filter_fields.value.specialization = null
  filter_fields.value.semester_subject = null
}

const onStageChange = () => {
  filter_fields.value.class_track = null
}

const onCollegeChange = () => {
  filter_fields.value.department = null
}

const applyFilters = async () => {
  loading.value = true
  try {
    const params = {}
    if (filter_fields.value.institution_type && filter_fields.value.institution_type !== 'all') {
      params.institution_type = filter_fields.value.institution_type
    }
    if (filter_fields.value.stage) params.stage = filter_fields.value.stage
    if (filter_fields.value.class_track) params.class_track = filter_fields.value.class_track
    if (filter_fields.value.subject) params.subject = filter_fields.value.subject
    if (filter_fields.value.college) params.college = filter_fields.value.college
    if (filter_fields.value.department) params.department = filter_fields.value.department
    if (filter_fields.value.specialization) params.specialization = filter_fields.value.specialization
    if (filter_fields.value.semester_subject) params.semester_subject = filter_fields.value.semester_subject
    if (filter_fields.value.status) params.status = filter_fields.value.status
    if (filter_fields.value.search) params.search = filter_fields.value.search

    const res = await reportsService.getCurriculumReport(params)
    lessonsList.value = res.results || (Array.isArray(res) ? res : [])
  } catch (err) {
    console.error('Error loading curriculum report data:', err)
  } finally {
    loading.value = false
  }
}

const resetFilters = async () => {
  filter_fields.value = {
    institution_type: 'all',
    stage: null,
    class_track: null,
    subject: null,
    college: null,
    department: null,
    specialization: null,
    semester_subject: null,
    status: 'all',
    search: '',
  }
  await applyFilters()
}

// Filtered Lessons
const filteredLessons = computed(() => {
  return lessonsList.value
})

// Status Options
const statusOptions = [
  { text: 'الكل', value: 'all' },
  { text: 'نشط', value: 'active' },
  { text: 'محذوف', value: 'inactive' },
]

// Table Headers (Dynamic by institution type)
const headers = computed(() => [
  { title: 'النوع', key: 'institutionType', sortable: true, width: '100px' },
  { title: 'الدرس والوحدة', key: 'name', sortable: true },
  { title: filter_fields.value.institution_type === 'university' ? 'المقرر' : 'المادة', key: 'subject', sortable: true },
  { title: filter_fields.value.institution_type === 'university' ? 'الكلية والتخصص' : 'الصف والقسم', key: 'levelInfo', sortable: false },
  { title: 'الحالة', key: 'status', sortable: true },
  { title: 'الأسئلة المرتبطة', key: 'questionsCount', sortable: true },
  { title: 'سجل التعديلات', key: 'actions', sortable: false },
])

// Open History Dialog
const openHistory = async (lesson) => {
  selectedLesson.value = lesson
  historyDialog.value = true
  historyLoading.value = true

  try {
    const res = await academicService.getAuditLogs({
      entity_type: 'lesson',
      entity_id: lesson.id,
      ordering: '-timestamp'
    })

    const rawLogs = Array.isArray(res) ? res : (res?.results || [])
    lessonHistory.value = rawLogs.map(entry => {
      let actionText = 'تعديل بيانات'
      let color = 'primary'
      let icon = 'mdi-pencil'

      if (entry.action === 'CREATE' || entry.action === 'insert') {
        actionText = 'إنشاء الدرس'
        color = 'success'
        icon = 'mdi-plus-circle'
      } else if (entry.action === 'DELETE' || entry.action === 'deactivate') {
        actionText = 'تعطيل / حذف'
        color = 'error'
        icon = 'mdi-delete'
      }

      const date = new Date(entry.timestamp || Date.now())
      const dateString = date.toLocaleDateString('ar-EG', { year: 'numeric', month: 'short', day: 'numeric' })

      return {
        ...entry,
        actionText,
        color,
        icon,
        dateString,
        actor_name: entry.actor_name || 'مدير النظام'
      }
    })
  } catch (err) {
    console.error('Failed to load history:', err)
  } finally {
    historyLoading.value = false
  }
}
const viewHistory = openHistory

// Backend Data Fetching
onMounted(async () => {
  await applyFilters()
})
</script>

<style scoped>
.qb-curriculum-report-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.glass-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
</style>
