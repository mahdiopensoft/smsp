<template>
  <div class="qb-bank-status-report-v4">
    <!-- Hero Banner Header (Screen HAS action buttons) -->
    <div class="hero-banner rounded-xl mb-8 pa-6 pa-md-8 position-relative overflow-hidden">
      <!-- Glow Backdrops -->
      <div class="glow-circle primary-glow"></div>
      <div class="glow-circle secondary-glow"></div>

      <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 position-relative z-index-1">
        <div class="d-flex align-center">
          <v-avatar size="54" color="white" class="bg-white/10 text-white me-4 rounded-xl backdrop-blur">
            <v-icon size="28">mdi-database-check</v-icon>
          </v-avatar>
          <div>
            <div class="greeting-badge mb-2">
              <v-icon size="14" color="white" class="me-1">mdi-sparkles</v-icon>
              <span>التقارير الإحصائية والتحليلية</span>
            </div>
            <h1 class="text-h4 font-weight-black text-white mb-1">تقرير حالة بنك الأسئلة</h1>
            <p class="text-body-2 text-white/80 mb-0">إحصائيات تحليلية شاملة عن توزيع الأسئلة في البنك والمستويات المعرفية.</p>
          </div>
        </div>

        <div class="d-flex align-center gap-3">
          <custom-btn
            type="add"
            label="تصدير PDF"
            icon="mdi-download"
            color="white"
            variant="outlined"
            class="font-weight-bold"
          />

          <custom-btn
            type="add"
            label="تحديث البيانات"
            icon="mdi-refresh"
            color="white"
            class="btn-glow-primary px-6 font-weight-bold text-indigo-900"
            :click="refreshData"
          />
        </div>
      </div>
    </div>

    <!-- Filters -->
    <filter-fields :label="'تصفية وتحليل بيانات بنك الأسئلة (مدرسي / جامعي)'" class="mb-4">
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

        <v-col cols="auto" class="d-flex align-center">
          <custom-btn type="filter" :loading="loading" :click="refreshData" />
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

    <!-- Loading State -->
    <div v-if="loading" class="d-flex justify-center align-center py-12">
      <v-progress-circular indeterminate color="primary" size="64" />
    </div>

    <template v-else>
      <!-- Summary Cards (Stat Glass Cards) -->
      <v-row class="mb-6">
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">إجمالي الأسئلة</span>
              <div class="icon-square bg-indigo-gradient">
                <v-icon color="white" size="20">mdi-help-circle-outline</v-icon>
              </div>
            </div>
            <div class="text-h3 font-weight-black mb-2">{{ stats.totalQuestions }}</div>
            <div class="d-flex align-center justify-space-between text-caption text-medium-emphasis border-t pt-2 mt-2">
              <span>أسئلة متوفرة بالبنك</span>
              <v-icon size="16">mdi-arrow-left</v-icon>
            </div>
          </div>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">أسئلة معتمدة</span>
              <div class="icon-square bg-emerald-gradient">
                <v-icon color="white" size="20">mdi-check-decagram-outline</v-icon>
              </div>
            </div>
            <div class="text-h3 font-weight-black mb-2">{{ stats.approved }}</div>
            <div class="d-flex align-center justify-space-between text-caption text-medium-emphasis border-t pt-2 mt-2">
              <span>جاهزة للاستخدام</span>
              <v-icon size="16">mdi-arrow-left</v-icon>
            </div>
          </div>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">قيد المراجعة</span>
              <div class="icon-square bg-amber-gradient">
                <v-icon color="white" size="20">mdi-clock-outline</v-icon>
              </div>
            </div>
            <div class="text-h3 font-weight-black mb-2">{{ stats.pending }}</div>
            <div class="d-flex align-center justify-space-between text-caption text-medium-emphasis border-t pt-2 mt-2">
              <span>بانتظار الاعتماد</span>
              <v-icon size="16">mdi-arrow-left</v-icon>
            </div>
          </div>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">أسئلة مرفوضة</span>
              <div class="icon-square bg-rose-gradient">
                <v-icon color="white" size="20">mdi-close-circle-outline</v-icon>
              </div>
            </div>
            <div class="text-h3 font-weight-black mb-2">{{ stats.rejected }}</div>
            <div class="d-flex align-center justify-space-between text-caption text-medium-emphasis border-t pt-2 mt-2">
              <span>تحتاج لتعديل</span>
              <v-icon size="16">mdi-arrow-left</v-icon>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Second Row Summary -->
      <v-row class="mb-6">
        <v-col cols="6" md="4">
          <v-card class="glass-card pa-4 text-center">
            <v-icon size="32" color="info" class="mb-2">mdi-book</v-icon>
            <div class="text-h4 font-weight-bold text-info">{{ stats.subjects }}</div>
            <div class="text-caption text-medium-emphasis">
              {{ filter_fields.institution_type === 'university' ? 'المقررات الجامعية' : (filter_fields.institution_type === 'school' ? 'المواد الدراسية' : 'المواد والمقررات') }}
            </div>
          </v-card>
        </v-col>
        <v-col cols="6" md="4">
          <v-card class="glass-card pa-4 text-center">
            <v-icon size="32" color="secondary" class="mb-2">mdi-folder-multiple</v-icon>
            <div class="text-h4 font-weight-bold text-secondary">{{ stats.units }}</div>
            <div class="text-caption text-medium-emphasis">الوحدات الدراسية</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="glass-card pa-4 text-center">
            <v-icon size="32" color="purple" class="mb-2">mdi-file-document</v-icon>
            <div class="text-h4 font-weight-bold" style="color: rgb(var(--v-theme-purple, 156, 39, 176));">{{ stats.lessons }}</div>
            <div class="text-caption text-medium-emphasis">الدروس</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Alerts for Missing Content -->
      <v-alert 
        v-for="alert in alerts" 
        :key="alert.id"
        :type="alert.type" 
        variant="tonal" 
        class="mb-4"
        closable
      >
        <template v-slot:title>{{ alert.title }}</template>
        {{ alert.message }}
      </v-alert>

      <v-row>
        <!-- Questions by Subject -->
        <v-col cols="12" md="6">
          <CustomCard class="glass-card pa-6">
            <h3 class="text-h6 font-weight-bold mb-4">
              <v-icon start color="primary">mdi-chart-pie</v-icon>
              {{ filter_fields.institution_type === 'university' ? 'توزيع الأسئلة حسب المقرر' : 'توزيع الأسئلة حسب المادة' }}
            </h3>
            <div v-if="subjectStats.length === 0" class="text-center text-medium-emphasis pa-8">
              <v-icon size="48" class="mb-2">mdi-database-off</v-icon>
              <div>لا توجد بيانات</div>
            </div>
            <div class="chart-container" v-else>
              <div v-for="subject in subjectStats" :key="subject.name" class="mb-4">
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-body-2">{{ subject.name }}</span>
                  <span class="text-body-2 font-weight-bold">{{ subject.count }} سؤال</span>
                </div>
                <v-progress-linear
                  :model-value="stats.totalQuestions > 0 ? (subject.count / stats.totalQuestions) * 100 : 0"
                  :color="subject.color"
                  height="12"
                  rounded
                />
              </div>
            </div>
          </CustomCard>
        </v-col>

        <!-- Questions by Difficulty -->
        <v-col cols="12" md="6">
          <CustomCard class="glass-card pa-6">
            <h3 class="text-h6 font-weight-bold mb-4">
              <v-icon start color="warning">mdi-speedometer</v-icon>
              توزيع الأسئلة حسب الصعوبة
            </h3>
            <div v-if="stats.totalQuestions === 0" class="text-center text-medium-emphasis pa-8">
              <v-icon size="48" class="mb-2">mdi-database-off</v-icon>
              <div>لا توجد بيانات</div>
            </div>
            <div class="d-flex justify-center gap-8" v-else>
              <div v-for="diff in difficultyStats" :key="diff.level" class="text-center">
                <v-progress-circular
                  :model-value="stats.totalQuestions > 0 ? (diff.count / stats.totalQuestions) * 100 : 0"
                  :color="diff.color"
                  :size="100"
                  :width="10"
                >
                  <div>
                    <div class="text-h5 font-weight-bold">{{ diff.count }}</div>
                    <div class="text-caption">{{ diff.percentage }}%</div>
                  </div>
                </v-progress-circular>
                <div class="text-body-2 mt-2">{{ diff.label }}</div>
              </div>
            </div>
          </CustomCard>
        </v-col>

        <!-- Questions by Bloom Level -->
        <v-col cols="12" md="6">
          <CustomCard class="glass-card pa-6">
            <h3 class="text-h6 font-weight-bold mb-4">
              <v-icon start color="secondary">mdi-brain</v-icon>
              توزيع الأسئلة حسب مستويات بلوم
            </h3>
            <div v-if="stats.totalQuestions === 0" class="text-center text-medium-emphasis pa-8">
              <v-icon size="48" class="mb-2">mdi-database-off</v-icon>
              <div>لا توجد بيانات</div>
            </div>
            <div class="bloom-chart" v-else>
              <div v-for="bloom in bloomStats" :key="bloom.level" class="bloom-bar mb-3">
                <div class="d-flex align-center">
                  <span class="text-body-2 bloom-label">{{ bloom.name }}</span>
                  <v-progress-linear
                    :model-value="stats.totalQuestions > 0 ? (bloom.count / stats.totalQuestions) * 100 : 0"
                    :color="bloom.color"
                    height="24"
                    rounded
                    class="flex-grow-1 mx-3"
                  >
                    <template v-slot:default>
                      <span class="text-white text-caption">{{ bloom.count }}</span>
                    </template>
                  </v-progress-linear>
                  <span class="text-body-2 font-weight-bold" style="min-width: 50px;">{{ bloom.percentage }}%</span>
                </div>
              </div>
            </div>
          </CustomCard>
        </v-col>

        <!-- Questions by Type -->
        <v-col cols="12" md="6">
          <CustomCard class="glass-card pa-6">
            <h3 class="text-h6 font-weight-bold mb-4">
              <v-icon start color="teal">mdi-format-list-bulleted-type</v-icon>
              توزيع الأسئلة حسب النوع
            </h3>
            <div v-if="stats.totalQuestions === 0" class="text-center text-medium-emphasis pa-8">
              <v-icon size="48" class="mb-2">mdi-database-off</v-icon>
              <div>لا توجد بيانات</div>
            </div>
            <div class="d-flex justify-center" v-else>
              <div v-for="typeItem in questionTypeStats" :key="typeItem.type" class="mb-4 w-100 px-4">
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-body-2">{{ typeItem.label }}</span>
                  <span class="text-body-2 font-weight-bold">{{ typeItem.count }} ({{ typeItem.percentage }}%)</span>
                </div>
                <v-progress-linear
                  :model-value="stats.totalQuestions > 0 ? (typeItem.count / stats.totalQuestions) * 100 : 0"
                  :color="typeItem.color"
                  height="12"
                  rounded
                />
              </div>
            </div>
          </CustomCard>
        </v-col>

        <!-- Coverage by Unit -->
        <v-col cols="12">
          <CustomCard class="glass-card pa-6">
            <h3 class="text-h6 font-weight-bold mb-4">
              <v-icon start color="info">mdi-folder-multiple</v-icon>
              تغطية الوحدات الدراسية
            </h3>
            <custom-data-table
              ref="table"
              v-bind="{
                items: coverageData,
                headers: coverageHeaders,
              }"
              density="comfortable"
              class="bg-transparent"
              :items-per-page="10"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :customLoading="loading"
            >
              <!-- Institution Type Chip -->
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

              <template v-slot:item.questionCount="{ item }">
                <v-chip variant="tonal" size="small" color="primary">
                  {{ item.questionCount }}
                </v-chip>
              </template>
              <template v-slot:item.coverage="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.coverage"
                    :color="getCoverageColor(item.coverage)"
                    height="8"
                    rounded
                    style="width: 100px;"
                  />
                  <span class="text-caption">{{ item.coverage }}%</span>
                </div>
              </template>
              <template v-slot:item.status="{ item }">
                <v-chip 
                  :color="getCoverageColor(item.coverage)" 
                  variant="tonal" 
                  size="x-small"
                >
                  {{ item.coverage >= 80 ? 'جيد' : item.coverage >= 50 ? 'متوسط' : 'ضعيف' }}
                </v-chip>
              </template>
            </custom-data-table>
          </CustomCard>
        </v-col>
      </v-row>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(true)
let alertId = 1

// Filters State (Unified School / University)
const filter_fields = ref({
  institution_type: 'all',
  stage: null,
  class_track: null,
  subject: null,
  college: null,
  department: null,
  specialization: null,
  semester_subject: null,
})

const onInstitutionTypeChange = () => {
  filter_fields.value.stage = null
  filter_fields.value.class_track = null
  filter_fields.value.subject = null
  filter_fields.value.college = null
  filter_fields.value.department = null
  filter_fields.value.specialization = null
  filter_fields.value.semester_subject = null
  refreshData()
}

const onStageChange = () => {
  filter_fields.value.class_track = null
  filter_fields.value.subject = null
}

const onCollegeChange = () => {
  filter_fields.value.department = null
}

const overviewData = ref({
  stats: { totalQuestions: 0, approved: 0, pending: 0, rejected: 0, subjects: 0, units: 0, lessons: 0 },
  difficultyDistribution: [],
  bloomDistribution: [],
  typeDistribution: [],
  subjectProgress: []
})

const stats = computed(() => {
  const s = overviewData.value.stats || {}
  return {
    totalQuestions: s.totalQuestions || 0,
    approved: s.approved || 0,
    pending: s.inReview || s.pending || 0,
    rejected: s.rejected || 0,
    subjects: s.subjects || 0,
    units: s.units || 0,
    lessons: s.lessons || 0,
  }
})

const subjectStats = computed(() => {
  return overviewData.value.subjectProgress?.map((s, idx) => ({
    name: s.subjectName,
    count: s.available,
    color: ['blue', 'purple', 'green', 'teal', 'orange', 'red', 'indigo', 'cyan'][idx % 8]
  })) || []
})

const difficultyStats = computed(() => {
  return overviewData.value.difficultyDistribution?.map(d => ({
    level: d.key,
    label: d.level,
    count: d.count,
    color: d.color === 'emerald' ? 'success' : (d.color === 'amber' ? 'warning' : 'error'),
    percentage: d.pct || 0
  })) || []
})

const bloomStats = computed(() => {
  return overviewData.value.bloomDistribution?.map((b, idx) => ({
    level: idx + 1,
    name: b.label,
    count: b.count,
    color: b.color || 'primary',
    percentage: b.percentage || 0
  })) || []
})

const questionTypeStats = computed(() => {
  return overviewData.value.typeDistribution?.map(t => ({
    type: t.type,
    label: t.type,
    count: t.count,
    color: t.color || 'primary',
    percentage: t.percentage || 0
  })) || []
})

const coverageHeaders = computed(() => [
  { title: 'النوع', key: 'institutionType', width: '100px' },
  { title: filter_fields.value.institution_type === 'university' ? 'المقرر والتخصص' : 'المادة', key: 'subject' },
  { title: 'الوحدة', key: 'unit' },
  { title: 'عدد الأسئلة', key: 'questionCount' },
  { title: 'التغطية', key: 'coverage' },
  { title: 'الحالة', key: 'status' },
])

const coverageData = computed(() => {
  return overviewData.value.subjectProgress?.map(s => ({
    institutionType: s.institutionType || 'school',
    subject: s.subjectName,
    unit: 'جميع الوحدات',
    questionCount: s.available,
    coverage: s.coverage,
    status: s.coverage >= 80 ? 'good' : (s.coverage >= 50 ? 'medium' : 'low')
  })) || []
})

const alerts = computed(() => {
  const result = []

  // Check for rejected questions
  if (stats.value.rejected > 0) {
    result.push({
      id: alertId++,
      type: 'error',
      title: 'أسئلة مرفوضة',
      message: `يوجد ${stats.value.rejected} سؤال مرفوض يحتاج إلى مراجعة وإعادة تعديل.`,
    })
  }

  return result
})

// Methods
const getCoverageColor = (coverage) => {
  if (coverage >= 80) return 'success'
  if (coverage >= 50) return 'warning'
  return 'error'
}

const resetFilters = () => {
  filter_fields.value = {
    institution_type: 'all',
    stage: null,
    class_track: null,
    subject: null,
    college: null,
    department: null,
    specialization: null,
    semester_subject: null,
  }
  refreshData()
}

const refreshData = async () => {
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

    const res = await reportsService.getBankStatusOverview(params)
    if (res) {
      overviewData.value = res
    }
  } catch (err) {
    console.error('Error fetching bank status overview:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}

.gap-8 {
  gap: 32px;
}

.bloom-label {
  min-width: 60px;
}

:deep(.v-data-table) {
  background: transparent !important;
}

/* ===== Theme & Banner Enhancements ===== */
.qb-bank-status-report-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.hero-banner {
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
  box-shadow: 0 10px 30px rgba(49, 46, 129, 0.25);
}

.glow-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  pointer-events: none;
}

.primary-glow {
  width: 250px;
  height: 250px;
  background: rgba(99, 102, 241, 0.35);
  top: -50px;
  right: -50px;
}

.secondary-glow {
  width: 200px;
  height: 200px;
  background: rgba(168, 85, 247, 0.25);
  bottom: -40px;
  left: 10%;
}

.greeting-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 700;
}

.btn-glow-primary {
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.4);
  transition: all 0.3s ease;
}

.btn-glow-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(255, 255, 255, 0.6);
}

/* ===== Stat Cards ===== */
.stat-glass-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.icon-square {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-indigo-gradient { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); }
.bg-emerald-gradient { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.bg-amber-gradient { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.bg-rose-gradient { background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%); }

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
