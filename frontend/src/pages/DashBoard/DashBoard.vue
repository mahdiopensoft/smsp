<template>
  <div class="dashboard-wrapper">
    <v-progress-linear v-if="loading" indeterminate color="indigo" height="4" class="mb-4 rounded-pill" />

    <!-- Stats Cards Row (Theme Compatible) -->
    <v-row class="mb-8">
      <v-col cols="12" sm="6" lg="3">
        <div class="stat-glass-card pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="stat-icon-wrapper bg-indigo-gradient">
              <v-icon size="26" color="white">mdi-file-document-multiple-outline</v-icon>
            </div>
            <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold px-3">
              <v-icon size="14" start>mdi-trending-up</v-icon>
              +12%
            </v-chip>
          </div>
          <div class="stat-value text-h3 font-weight-black text-indigo mb-1">
            {{ stats.totalQuestions }}
          </div>
          <div class="stat-label text-subtitle-2 font-weight-medium text-medium-emphasis">إجمالي الأسئلة في البنك</div>
          <div class="stat-footer mt-3 pt-3 border-t border-slate-100 d-flex align-center justify-space-between text-caption text-medium-emphasis">
            <span>تاريخ التحديث: اليوم</span>
            <v-icon size="14">mdi-arrow-left</v-icon>
          </div>
        </div>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <div class="stat-glass-card pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="stat-icon-wrapper bg-emerald-gradient">
              <v-icon size="26" color="white">mdi-check-decagram</v-icon>
            </div>
            <v-chip size="small" color="emerald" variant="tonal" class="font-weight-bold px-3">
              <v-icon size="14" start>mdi-trending-up</v-icon>
              +8%
            </v-chip>
          </div>
          <div class="stat-value text-h3 font-weight-black text-emerald mb-1">
            {{ stats.approvedQuestions }}
          </div>
          <div class="stat-label text-subtitle-2 font-weight-medium text-medium-emphasis">أسئلة معتمدة وجاهزة</div>
          <div class="stat-footer mt-3 pt-3 border-t border-slate-100 d-flex align-center justify-space-between text-caption text-medium-emphasis">
            <span>نسبة الاعتماد: {{ Math.round((stats.approvedQuestions / (stats.totalQuestions || 1)) * 100) }}%</span>
            <v-icon size="14">mdi-arrow-left</v-icon>
          </div>
        </div>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <div class="stat-glass-card pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="stat-icon-wrapper bg-amber-gradient">
              <v-icon size="26" color="white">mdi-clock-fast</v-icon>
            </div>
            <v-chip size="small" color="amber" variant="tonal" class="font-weight-bold px-3">
              <v-icon size="14" start>mdi-clock-outline</v-icon>
              مطلوبة
            </v-chip>
          </div>
          <div class="stat-value text-h3 font-weight-black text-amber mb-1">
            {{ stats.pendingReview }}
          </div>
          <div class="stat-label text-subtitle-2 font-weight-medium text-medium-emphasis">أسئلة بانتظار المراجعة</div>
          <div class="stat-footer mt-3 pt-3 border-t border-slate-100 d-flex align-center justify-space-between text-caption text-medium-emphasis">
            <span>تحتاج قرار المراجعين</span>
            <v-icon size="14">mdi-arrow-left</v-icon>
          </div>
        </div>
      </v-col>

      <v-col cols="12" sm="6" lg="3">
        <div class="stat-glass-card pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="stat-icon-wrapper bg-sky-gradient">
              <v-icon size="26" color="white">mdi-file-percent</v-icon>
            </div>
            <v-chip size="small" color="sky" variant="tonal" class="font-weight-bold px-3">
              <v-icon size="14" start>mdi-trending-up</v-icon>
              +15%
            </v-chip>
          </div>
          <div class="stat-value text-h3 font-weight-black text-sky mb-1">
            {{ stats.generatedExams }}
          </div>
          <div class="stat-label text-subtitle-2 font-weight-medium text-medium-emphasis">نماذج اختبارات مولدة</div>
          <div class="stat-footer mt-3 pt-3 border-t border-slate-100 d-flex align-center justify-space-between text-caption text-medium-emphasis">
            <span>جاهزة للطباعة والتصدير</span>
            <v-icon size="14">mdi-arrow-left</v-icon>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Charts & Analytics Row (Theme Compatible) -->
    <v-row class="mb-8">
      <!-- Main Bar Chart: Questions by Subject -->
      <v-col cols="12" lg="8">
        <div class="main-card pa-6 rounded-2xl h-100 d-flex flex-column">
          <div class="d-flex align-center justify-space-between mb-6">
            <div>
              <div class="d-flex align-center gap-2 mb-1">
                <v-icon color="indigo">mdi-chart-bar-stacked</v-icon>
                <h3 class="text-h6 font-weight-bold">توزيع الأسئلة حسب المادة</h3>
              </div>
              <p class="text-caption text-medium-emphasis mb-0">نظرة عامة على حجم المحتوى لكل مادة دراسية</p>
            </div>
            <div class="segmented-control">
              <button :class="{ active: chartPeriod === 'week' }" @click="chartPeriod = 'week'">أسبوع</button>
              <button :class="{ active: chartPeriod === 'month' }" @click="chartPeriod = 'month'">شهر</button>
              <button :class="{ active: chartPeriod === 'year' }" @click="chartPeriod = 'year'">سنة</button>
            </div>
          </div>

          <!-- Bar Chart Area -->
          <div class="flex-grow-1 d-flex align-end justify-center pt-8 pb-2 px-2">
            <div class="modern-bar-chart">
              <div
                v-for="(item, index) in questionsBySubject"
                :key="item.name"
                class="modern-bar-group"
              >
                <div class="bar-badge font-weight-bold">{{ item.count }}</div>
                <div class="bar-track">
                  <div
                    class="bar-fill"
                    :style="{
                      height: getBarHeight(item.count) + '%',
                      background: item.gradient,
                      animationDelay: (index * 0.08) + 's'
                    }"
                  >
                    <div class="bar-glow"></div>
                  </div>
                </div>
                <div class="bar-title text-caption font-weight-medium text-medium-emphasis" :title="item.name">
                  {{ item.name }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-col>

      <!-- Question Types Donut Chart -->
      <v-col cols="12" lg="4">
        <div class="main-card pa-6 rounded-2xl h-100 d-flex flex-column justify-space-between">
          <div>
            <div class="d-flex align-center gap-2 mb-1">
              <v-icon color="emerald">mdi-chart-donut</v-icon>
              <h3 class="text-h6 font-weight-bold">توزيع أنواع الأسئلة</h3>
            </div>
            <p class="text-caption text-medium-emphasis mb-6">النسبة المئوية حسب نمط السؤال</p>

            <!-- Donut SVG Area -->
            <div class="d-flex justify-center my-4">
              <div class="donut-chart-box">
                <svg viewBox="0 0 140 140" class="donut-svg">
                  <circle
                    v-for="(seg, i) in donutSegments"
                    :key="i"
                    cx="70" cy="70" r="50"
                    fill="none"
                    :stroke="seg.color"
                    stroke-width="16"
                    :stroke-dasharray="seg.dashArray"
                    :stroke-dashoffset="seg.dashOffset"
                    class="donut-ring-segment"
                    :style="{ animationDelay: (i * 0.15) + 's' }"
                  />
                </svg>
                <div class="donut-center-content">
                  <div class="donut-number text-h4 font-weight-black">{{ stats.totalQuestions }}</div>
                  <div class="donut-subtitle text-caption text-medium-emphasis font-weight-medium">إجمالي الأسئلة</div>
                </div>
              </div>
            </div>

            <!-- Legend List -->
            <div class="legend-list mt-6 d-flex flex-column gap-3">
              <div
                v-for="type in questionTypes"
                :key="type.name"
                class="legend-item pa-2 rounded-lg d-flex align-center justify-space-between"
              >
                <div class="d-flex align-center gap-2">
                  <span class="legend-dot" :style="{ background: type.color }"></span>
                  <span class="text-body-2 font-weight-medium">{{ type.name }}</span>
                </div>
                <div class="d-flex align-center gap-2">
                  <span class="text-body-2 font-weight-black">{{ type.count }}</span>
                  <v-chip size="x-small" variant="tonal" class="font-weight-bold" :color="type.chipColor">
                    {{ type.percentage }}%
                  </v-chip>
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Difficulty & Bloom Level Row -->
    <v-row class="mb-8">
      <!-- Difficulty Distribution Card -->
      <v-col cols="12" md="6">
        <div class="main-card pa-6 rounded-2xl h-100">
          <div class="d-flex align-center justify-space-between mb-6">
            <div class="d-flex align-center gap-2">
              <v-icon color="amber-darken-2">mdi-gauge</v-icon>
              <h3 class="text-h6 font-weight-bold">توزيع مستوى الصعوبة</h3>
            </div>
            <v-chip size="small" variant="tonal" color="secondary" class="font-weight-medium">3 مستويات</v-chip>
          </div>

          <div class="d-flex flex-column gap-5">
            <div v-for="diff in difficultyDistribution" :key="diff.name" class="gauge-row">
              <div class="d-flex align-center justify-space-between mb-2">
                <div class="d-flex align-center gap-2">
                  <v-icon size="18" :color="diff.color">
                    {{ diff.key === 1 ? 'mdi-emoticon-happy-outline' : diff.key === 2 ? 'mdi-emoticon-neutral-outline' : 'mdi-emoticon-sad-outline' }}
                  </v-icon>
                  <span class="text-body-2 font-weight-bold">{{ diff.name }}</span>
                </div>
                <span class="text-caption font-weight-black">{{ diff.count }} سؤال ({{ diff.percentage }}%)</span>
              </div>
              <v-progress-linear
                :model-value="diff.percentage"
                :color="diff.color"
                height="12"
                rounded="pill"
                class="modern-progress"
              />
            </div>
          </div>
        </div>
      </v-col>

      <!-- Bloom Taxonomy Distribution Card -->
      <v-col cols="12" md="6">
        <div class="main-card pa-6 rounded-2xl h-100">
          <div class="d-flex align-center justify-space-between mb-6">
            <div class="d-flex align-center gap-2">
              <v-icon color="purple">mdi-brain</v-icon>
              <h3 class="text-h6 font-weight-bold">توزيع مستويات بلوم المعرفية</h3>
            </div>
            <v-chip size="small" color="purple" variant="tonal" class="font-weight-medium">هرم بلوم</v-chip>
          </div>

          <div class="bloom-grid">
            <div
              v-for="bloom in bloomDistribution"
              :key="bloom.name"
              class="bloom-card pa-3 rounded-xl d-flex align-center justify-space-between"
            >
              <div class="d-flex align-center gap-3">
                <div class="bloom-icon-box" :style="{ background: bloom.color + '20', color: bloom.color }">
                  <v-icon size="18">{{ getBloomIcon(bloom.name) }}</v-icon>
                </div>
                <div>
                  <div class="text-body-2 font-weight-bold">{{ bloom.name }}</div>
                  <div class="text-caption text-medium-emphasis">{{ bloom.percentage }}% من الإجمالي</div>
                </div>
              </div>
              <div class="text-h6 font-weight-black" :style="{ color: bloom.color }">
                {{ bloom.count }}
              </div>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Quick Actions Panel -->
    <div class="mb-8">
      <h3 class="text-h6 font-weight-bold mb-4 d-flex align-center gap-2">
        <v-icon color="primary">mdi-lightning-bolt</v-icon>
        إجراءات سريعة وشائعة
      </h3>
      <v-row>
        <v-col cols="12" sm="6" md="3">
          <router-link to="/author/questions/new" class="action-card-link">
            <div class="action-card pa-5 rounded-2xl d-flex align-center gap-4">
              <div class="action-icon-circle bg-indigo-light">
                <v-icon size="24" color="indigo">mdi-plus</v-icon>
              </div>
              <div>
                <div class="text-subtitle-2 font-weight-bold">سؤال جديد</div>
                <div class="text-caption text-medium-emphasis">إضافة سؤال جديد للبنك</div>
              </div>
            </div>
          </router-link>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <router-link to="/generator/exams/create" class="action-card-link">
            <div class="action-card pa-5 rounded-2xl d-flex align-center gap-4">
              <div class="action-icon-circle bg-emerald-light">
                <v-icon size="24" color="emerald">mdi-file-document-plus</v-icon>
              </div>
              <div>
                <div class="text-subtitle-2 font-weight-bold">إنشاء اختبار</div>
                <div class="text-caption text-medium-emphasis">توليد اختبار أوتوماتيكي</div>
              </div>
            </div>
          </router-link>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <router-link to="/reviewer/review-queue" class="action-card-link">
            <div class="action-card pa-5 rounded-2xl d-flex align-center gap-4">
              <div class="action-icon-circle bg-amber-light">
                <v-icon size="24" color="amber-darken-2">mdi-clipboard-check-outline</v-icon>
              </div>
              <div class="flex-grow-1">
                <div class="d-flex align-center justify-space-between">
                  <div class="text-subtitle-2 font-weight-bold">مراجعة الأسئلة</div>
                  <v-chip size="x-small" color="amber-darken-2" class="font-weight-bold">
                    {{ stats.pendingReview }}
                  </v-chip>
                </div>
                <div class="text-caption text-medium-emphasis">مراجعة والاعتماد</div>
              </div>
            </div>
          </router-link>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <router-link to="/admin/users" class="action-card-link">
            <div class="action-card pa-5 rounded-2xl d-flex align-center gap-4">
              <div class="action-icon-circle bg-purple-light">
                <v-icon size="24" color="purple">mdi-account-group-outline</v-icon>
              </div>
              <div>
                <div class="text-subtitle-2 font-weight-bold">إدارة المستخديمن</div>
                <div class="text-caption text-medium-emphasis">إدارة الصلاحيات والأدوار</div>
              </div>
            </div>
          </router-link>
        </v-col>
      </v-row>
    </div>

    <!-- Recent Activity & Latest Content -->
    <v-row class="mb-8">
      <!-- Recent Questions List -->
      <v-col cols="12" lg="6">
        <div class="main-card rounded-2xl overflow-hidden h-100 d-flex flex-column">
          <div class="pa-5 border-b border-slate-100 d-flex align-center justify-space-between">
            <div class="d-flex align-center gap-2">
              <v-icon color="primary">mdi-history</v-icon>
              <h3 class="text-h6 font-weight-bold">آخر الأسئلة المضافة</h3>
            </div>
            <v-btn variant="text" color="primary" size="small" class="font-weight-bold" to="/author/questions">
              عرض الكل <v-icon end size="14">mdi-arrow-left</v-icon>
            </v-btn>
          </div>

          <div class="flex-grow-1 pa-3">
            <div v-if="recentQuestions.length === 0" class="text-center py-8 text-medium-emphasis">
              <v-icon size="40" class="mb-2">mdi-file-hidden</v-icon>
              <div>لا توجد أسئلة مضافة مؤخراً</div>
            </div>

            <div
              v-for="question in recentQuestions"
              :key="question.id"
              class="question-item-row pa-3 rounded-xl mb-2 d-flex align-center justify-space-between gap-3"
            >
              <div class="d-flex align-center gap-3 overflow-hidden">
                <v-avatar :color="getStatusColor(question.status)" variant="tonal" size="42" rounded="lg">
                  <v-icon size="20" :color="getStatusColor(question.status)">{{ getStatusIcon(question.status) }}</v-icon>
                </v-avatar>
                <div class="overflow-hidden">
                  <div class="text-body-2 font-weight-bold text-truncate" :title="question.title">
                    {{ question.title }}
                  </div>
                  <div class="text-caption text-medium-emphasis text-truncate">
                    {{ question.subject }} • {{ question.lesson }}
                  </div>
                </div>
              </div>
              <v-chip size="small" :color="getStatusColor(question.status)" variant="tonal" class="font-weight-bold px-3">
                {{ getStatusText(question.status) }}
              </v-chip>
            </div>
          </div>
        </div>
      </v-col>

      <!-- Audit Activity Log -->
      <v-col cols="12" lg="6">
        <div class="main-card rounded-2xl overflow-hidden h-100 d-flex flex-column">
          <div class="pa-5 border-b border-slate-100 d-flex align-center justify-space-between">
            <div class="d-flex align-center gap-2">
              <v-icon color="indigo">mdi-format-list-bulleted-type</v-icon>
              <h3 class="text-h6 font-weight-bold">آخر النشاطات في النظام</h3>
            </div>
            <v-btn variant="text" color="indigo" size="small" class="font-weight-bold" to="/admin/audit-logs">
              عرض سجل الأنشطة <v-icon end size="14">mdi-arrow-left</v-icon>
            </v-btn>
          </div>

          <div class="flex-grow-1 pa-4">
            <div v-if="recentActivities.length === 0" class="text-center py-8 text-medium-emphasis">
              <v-icon size="40" class="mb-2">mdi-clipboard-text-off-outline</v-icon>
              <div>لا يوجد سجل نشاطات حالي</div>
            </div>

            <div class="activity-timeline">
              <div
                v-for="activity in recentActivities"
                :key="activity.id"
                class="activity-item d-flex gap-3 mb-4"
              >
                <div class="activity-dot-wrapper">
                  <span class="activity-dot" :class="'bg-' + activity.color"></span>
                </div>
                <div class="flex-grow-1 pb-3 border-b border-slate-100">
                  <div class="d-flex align-center justify-space-between mb-1">
                    <span class="text-body-2 font-weight-bold">{{ activity.action }}</span>
                    <span class="text-caption text-medium-emphasis font-weight-medium">{{ activity.time }}</span>
                  </div>
                  <div class="text-caption text-medium-emphasis d-flex align-center gap-1">
                    <v-icon size="12">mdi-account-outline</v-icon>
                    {{ activity.user }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Top Contributors Leaderboard -->
    <div class="main-card pa-6 rounded-2xl">
      <div class="d-flex align-center justify-space-between mb-6">
        <div>
          <div class="d-flex align-center gap-2 mb-1">
            <v-icon color="amber-darken-2">mdi-trophy-variant</v-icon>
            <h3 class="text-h6 font-weight-bold">أكثر المساهمين إنجازاً</h3>
          </div>
          <p class="text-caption text-medium-emphasis mb-0">لوحة الشرف لأعضاء الفريق الأكثر إضافة للأسئلة</p>
        </div>
      </div>

      <v-row>
        <v-col
          v-for="(contributor, idx) in topContributors"
          :key="contributor.id"
          cols="12" sm="6" md="3"
        >
          <div class="contributor-rank-card pa-4 rounded-xl d-flex align-center gap-3">
            <div class="rank-badge font-weight-black">
              {{ idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : '#' + (idx + 1) }}
            </div>
            <v-avatar :color="contributor.avatarColor" size="46" class="elevation-2">
              <span class="text-subtitle-1 font-weight-black text-white">{{ contributor.initials }}</span>
            </v-avatar>
            <div class="flex-grow-1 overflow-hidden">
              <div class="text-body-2 font-weight-bold text-truncate">{{ contributor.name }}</div>
              <div class="text-caption text-medium-emphasis text-truncate">{{ contributor.role }}</div>
              <div class="d-flex align-center gap-1 mt-1">
                <v-icon size="13" color="amber-darken-2">mdi-star</v-icon>
                <span class="text-caption font-weight-black">{{ contributor.questionsCount }} سؤال</span>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { bankService } from '@/services/bankService'
import { useDataStore } from '@/stores/dataStore'

const dataStore = useDataStore()
const loading = ref(false)
const dashboardData = ref(null)

// Dynamic Greeting based on time of day
const greetingText = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'صباح الخير والبركة'
  if (hour < 18) return 'مساء الخير والنشاط'
  return 'مساء الخير والهدوء'
})

// Status check helpers
const isApproved = (status) => {
  if (!status) return false
  const s = String(status).toLowerCase()
  return s === 'معتمد' || s === 'approved' || s === 'active'
}

const isPending = (status) => {
  if (!status) return false
  const s = String(status).toLowerCase()
  return s === 'قيد المراجعة' || s === 'pending' || s === 'under_review'
}

// ==================== Chart Period ====================
const chartPeriod = ref('month')

// Fetch data from dedicated Backend Dashboard API with fallback
const loadDashboardData = async (period = 'month') => {
  loading.value = true
  try {
    const data = await bankService.getDashboardSummary({ period })
    dashboardData.value = data
  } catch (err) {
    console.error('Failed to load dashboard summary from backend API, using local store fallback:', err)
    await dataStore.loadAcademicData()
    await dataStore.fetchQuestions()
    await dataStore.fetchExams()
  } finally {
    loading.value = false
  }
}

watch(chartPeriod, (newPeriod) => {
  loadDashboardData(newPeriod)
})

onMounted(() => {
  loadDashboardData(chartPeriod.value)
})

// ==================== Computed Stats ====================
const stats = computed(() => {
  if (dashboardData.value?.stats) {
    const s = dashboardData.value.stats
    return {
      totalQuestions: s.total_questions ?? 0,
      approvedQuestions: s.approved_questions ?? 0,
      pendingReview: s.pending_questions ?? 0,
      generatedExams: s.generated_exams ?? 0,
    }
  }
  const questions = dataStore.getAll('questions')
  const total = questions.length
  const approved = questions.filter(q => isApproved(q.status || q.review_status)).length
  const pending = questions.filter(q => isPending(q.status || q.review_status)).length
  const exams = dataStore.getAll('exams').length
  return {
    totalQuestions: total,
    approvedQuestions: approved,
    pendingReview: pending,
    generatedExams: exams,
  }
})

// ==================== Questions by Subject (Bar Chart) ====================
const barColors = [
  'linear-gradient(180deg, #6366f1, #4f46e5)',
  'linear-gradient(180deg, #10b981, #059669)',
  'linear-gradient(180deg, #f59e0b, #d97706)',
  'linear-gradient(180deg, #ef4444, #dc2626)',
  'linear-gradient(180deg, #3b82f6, #2563eb)',
  'linear-gradient(180deg, #8b5cf6, #7c3aed)',
  'linear-gradient(180deg, #ec4899, #db2777)',
  'linear-gradient(180deg, #14b8a6, #0d9488)',
]

const questionsBySubject = computed(() => {
  if (dashboardData.value?.questions_by_subject?.length > 0) {
    return dashboardData.value.questions_by_subject.map((s, i) => ({
      name: s.name,
      count: s.count,
      gradient: barColors[i % barColors.length],
    }))
  }

  const subjects = dataStore.getAll('subjects')
  return subjects.map((s, i) => ({
    name: s.name,
    count: 0,
    gradient: barColors[i % barColors.length],
  }))
})

const maxQuestionCount = computed(() => {
  return Math.max(...questionsBySubject.value.map(s => s.count), 1)
})

const getBarHeight = (count) => {
  return Math.max((count / maxQuestionCount.value) * 88, 6)
}

// ==================== Question Types (Donut Chart) ====================
const donutColors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
const questionTypes = computed(() => {
  if (dashboardData.value?.question_types?.length > 0) {
    return dashboardData.value.question_types.map((t, i) => ({
      name: t.name,
      count: t.count,
      percentage: t.percentage,
      color: donutColors[i % donutColors.length],
      chipColor: ['indigo', 'emerald', 'amber', 'rose', 'purple'][i % 5],
    }))
  }

  return [
    { name: 'اختيار من متعدد', count: 0, percentage: 0, color: donutColors[0], chipColor: 'indigo' },
    { name: 'صح وخطأ', count: 0, percentage: 0, color: donutColors[1], chipColor: 'emerald' },
  ]
})

const donutSegments = computed(() => {
  const circumference = 2 * Math.PI * 50
  const total = stats.value.totalQuestions || 1
  let offset = 0
  return questionTypes.value.map(type => {
    const fraction = type.count / total
    const dashLen = fraction * circumference
    const gap = circumference - dashLen
    const segment = {
      color: type.color,
      dashArray: `${dashLen} ${gap}`,
      dashOffset: -offset,
    }
    offset += dashLen
    return segment
  })
})

// ==================== Difficulty Distribution ====================
const difficultyDistribution = computed(() => {
  if (dashboardData.value?.difficulty_distribution?.length > 0) {
    return dashboardData.value.difficulty_distribution
  }

  return [
    { key: 1, name: 'سهل', color: 'success', count: 0, percentage: 0 },
    { key: 2, name: 'متوسط', color: 'warning', count: 0, percentage: 0 },
    { key: 3, name: 'صعب', color: 'error', count: 0, percentage: 0 },
  ]
})

// ==================== Bloom Level Distribution ====================
const bloomDistribution = computed(() => {
  if (dashboardData.value?.bloom_distribution?.length > 0) {
    return dashboardData.value.bloom_distribution
  }

  const bloomColors = {
    'تذكر': '#6366f1',
    'فهم': '#3b82f6',
    'تطبيق': '#10b981',
    'تحليل': '#f59e0b',
    'تقييم': '#8b5cf6',
    'ابتكار': '#ec4899',
  }

  return ['تذكر', 'فهم', 'تطبيق', 'تحليل', 'تقييم', 'ابتكار'].map(name => ({
    name,
    count: 0,
    color: bloomColors[name] || '#64748b',
    percentage: 0,
  }))
})

const getBloomIcon = (name) => {
  const icons = {
    'تذكر': 'mdi-book-open-outline',
    'فهم': 'mdi-lightbulb-outline',
    'تطبيق': 'mdi-cog-outline',
    'تحليل': 'mdi-chart-pie',
    'تقييم': 'mdi-scale-balance',
    'ابتكار': 'mdi-creation',
  }
  return icons[name] || 'mdi-brain'
}

// ==================== Recent Questions ====================
const recentQuestions = computed(() => {
  if (dashboardData.value?.recent_questions?.length > 0) {
    return dashboardData.value.recent_questions
  }
  return []
})

// ==================== Recent Activities ====================
const recentActivities = computed(() => {
  const logs = dataStore.getAll('auditLogs') || []
  if (logs.length > 0) {
    const users = dataStore.getAll('users')
    const userMap = {}
    users.forEach(u => { userMap[u.id] = u.name || u.full_name || u.username })

    const actionColors = {
      login: 'indigo',
      create: 'emerald',
      update: 'sky',
      delete: 'rose',
      approve: 'emerald',
      reject: 'rose',
    }

    const sorted = [...logs]
      .sort((a, b) => new Date(b.timestamp || 0) - new Date(a.timestamp || 0))
      .slice(0, 5)

    return sorted.map(log => ({
      id: log.id,
      action: log.details || log.action || 'إجراء في النظام',
      user: userMap[log.userId] || 'مستخدم النظام',
      time: getRelativeTime(log.timestamp),
      color: actionColors[log.action] || 'slate',
    }))
  }

  // Fallback to recent questions as activities
  const rq = recentQuestions.value
  return rq.slice(0, 4).map(q => ({
    id: q.id,
    action: `إضافة سؤال جديد في ${q.subject}`,
    user: 'معلم مادة',
    time: getRelativeTime(q.created_at),
    color: 'emerald',
  }))
})

// ==================== Top Contributors ====================
const topContributors = computed(() => {
  if (dashboardData.value?.top_contributors?.length > 0) {
    return dashboardData.value.top_contributors.map(c => ({
      ...c,
      questionsCount: c.questions_count ?? c.questionsCount,
      avatarColor: c.avatar_color ?? c.avatarColor ?? 'indigo-darken-1',
    }))
  }
  return []
})

// ==================== Helper Functions ====================
const getRelativeTime = (timestamp) => {
  if (!timestamp) return 'منذ قليل'
  const date = new Date(timestamp)
  if (isNaN(date.getTime())) return 'منذ قليل'
  const diffMs = Date.now() - date.getTime()
  const diffMins = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffMins < 1) return 'الآن'
  if (diffMins < 60) return `منذ ${diffMins} دقيقة`
  if (diffHours < 24) return `منذ ${diffHours} ساعة`
  if (diffDays < 7) return `منذ ${diffDays} يوم`
  return date.toLocaleDateString('ar-EG')
}

const getStatusColor = (status) => {
  const colors = {
    'معتمد': 'emerald',
    'قيد المراجعة': 'amber',
    'مرفوض': 'rose',
    'مسودة': 'slate',
  }
  return colors[status] || 'slate'
}

const getStatusIcon = (status) => {
  const icons = {
    'معتمد': 'mdi-check-circle',
    'قيد المراجعة': 'mdi-clock-outline',
    'مرفوض': 'mdi-close-circle',
    'مسودة': 'mdi-pencil-outline',
  }
  return icons[status] || 'mdi-file-outline'
}

const getStatusText = (status) => {
  return status || 'مسودة'
}
</script>

<style scoped>
/* ===== Core Theme Compatible ===== */
.dashboard-wrapper {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Hero Header ===== */
.hero-header {
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
  box-shadow: 0 20px 25px -5px rgba(49, 46, 129, 0.25);
  position: relative;
  overflow: hidden;
}

.hero-header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(129, 140, 248, 0.3) 0%, transparent 70%);
  pointer-events: none;
}

.greeting-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.12);
  color: #f8fafc;
  font-size: 0.85rem;
  padding: 4px 12px;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.btn-glow-primary {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
  box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.5) !important;
  transition: all 0.3s ease !important;
}

.btn-glow-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 25px -5px rgba(99, 102, 241, 0.7) !important;
}

/* ===== Stat Glass Cards ===== */
.stat-glass-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-glass-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 16px 35px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.05);
  border-color: rgba(var(--v-border-color), 0.25);
}

.stat-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.bg-indigo-gradient { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.bg-emerald-gradient { background: linear-gradient(135deg, #10b981, #059669); }
.bg-amber-gradient   { background: linear-gradient(135deg, #f59e0b, #d97706); }
.bg-sky-gradient     { background: linear-gradient(135deg, #0ea5e9, #0284c7); }

/* ===== Main Cards ===== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.04);
}

/* ===== Segmented Control Switcher ===== */
.segmented-control {
  display: flex;
  background: rgb(var(--v-theme-background));
  padding: 4px;
  border-radius: 12px;
  gap: 2px;
}

.segmented-control button {
  border: none;
  background: transparent;
  padding: 6px 14px;
  font-size: 0.82rem;
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.7);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.segmented-control button.active {
  background: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-primary));
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

/* ===== Bar Chart ===== */
.modern-bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  width: 100%;
  height: 240px;
  gap: 12px;
}

.modern-bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
  justify-content: flex-end;
}

.bar-badge {
  font-size: 0.78rem;
  margin-bottom: 6px;
}

.bar-track {
  width: 100%;
  max-width: 44px;
  height: 100%;
  display: flex;
  align-items: flex-end;
  background: rgb(var(--v-theme-background));
  border-radius: 10px 10px 4px 4px;
  overflow: hidden;
}

.bar-fill {
  width: 100%;
  border-radius: 10px 10px 4px 4px;
  position: relative;
  transition: height 1s cubic-bezier(0.4, 0, 0.2, 1);
  animation: growUp 1s ease-out forwards;
}

.bar-glow {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 40%;
  background: linear-gradient(180deg, rgba(255,255,255,0.3) 0%, transparent 100%);
}

@keyframes growUp {
  from { transform: scaleY(0); transform-origin: bottom; }
  to   { transform: scaleY(1); transform-origin: bottom; }
}

.bar-title {
  margin-top: 8px;
  text-align: center;
  max-width: 68px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ===== Donut Chart ===== */
.donut-chart-box {
  position: relative;
  width: 180px;
  height: 180px;
}

.donut-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-ring-segment {
  stroke-linecap: round;
  transition: all 0.5s ease;
}

.donut-center-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.legend-item {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  transition: all 0.2s ease;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

/* ===== Gauges & Bloom ===== */
.gauge-row {
  background: rgb(var(--v-theme-background));
  padding: 12px;
  border-radius: 12px;
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.bloom-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.bloom-card {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.bloom-card:hover {
  background: rgb(var(--v-theme-surface));
  border-color: rgba(var(--v-border-color), 0.25);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  transform: translateY(-3px);
}

.bloom-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ===== Quick Action Cards ===== */
.action-card-link {
  text-decoration: none;
  color: inherit;
}

.action-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 16px 35px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.05);
  border-color: rgba(var(--v-border-color), 0.25);
}

.action-icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-indigo-light  { background: rgba(99, 102, 241, 0.15); }
.bg-emerald-light { background: rgba(16, 185, 129, 0.15); }
.bg-amber-light   { background: rgba(245, 158, 11, 0.15); }
.bg-purple-light  { background: rgba(168, 85, 247, 0.15); }

/* ===== Question Row ===== */
.question-item-row {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.question-item-row:hover {
  background: rgb(var(--v-theme-surface));
  border-color: rgba(var(--v-border-color), 0.25);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  transform: translateY(-3px);
}

/* ===== Timeline Activity ===== */
.activity-timeline {
  display: flex;
  flex-direction: column;
}

.activity-dot-wrapper {
  display: flex;
  align-items: flex-start;
  padding-top: 4px;
}

.activity-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.bg-indigo  { background-color: #6366f1; }
.bg-emerald { background-color: #10b981; }
.bg-sky     { background-color: #0ea5e9; }
.bg-rose    { background-color: #f43f5e; }
.bg-slate   { background-color: #94a3b8; }

/* ===== Leaderboard ===== */
.contributor-rank-card {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.contributor-rank-card:hover {
  background: rgb(var(--v-theme-surface));
  border-color: rgba(var(--v-border-color), 0.25);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  transform: translateY(-3px);
}

.rank-badge {
  font-size: 1.2rem;
}
</style>
