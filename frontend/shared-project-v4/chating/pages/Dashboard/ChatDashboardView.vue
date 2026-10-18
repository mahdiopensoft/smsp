<template>
  <div class="chat-dashboard pa-6">


    <!-- Filters Row -->
    <v-card class="mb-6 rounded-xl border-thin bg-surface" variant="flat" v-if="company_level && [20, 30, 40].includes(company_level.zi)">
      <v-card-text>
        <v-row class="align-center">
          <fields
            :data="filter"
            :fields="$filter_fields()"
            :attr="{
              fk_governorate: {
                depend: true,
                cols: 3,
              },
              fk_directorate: {
                depend: true,
                cols: 3,
                param: filter?.fk_governorate,
              },
              fk_school: {
                depend: true,
                cols: 3,
                param: filter?.fk_directorate,
              },
            }"
          />
          <v-col cols="3" class="d-flex justify-end">
            <v-btn variant="text" color="error" @click="resetFilters" prepend-icon="mdi-close" class="me-3">
              إعادة ضبط (إحصائية كاملة)
            </v-btn>
            <v-btn color="primary" @click="loadStats" prepend-icon="mdi-filter" :loading="loading">
              تطبيق الفلاتر
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Skeleton Loader -->
    <div v-if="loading && !stats" class="d-flex flex-column gap-6">
      <v-row>
        <v-col cols="12" md="3" v-for="i in 4" :key="i">
          <v-skeleton-loader type="article" class="rounded-xl"></v-skeleton-loader>
        </v-col>
      </v-row>
      <v-skeleton-loader type="image" height="400" class="rounded-xl"></v-skeleton-loader>
    </div>

    <div v-else-if="stats" class="dashboard-content">
      <!-- KPI Cards Row 1 -->
      <v-row class="mb-4">
        <v-col cols="12" sm="6" md="3">
          <v-card class="stat-card rounded-xl pa-5 bg-surface border-thin" variant="flat">
            <div class="d-flex justify-space-between align-start">
              <div>
                <div class="text-overline text-medium-emphasis mb-1">إجمالي المحادثات</div>
                <div class="text-h3 font-weight-bold color-text-primary">{{ stats.summary.total_chats }}</div>
              </div>
              <v-avatar color="primary" variant="tonal" rounded="lg" size="48">
                <v-icon icon="mdi-forum" size="28"></v-icon>
              </v-avatar>
            </div>
            <div class="d-flex align-center mt-4 text-caption">
              <span class="text-success font-weight-bold me-1">
                <v-icon icon="mdi-account-group" size="14" class="me-1"></v-icon>
                {{ stats.summary.group_chats }} مجموعات
              </span>
              <v-spacer></v-spacer>
              <span class="text-info font-weight-bold">
                <v-icon icon="mdi-account" size="14" class="me-1"></v-icon>
                {{ stats.summary.private_chats }} خاصة
              </span>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="stat-card rounded-xl pa-5 bg-surface border-thin" variant="flat">
            <div class="d-flex justify-space-between align-start">
              <div>
                <div class="text-overline text-medium-emphasis mb-1">إجمالي الرسائل</div>
                <div class="text-h3 font-weight-bold color-text-primary">{{ stats.summary.total_messages }}</div>
              </div>
              <v-avatar color="info" variant="tonal" rounded="lg" size="48">
                <v-icon icon="mdi-message-text" size="28"></v-icon>
              </v-avatar>
            </div>
            <div class="mt-4 text-caption text-medium-emphasis">
              <v-icon icon="mdi-trending-up" size="14" color="success" class="me-1"></v-icon>
              <span class="font-weight-bold text-success">{{ stats.summary.messages_last_week }}</span> رسالة هذا الأسبوع
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="stat-card rounded-xl pa-5 bg-surface border-thin" variant="flat">
            <div class="d-flex justify-space-between align-start">
              <div>
                <div class="text-overline text-medium-emphasis mb-1">التعميمات</div>
                <div class="text-h3 font-weight-bold color-text-primary">{{ stats.summary.total_generalizations }}</div>
              </div>
              <v-avatar color="warning" variant="tonal" rounded="lg" size="48">
                <v-icon icon="mdi-bullhorn" size="28"></v-icon>
              </v-avatar>
            </div>
            <div class="mt-4 text-caption text-medium-emphasis">
              <v-icon icon="mdi-calendar-month" size="14" class="me-1"></v-icon>
              <span class="font-weight-bold color-text-primary">{{ stats.summary.generalizations_last_month }}</span> تعميم هذا الشهر
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="stat-card rounded-xl pa-5 bg-surface border-thin" variant="flat">
            <div class="d-flex justify-space-between align-start">
              <div>
                <div class="text-overline text-medium-emphasis mb-1">ردود التعميمات</div>
                <div class="text-h3 font-weight-bold color-text-primary">{{ stats.summary.total_replies }}</div>
              </div>
              <v-avatar color="success" variant="tonal" rounded="lg" size="48">
                <v-icon icon="mdi-reply-all" size="28"></v-icon>
              </v-avatar>
            </div>
            <div class="mt-4 text-caption text-medium-emphasis">
              إجمالي الردود المباشرة من المستهدفين
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Charts & Lists -->
      <v-row>
        <!-- Activity Chart -->
        <v-col cols="12" lg="8">
          <v-card class="rounded-xl border-thin bg-surface h-100" variant="flat">
            <v-card-title class="px-6 pt-6 pb-2 d-flex align-center">
              <v-icon icon="mdi-chart-areaspline" color="primary" class="me-2"></v-icon>
              نشاط النظام خلال الأسبوع
            </v-card-title>
            <v-card-text class="px-2 pb-6">
              <apexchart
                type="area"
                height="350"
                :options="chartOptions"
                :series="chartSeries"
              ></apexchart>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Donut Chart -->
        <v-col cols="12" lg="4">
          <v-card class="rounded-xl border-thin bg-surface h-100" variant="flat">
            <v-card-title class="px-6 pt-6 pb-2 d-flex align-center">
              <v-icon icon="mdi-chart-donut" color="primary" class="me-2"></v-icon>
              توزيع المحادثات النشطة
            </v-card-title>
            <v-card-text class="pt-4 d-flex align-center justify-center" style="height: 350px;">
              <apexchart type="donut" height="300" :options="chatTypesOptions" :series="chatTypesSeries"></apexchart>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <!-- Top Chats Bar Chart -->
        <v-col cols="12" lg="8">
          <v-card class="rounded-xl border-thin bg-surface h-100" variant="flat">
            <v-card-title class="px-6 pt-6 pb-2 d-flex align-center">
              <v-icon icon="mdi-fire" color="error" class="me-2"></v-icon>
              أكثر المحادثات تفاعلاً
            </v-card-title>
            <v-card-text class="pt-4">
              <apexchart type="bar" height="350" :options="topChatsOptions" :series="topChatsSeries"></apexchart>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Generalization Status Pie Chart -->
        <v-col cols="12" lg="4">
          <v-card class="rounded-xl border-thin bg-surface h-100" variant="flat">
            <v-card-title class="px-6 pt-6 pb-2 d-flex align-center">
              <v-icon icon="mdi-reply-all-outline" color="success" class="me-2"></v-icon>
              معدل الرد على التعميمات (الهامة)
            </v-card-title>
            <v-card-text class="pt-4 d-flex align-center justify-center" style="height: 350px;">
              <apexchart type="pie" height="300" :options="genStatusOptions" :series="genStatusSeries"></apexchart>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <!-- Peak Hours Chart -->
        <v-col cols="12" lg="12">
          <v-card class="rounded-xl border-thin bg-surface h-100" variant="flat">
            <v-card-title class="px-6 pt-6 pb-2 d-flex align-center">
              <v-icon icon="mdi-clock-time-four-outline" color="warning" class="me-2"></v-icon>
              أوقات الذروة (خلال آخر 7 أيام)
            </v-card-title>
            <v-card-text class="pt-4">
              <apexchart type="bar" height="300" :options="peakHoursOptions" :series="peakHoursSeries"></apexchart>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Error State -->
    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      class="rounded-xl mt-6"
      closable
      @click:close="error = null"
    >
      {{ error }}
    </v-alert>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, getCurrentInstance } from 'vue'
import { useTheme } from 'vuetify'
import { dashboardService } from '../../services/dashboardService'
import api from '../../../plugins/axios-plugin'
import apexchart from 'vue3-apexcharts'

const theme = useTheme()
const { proxy } = getCurrentInstance()
const company_level = computed(() => proxy.$state?.profile || {})

const loading = ref(true)

const filter = ref({
  fk_governorate: null,
  fk_directorate: null,
  fk_school: null
})

// Clear child filters when parent changes
watch(() => filter.value.fk_governorate, () => {
  filter.value.fk_directorate = null
  filter.value.fk_school = null
})

watch(() => filter.value.fk_directorate, () => {
  filter.value.fk_school = null
})

function resetFilters() {
  filter.value = {
    fk_governorate: null,
    fk_directorate: null,
    fk_school: null
  }
  loadStats()
}
const stats = ref(null)
const error = ref(null)


const topChatsSeries = computed(() => {
  if (!stats.value || !stats.value.top_chats) return [{ name: 'الرسائل', data: [] }]
  return [{
    name: 'الرسائل',
    data: stats.value.top_chats.map(chat => chat.messages_count)
  }]
})

const topChatsOptions = computed(() => {
  const categories = stats.value && stats.value.top_chats ? stats.value.top_chats.map(chat => chat.name) : []
  return {
    chart: { type: 'bar', toolbar: { show: false }, fontFamily: 'inherit' },
    plotOptions: { bar: { horizontal: true, borderRadius: 4, barHeight: '50%' } },
    colors: ['#ef4444'], // error color for fire icon match
    dataLabels: { enabled: true },
    xaxis: { categories: categories, labels: { style: { colors: '#9ca3af' } } },
    yaxis: { labels: { style: { colors: '#9ca3af', fontWeight: 'bold' }, maxWidth: 150 } },
    grid: { strokeDashArray: 4, borderColor: 'rgba(156, 163, 175, 0.1)' },
    theme: { mode: 'light' }
  }
})

const chatTypesSeries = computed(() => {
  if (!stats.value || !stats.value.summary) return [0, 0]
  return [stats.value.summary.group_chats || 0, stats.value.summary.private_chats || 0]
})

const chatTypesOptions = computed(() => {
  return {
    chart: { type: 'donut', fontFamily: 'inherit' },
    labels: ['مجموعات', 'محادثات خاصة'],
    colors: [theme.current.value.colors.success, theme.current.value.colors.primary], // success and primary colors
    plotOptions: { pie: { donut: { size: '65%' } } },
    stroke: { width: 0 },
    legend: { position: 'bottom' },
    dataLabels: { enabled: false }
  }
})

const chartSeries = computed(() => {
  if (!stats.value) return []
  return [
    {
      name: 'الرسائل',
      data: stats.value.daily_activity.map(d => d.messages)
    },
    {
      name: 'التعميمات',
      data: stats.value.daily_activity.map(d => d.generalizations)
    }
  ]
})

const chartOptions = computed(() => {
  const dates = stats.value ? stats.value.daily_activity.map(d => d.date) : []
  
  return {
    chart: {
      type: 'area',
      fontFamily: 'inherit',
      toolbar: { show: false },
      zoom: { enabled: false }
    },
    colors: [theme.current.value.colors.primary, theme.current.value.colors.success],
    dataLabels: { enabled: false },
    stroke: {
      curve: 'smooth',
      width: 3
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.4,
        opacityTo: 0.05,
        stops: [0, 90, 100]
      }
    },
    xaxis: {
      categories: dates,
      axisBorder: { show: false },
      axisTicks: { show: false },
      labels: {
        style: { colors: '#9ca3af' }
      }
    },
    yaxis: {
      labels: {
        style: { colors: '#9ca3af' }
      }
    },
    grid: {
      borderColor: 'rgba(156, 163, 175, 0.1)',
      strokeDashArray: 4,
      xaxis: { lines: { show: true } },
      yaxis: { lines: { show: true } }
    },
    theme: { mode: 'light' },
    legend: {
      position: 'top',
      horizontalAlign: 'right'
    }
  }
})

const peakHoursSeries = computed(() => {
  if (!stats.value || !stats.value.peak_hours) return [{ name: 'نشاط', data: [] }]
  const data = []
  for (let i = 0; i < 24; i++) {
    data.push(stats.value.peak_hours[i.toString()] || 0)
  }
  return [{ name: 'حجم الرسائل', data }]
})

const peakHoursOptions = computed(() => {
  const categories = Array.from({ length: 24 }, (_, i) => `${i}:00`)
  return {
    chart: { type: 'bar', toolbar: { show: false }, fontFamily: 'inherit' },
    plotOptions: { bar: { borderRadius: 4, columnWidth: '60%' } },
    colors: ['#f59e0b'], // warning color
    dataLabels: { enabled: false },
    xaxis: { categories: categories, labels: { style: { colors: '#9ca3af' } }, tickAmount: 12 },
    yaxis: { labels: { style: { colors: '#9ca3af' } } },
    grid: { strokeDashArray: 4, borderColor: 'rgba(156, 163, 175, 0.1)' },
    theme: { mode: 'light' }
  }
})

const genStatusSeries = computed(() => {
  if (!stats.value || !stats.value.generalization_status) return [0, 0]
  const status = stats.value.generalization_status
  return [status.replied || 0, status.pending || 0]
})

const genStatusOptions = computed(() => {
  return {
    chart: { type: 'pie', fontFamily: 'inherit' },
    labels: ['تم الرد', 'بانتظار الرد'],
    colors: ['#10b981', '#f43f5e'], // success and error colors
    stroke: { width: 0 },
    legend: { position: 'bottom' },
    dataLabels: { enabled: true }
  }
})

async function loadStats() {
  loading.value = true
  error.value = null
  try {
    const apiFilters = {
      governorate_id: filter.value.fk_governorate,
      directorate_id: filter.value.fk_directorate,
      organization_id: filter.value.fk_school
    }
    stats.value = await dashboardService.getStats(apiFilters)
  } catch (err) {
    console.error('Error loading dashboard stats:', err)
    error.value = 'حدث خطأ أثناء تحميل الإحصائيات. الرجاء المحاولة مرة أخرى.'
    if (err.response?.status === 403) {
      error.value = 'ليس لديك صلاحية للوصول إلى لوحة التحكم. هذه الصفحة مخصصة لمدراء النظام فقط.'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.chat-dashboard {
  min-height: 100vh;
  background-color: rgba(var(--v-theme-background), 0.5);
}

.stat-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, rgba(var(--v-theme-primary), 0.8), rgba(var(--v-theme-info), 0.8));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08) !important;
}

.stat-card:hover::before {
  opacity: 1;
}

.top-chat-item {
  transition: background-color 0.2s ease;
  border: 1px solid transparent;
}

.top-chat-item:hover {
  background-color: rgba(var(--v-theme-surface-variant), 0.3);
  border-color: rgba(var(--v-border-color), 0.2);
}

.color-text-primary {
  color: rgba(var(--v-theme-on-surface), 0.87);
}
</style>
