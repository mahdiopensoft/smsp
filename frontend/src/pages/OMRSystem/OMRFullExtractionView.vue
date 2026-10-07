<template>
  <div class="qb-full-extraction-v4">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-api</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">محرك الاستخراج والتكامل المباشر</h1>
          <p class="text-caption text-medium-emphasis mb-0">واجهة الربط المباشر مع محرك الباك-إند لاستخراج بيانات OMR</p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          v-if="submission && submission.status === 'completed'"
          color="primary"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-refresh"
          @click="reset"
        >
          معالجة وثيقة جديدة
        </v-btn>
      </div>
    </div>

    <!-- Error State -->
    <v-alert v-if="errorMsg" type="error" variant="tonal" class="mb-6 rounded-2xl font-weight-bold">
      {{ errorMsg }}
    </v-alert>

    <!-- Upload Section -->
    <div
      v-if="!submission && exams.length > 0 && !isUploading"
      class="main-card pa-12 rounded-2xl text-center cursor-pointer border-subtle mb-6 hover-lift"
      @click="triggerFileInput"
      @dragover.prevent
      @drop.prevent="handleDrop"
    >
      <input type="file" ref="fileInput" accept="image/*,application/pdf" class="d-none" @change="handleFileSelect" />

      <v-avatar size="72" color="primary" variant="tonal" class="mb-4 rounded-2xl">
        <v-icon size="36">mdi-cloud-upload-outline</v-icon>
      </v-avatar>
      <h3 class="text-h6 font-weight-black mb-2">ارفع الوثيقة الفعلية للمحرك مباشرة</h3>
      <p class="text-body-2 text-medium-emphasis mb-4">
        سيتم ربطها بالاختبار: <strong class="text-primary">{{ selectedExam?.name || exams[0]?.name }}</strong>
      </p>

      <div v-if="exams.length > 1" class="d-inline-flex align-center gap-2 pa-2 rounded-xl border-subtle" @click.stop>
        <span class="text-caption font-weight-bold text-medium-emphasis">اختر الاختبار:</span>
        <v-select
          v-model="selectedExamId"
          :items="exams"
          item-title="name"
          item-value="id"
          density="compact"
          variant="outlined"
          rounded="lg"
          hide-details
          style="width: 220px;"
        />
      </div>
    </div>

    <!-- Uploading Status -->
    <div v-if="isUploading" class="main-card pa-12 rounded-2xl text-center mb-6">
      <v-progress-circular indeterminate color="primary" size="48" class="mb-4" />
      <h3 class="text-h6 font-weight-black mb-0">جاري الرفع والمعالجة في محرك OMR...</h3>
    </div>

    <!-- Processing Monitor (Real API Data) -->
    <div v-if="submission" class="d-flex flex-column gap-6">
      <div class="main-card pa-6 rounded-2xl">
        <div class="d-flex justify-space-between align-center mb-6 border-b pb-4">
          <div>
            <h3 class="text-h6 font-weight-black mb-1">مراقبة المحرك المباشرة (Engine Monitor)</h3>
            <span class="text-caption text-medium-emphasis">معرف السجل (ID): {{ submission.id }}</span>
          </div>
          <v-chip :color="statusSeverity(submission.status)" variant="flat" class="font-weight-bold text-white px-4">
            {{ statusLabel(submission.status) }}
          </v-chip>
        </div>

        <div class="pa-4 rounded-xl border-subtle d-flex align-center gap-4 mb-6">
          <div>
            <span class="text-caption font-weight-bold text-medium-emphasis d-block mb-1">المحرك النشط حالياً:</span>
            <span class="font-weight-black text-primary text-body-1">{{ submission.current_stage_label || 'محرك القراءة الهجين' }}</span>
          </div>
        </div>

        <div class="d-flex justify-space-between align-center">
          <custom-btn type="add" label="إعادة ضبط" variant="tonal" class="font-weight-bold" :click="reset" />
          <custom-btn type="add" label="عرض تحليل الثقة والتفاصيل الكاملة ←" color="primary" class="font-weight-bold px-6" :click="() => $router.push(`/omr/submissions/${submission.id}`)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { examsAPI, submissionsAPI } from '../../services/omr/endpoints.js'

const exams = ref([])
const selectedExamId = ref(null)
const submission = ref(null)
const errorMsg = ref('')
const isUploading = ref(false)
const fileInput = ref(null)
let pollTimer = null

const selectedExam = computed(() => exams.value.find(e => e.id === selectedExamId.value))

function statusSeverity(status) {
  const map = { completed: 'success', needs_review: 'warning', failed: 'error', pending: 'info', processing: 'info' }
  return map[status] || 'info'
}

function statusLabel(status) {
  const map = { completed: 'مكتمل', needs_review: 'مراجعة', failed: 'فشل', pending: 'انتظار', processing: 'معالجة' }
  return map[status] || status
}

onMounted(async () => {
  try {
    const res = await examsAPI.list()
    exams.value = res.data.results || []
    if (exams.value.length > 0) {
      selectedExamId.value = exams.value[0].id
    } else {
      errorMsg.value = 'لا توجد اختبارات مضافة في النظام.'
    }
  } catch (err) {
    errorMsg.value = 'فشل في الاتصال بمحرك OMR.'
  }
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) uploadFile(file)
}

function handleDrop(e) {
  const file = e.dataTransfer.files[0]
  if (file) uploadFile(file)
}

async function uploadFile(file) {
  if (!selectedExamId.value) return
  isUploading.value = true
  try {
    const formData = new FormData()
    formData.append('exam', selectedExamId.value)
    formData.append('original_image', file)
    const res = await submissionsAPI.create(formData)
    submission.value = res.data
    startPolling(res.data.id)
  } catch (err) {
    errorMsg.value = 'فشل رفع الملف للمحرك.'
  } finally {
    isUploading.value = false
  }
}

function startPolling(id) {
  if (pollTimer) clearInterval(pollTimer)
  pollTimer = setInterval(async () => {
    try {
      const res = await submissionsAPI.get(id)
      submission.value = res.data
      if (['completed', 'needs_review', 'failed'].includes(res.data.status)) {
        clearInterval(pollTimer)
      }
    } catch (e) {
      clearInterval(pollTimer)
    }
  }, 2000)
}

function reset() {
  submission.value = null
  if (pollTimer) clearInterval(pollTimer)
}
</script>

<style scoped>
.qb-full-extraction-v4 {
  color: rgb(var(--v-theme-on-surface));
}

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
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06) !important;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
