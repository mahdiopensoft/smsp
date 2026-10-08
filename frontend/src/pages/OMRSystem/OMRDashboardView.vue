<template>
  <div class="qb-omr-dashboard-v4">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-view-dashboard-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">لوحة تحكم القراءة والتصحيح</h1>
          <p class="text-caption text-medium-emphasis mb-0">نظرة عامة شمولية على حالة المعالجة الضوئية والأوراق المرفوعة ونسب الثقة</p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <custom-btn
          type="add"
          :click="() => $router.push('/omr/scanner')"
          label="بدء مسح ضوئي جديد"
          class="font-weight-bold"
        />
        <custom-btn
          type="imports"
          :click="() => $router.push('/omr/templates')"
          label="مصمم القوالب"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
        <custom-btn
          type="restore"
          :click="() => $router.push('/omr/submissions')"
          label="سجل الأوراق"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
        <custom-btn
          type="show"
          :click="() => $router.push('/omr/gradebook')"
          label="سجل الدرجات والكنترول"
          color="primary"
          variant="tonal"
          class="font-weight-bold"
        />
      </div>
    </div>

    <!-- Stat Summary Cards Grid (4 Calm Institutional Cards) -->
    <v-row class="mb-6" dense>
      <!-- Total Exams -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">إجمالي الاختبارات</span>
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-file-document-multiple-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-primary">{{ stats.total_exams }}</div>
          <div class="text-caption text-medium-emphasis mt-1">اختبارات OMR معتمدة ومربوطة</div>
        </v-card>
      </v-col>

      <!-- Total Submissions -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">أوراق مرفوعة</span>
            <v-avatar color="info" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-inbox-arrow-down-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-info">{{ stats.total_submissions }}</div>
          <div class="text-caption text-medium-emphasis mt-1">إجمالي الأوراق المعالجة بالماسح</div>
        </v-card>
      </v-col>

      <!-- Completed -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">مكتملة بنجاح</span>
            <v-avatar color="success" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-check-decagram-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-success">{{ stats.completed }}</div>
          <div class="text-caption text-medium-emphasis mt-1">تم تصحيحها وحساب درجاتها</div>
        </v-card>
      </v-col>

      <!-- Needs Review -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">بانتظار المراجعة</span>
            <v-avatar color="warning" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-clock-alert-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-warning">{{ stats.needs_review }}</div>
          <div class="text-caption text-medium-emphasis mt-1">تتطلب تدقيق بشري بالعين المجردة</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- OMR Workflow Banner Card -->
    <div
      class="main-card pa-5 rounded-2xl mb-6 border-subtle hover-lift cursor-pointer"
      @click="$router.push('/omr/scanner-lab')"
    >
      <div class="d-flex align-center justify-space-between flex-wrap gap-4">
        <div class="d-flex align-center gap-4">
          <v-avatar size="50" color="primary" variant="tonal" class="rounded-xl">
            <v-icon size="26">mdi-scanner-scanner</v-icon>
          </v-avatar>
          <div>
            <h3 class="text-subtitle-1 font-weight-black mb-1">مسار التصحيح الضوئي الفوري (OMR Workflow)</h3>
            <p class="text-body-2 text-medium-emphasis mb-0">تصدير أوراق الإجابة · رفع حزم الأوراق الممسوحة · معالجة دقيقة بالذكاء الاصطناعي مع قياس الثقة</p>
          </div>
        </div>
        <custom-btn type="add" label="الانتقال إلى سير العمل" color="primary" variant="tonal" class="font-weight-bold" icon="mdi-arrow-left" />
      </div>
    </div>

    <!-- Unified Filter Fields -->
    <filter-fields label="خيارات التصفية والبحث في الأوراق المعالجة" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Search Query Input -->
        <v-col cols="12" sm="6" md="5">
          <v-text-field
            v-model="searchQuery"
            label="اسم الطالب أو الاختبار"
            placeholder="بحث باسم الطالب أو الاختبار..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Status Filter -->
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="selectedStatus"
            :items="statusOptions"
            item-title="label"
            item-value="value"
            label="حالة التصحيح"
            prepend-inner-icon="mdi-check-decagram-outline"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Actions -->
        <v-col cols="12" sm="12" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6"
          />
          <custom-btn
            type="show"
            label="تحديث"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="fetchDashboardData"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Recent Processed Submissions Main Table -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <div class="d-flex align-center justify-space-between pa-5 border-b">
        <div>
          <h3 class="text-h6 font-weight-black mb-1">آخر الأوراق المعالجة</h3>
          <p class="text-caption text-medium-emphasis mb-0">قائمة الأوراق التي تم مسحها وتصحيحها مؤخراً عبر المحرك</p>
        </div>
        <custom-btn
          type="add"
          label="عرض جميع الأوراق"
          variant="tonal"
          size="small"
          class="font-weight-bold"
          :click="() => $router.push('/omr/submissions')"
        />
      </div>

      <custom-data-table
        v-bind="{
          items: tableItems,
          headers,
          loading,
        }"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Student Name -->
          <template v-if="key === 'student_name'">
            <div class="d-flex align-center gap-3 py-1">
              <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
                <v-icon size="20">mdi-account-outline</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-bold text-body-2 text-on-surface">{{ item.student_name || 'غير محدد' }}</div>
                <div class="text-caption text-medium-emphasis">رقم الجلوس: {{ item.student_seat_number || item.seat_number || '—' }}</div>
              </div>
            </div>
          </template>

          <!-- Exam Name -->
          <template v-else-if="key === 'exam_name'">
            <div class="font-weight-bold text-body-2">{{ item.exam_name || '—' }}</div>
            <div class="text-caption text-medium-emphasis">نموذج {{ item.version_code || item.model_code || 'A' }}</div>
          </template>

          <!-- Status -->
          <template v-else-if="key === 'status'">
            <v-chip
              size="small"
              :color="statusSeverity(item.status)"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              {{ statusLabel(item.status) }}
            </v-chip>
          </template>

          <!-- Total Score -->
          <template v-else-if="key === 'total_score'">
            <span class="font-weight-black text-body-1 text-primary">{{ item.total_score ?? '—' }}</span>
          </template>

          <!-- Confidence Indicator -->
          <template v-else-if="key === 'confidence'">
            <div v-if="item.overall_confidence != null" class="d-flex align-center justify-center gap-2">
              <v-progress-linear
                :model-value="Math.round(item.overall_confidence * 100)"
                :color="getConfidenceColor(item.overall_confidence)"
                height="6"
                rounded
                style="width: 80px;"
              />
              <span class="text-caption font-mono font-weight-bold">{{ Math.round(item.overall_confidence * 100) }}%</span>
            </div>
            <span v-else class="text-caption text-medium-emphasis">—</span>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                type="show"
                is-icon
                label="عرض وتدقيق الورقة"
                :click="() => $router.push(`/omr/submissions?id=${item.id}`)"
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
import { submissionsAPI, examsAPI } from '../../services/omr/endpoints.js'

const loading = ref(false)
const searchQuery = ref('')
const selectedStatus = ref('all')

const statusOptions = [
  { label: 'كافة الحالات', value: 'all' },
  { label: 'مكتمل بنجاح', value: 'completed' },
  { label: 'بانتظار المراجعة', value: 'needs_review' },
  { label: 'فشل المعالجة', value: 'failed' },
  { label: 'قيد المعالجة', value: 'processing' },
]

const stats = ref({
  total_exams: 0,
  total_submissions: 0,
  completed: 0,
  needs_review: 0,
  failed: 0,
})

const recentSubmissions = ref([])

const headers = computed(() => [
  { title: "اسم الطالب", key: "student_name", sortable: true },
  { title: "الاختبار والنموذج", key: "exam_name", sortable: true },
  { title: "حالة التصحيح", key: "status", sortable: true, align: "center", width: "140px" },
  { title: "الدرجة", key: "total_score", sortable: true, align: "center", width: "110px" },
  { title: "مؤشر الثقة", key: "confidence", sortable: true, align: "center", width: "150px" },
])

const filteredSubmissions = computed(() => {
  let list = recentSubmissions.value || []
  if (selectedStatus.value && selectedStatus.value !== 'all') {
    list = list.filter(s => s.status === selectedStatus.value)
  }
  if (searchQuery.value && searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter(s =>
      (s.student_name && s.student_name.toLowerCase().includes(q)) ||
      (s.exam_name && s.exam_name.toLowerCase().includes(q)) ||
      (s.student_seat_number && String(s.student_seat_number).includes(q))
    )
  }
  return list
})

const tableItems = computed(() => ({
  results: filteredSubmissions.value,
  count: filteredSubmissions.value.length,
  pagination: {
    count: filteredSubmissions.value.length,
    total: filteredSubmissions.value.length,
  }
}))

const resetFilters = () => {
  searchQuery.value = ''
  selectedStatus.value = 'all'
}

function statusSeverity(status) {
  const map = {
    completed: 'success',
    needs_review: 'warning',
    failed: 'error',
    pending: 'info',
    processing: 'info',
    reviewed: 'primary',
  }
  return map[status] || 'info'
}

function statusLabel(status) {
  const map = {
    completed: 'مكتمل',
    needs_review: 'مراجعة',
    failed: 'فشل',
    pending: 'انتظار',
    processing: 'معالجة',
    reviewed: 'مراجعة نهائية',
  }
  return map[status] || status
}

function getConfidenceColor(conf) {
  if (conf >= 0.8) return 'success'
  if (conf >= 0.5) return 'warning'
  return 'error'
}

const fetchDashboardData = async () => {
  loading.value = true
  try {
    const [examsRes, subsRes] = await Promise.all([
      examsAPI.list(),
      submissionsAPI.list({ ordering: '-created_at', page_size: 15 }),
    ])

    stats.value.total_exams = examsRes.data.count || examsRes.data.results?.length || 0

    const subs = subsRes.data.results || []
    recentSubmissions.value = subs
    stats.value.total_submissions = subsRes.data.count || subs.length
    stats.value.completed = subs.filter(s => s.status === 'completed').length
    stats.value.needs_review = subs.filter(s => s.status === 'needs_review').length
    stats.value.failed = subs.filter(s => s.status === 'failed').length
  } catch (err) {
    console.error('Dashboard load error:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.qb-omr-dashboard-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Stat Cards ===== */
.stat-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

/* ===== Main Cards & Tables ===== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12);
  background: rgb(var(--v-theme-background));
}

.hover-lift {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05) !important;
}

.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}

.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.font-mono {
  font-family: monospace, monospace;
}
</style>
