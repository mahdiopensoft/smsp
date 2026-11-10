<template>
  <div class="omr-ai-scoring-policy-view">
    <!-- Header Hero Banner -->
    <v-card class="pa-4 pa-md-5 rounded-2xl border mb-5 bg-surface elevation-1">
      <div class="d-flex align-center justify-space-between flex-wrap gap-3">
        <div class="d-flex align-center gap-3">
          <v-avatar color="indigo-lighten-5" size="52" class="rounded-xl border border-indigo-lighten-4">
            <v-icon color="indigo-darken-1" size="30">mdi-brain</v-icon>
          </v-avatar>
          <div>
            <div class="d-flex align-center gap-2">
              <h1 class="text-h6 font-weight-black mb-0">لوحة إعدادات وسياسات الذكاء الاصطناعي والتصحيح</h1>
              <v-chip size="small" color="success" variant="flat" class="font-weight-bold">
                مباشر ونشط
              </v-chip>
            </div>
            <p class="text-caption text-medium-emphasis mb-0 mt-1">
              ضبط عتبات الرؤية الحاسوبية (OpenCV + YOLOv8 + ResNet) وقواعد احتساب درجات التظليل المتعدد، الشطب، والدرجات السالبة.
            </p>
          </div>
        </div>

        <!-- Template Selector and Quick Save Actions -->
        <div class="d-flex align-center gap-2 flex-wrap">
          <div style="min-width: 240px; max-width: 320px;">
            <v-select
              v-model="selectedTemplateId"
              :items="templateSelectOptions"
              item-title="name"
              item-value="id"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              prepend-inner-icon="mdi-card-text-outline"
              label="القالب المستهدف للتخصيص"
              @update:model-value="onTemplateSelected"
            />
          </div>

          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-content-save-check-outline"
            :loading="isSaving"
            @click="handleSavePolicies"
          >
            حفظ واعتماد السياسات
          </v-btn>
        </div>
      </div>
    </v-card>

    <v-row>
      <!-- Column 1: AI Vision & Optical Thresholds -->
      <v-col cols="12" md="6">
        <v-card class="pa-4 pa-md-5 rounded-2xl border bg-surface elevation-0 h-100">
          <div class="d-flex align-center gap-2 mb-4 pb-2 border-b">
            <v-avatar color="primary" variant="tonal" size="32" class="rounded-lg">
              <v-icon size="18">mdi-eye-check-outline</v-icon>
            </v-avatar>
            <div>
              <h2 class="text-subtitle-1 font-weight-black mb-0">معايير الرؤية والذكاء الاصطناعي</h2>
              <span class="text-caption text-medium-emphasis">ضبط حساسية النماذج العصبية وكثافة الحبر</span>
            </div>
          </div>

          <!-- Engine Selection -->
          <div class="pa-3 rounded-xl border bg-grey-lighten-5 mb-4">
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-caption font-weight-bold">محرك التحليل البصري:</span>
              <v-chip size="x-small" color="primary" class="font-weight-bold">موصى به</v-chip>
            </div>
            <v-radio-group v-model="detection.engine" hide-details density="compact">
              <v-radio value="opencv_omr" color="primary" class="mb-2">
                <template #label>
                  <div>
                    <strong class="text-caption font-weight-bold">OpenCV + الذكاء الاصطناعي (YOLOv8 & CNN)</strong>
                    <div class="text-caption text-medium-emphasis">أعلى دقة قراءة بمحاذاة المربعات الأربعة وكشف الشطب.</div>
                  </div>
                </template>
              </v-radio>
              <v-radio value="legacy_vector" color="primary">
                <template #label>
                  <div>
                    <strong class="text-caption font-weight-bold">المحرك الكلاسيكي البسيط (Vector Engine)</strong>
                    <div class="text-caption text-medium-emphasis">حساب كثافة البكسلات المباشرة بدون شبكة عصبية.</div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>

          <!-- Shading Thresholds -->
          <div class="pa-3 rounded-xl border bg-grey-lighten-5 mb-4">
            <span class="text-caption font-weight-bold d-block mb-3">عتبات كثافة التظليل المادي (Physical Ink):</span>

            <div class="mb-3">
              <div class="d-flex justify-space-between align-center mb-1">
                <span class="text-caption">الحد الأدنى لاعتبار الفقاعة مظللة:</span>
                <v-chip size="x-small" color="primary" class="font-weight-black">{{ detection.thresholds.filled_min }}%</v-chip>
              </div>
              <v-slider
                v-model="detection.thresholds.filled_min"
                min="40"
                max="80"
                step="5"
                thumb-label
                color="primary"
                hide-details
              />
            </div>

            <div>
              <div class="d-flex justify-space-between align-center mb-1">
                <span class="text-caption">الحد الأقصى للفقاعة الفارغة (فراغ):</span>
                <v-chip size="x-small" color="secondary" class="font-weight-black">{{ detection.thresholds.empty_max }}%</v-chip>
              </div>
              <v-slider
                v-model="detection.thresholds.empty_max"
                min="10"
                max="35"
                step="1"
                thumb-label
                color="secondary"
                hide-details
              />
            </div>
          </div>

          <!-- AI Model Confidence Sliders -->
          <div class="pa-3 rounded-xl border bg-grey-lighten-5 mb-4">
            <div class="d-flex align-center justify-space-between mb-3">
              <div>
                <span class="text-caption font-weight-bold d-block">التحقق بالذكاء الاصطناعي (AI Verification):</span>
                <span class="text-caption text-medium-emphasis">تمرير الفقاعات للشبكات العصبية لتمييز المسح والشطب</span>
              </div>
              <v-switch v-model="detection.ai_verification" color="success" hide-details density="compact" />
            </div>

            <div v-if="detection.ai_verification" class="pt-2 border-t">
              <div class="d-flex justify-space-between align-center mb-1">
                <span class="text-caption">عتبة ثقة نموذج كشف الفقاعات YOLOv8:</span>
                <v-chip size="x-small" color="success" class="font-weight-black">{{ Math.round((omrModel.yolo_conf || 0.35) * 100) }}%</v-chip>
              </div>
              <v-slider
                v-model="omrModel.yolo_conf"
                min="0.20"
                max="0.80"
                step="0.05"
                thumb-label
                color="success"
                hide-details
              />

              <div class="d-flex justify-space-between align-center mb-1 mt-3">
                <span class="text-caption">عتبة ثقة شبكة التصنيف المساعد ResNet CNN:</span>
                <v-chip size="x-small" color="indigo" class="font-weight-black">{{ Math.round((omrModel.cnn_conf || 0.75) * 100) }}%</v-chip>
              </div>
              <v-slider
                v-model="omrModel.cnn_conf"
                min="0.50"
                max="0.95"
                step="0.05"
                thumb-label
                color="indigo"
                hide-details
              />
            </div>
          </div>

          <!-- Alignment Tolerance -->
          <div class="pa-3 rounded-xl border bg-grey-lighten-5">
            <div class="d-flex justify-space-between align-center mb-2">
              <span class="text-caption font-weight-bold">تسامح انحراف الورقة بالملم:</span>
              <v-chip size="x-small" color="warning" class="font-weight-black">{{ detection.tolerance_mm }} مم</v-chip>
            </div>
            <v-slider
              v-model="detection.tolerance_mm"
              min="0.5"
              max="3.0"
              step="0.1"
              thumb-label
              color="warning"
              hide-details
            />
          </div>
        </v-card>
      </v-col>

      <!-- Column 2: Academic Scoring Policies -->
      <v-col cols="12" md="6">
        <v-card class="pa-4 pa-md-5 rounded-2xl border bg-surface elevation-0 h-100">
          <div class="d-flex align-center gap-2 mb-4 pb-2 border-b">
            <v-avatar color="indigo" variant="tonal" size="32" class="rounded-lg">
              <v-icon size="18">mdi-scale-balance</v-icon>
            </v-avatar>
            <div>
              <h2 class="text-subtitle-1 font-weight-black mb-0">سياسات احتساب الدرجات الأكاديمية</h2>
              <span class="text-caption text-medium-emphasis">قواعد احتساب التردد والتظليل المتعدد والشطب</span>
            </div>
          </div>

          <!-- Component for granular scoring policies -->
          <ScoringPolicySettingsCard :config="config" />
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import ScoringPolicySettingsCard from './ScoringPolicySettingsCard.vue'

const props = defineProps<{
  config: any
  savedTemplatesList: any[]
  savedDbId: any
  isSaving: boolean
}>()

const emit = defineEmits<{
  (e: 'save-template'): void
  (e: 'load-template', template: any): void
}>()

const selectedTemplateId = ref<number | string | null>(props.savedDbId || null)

// Build template select options
const templateSelectOptions = computed(() => {
  const list = (props.savedTemplatesList || []).map((t: any) => ({
    id: t.id,
    name: t.name || `قالب رقم ${t.id}`,
  }))
  return [
    { id: 'current', name: `القالب النشط حالياً: ${props.config.template_name || 'بدون اسم'}` },
    ...list,
  ]
})

function onTemplateSelected(val: any) {
  if (!val || val === 'current') return
  const found = (props.savedTemplatesList || []).find((t: any) => t.id === val)
  if (found) {
    emit('load-template', found)
  }
}

watch(
  () => props.savedDbId,
  (newId) => {
    if (newId) selectedTemplateId.value = newId
  }
)

function handleSavePolicies() {
  emit('save-template')
}

// Ensure nested detection object exists
if (!props.config.detection) {
  props.config.detection = {
    engine: 'opencv_omr',
    ai_verification: true,
    thresholds: {
      filled_min: 55,
      empty_max: 28,
    },
    tolerance_mm: 1.0,
  }
} else if (!props.config.detection.thresholds) {
  props.config.detection.thresholds = {
    filled_min: 55,
    empty_max: 28,
  }
}

// Ensure omr_config exists
if (!props.config.omr_config) {
  props.config.omr_config = {}
}
if (!props.config.omr_config.model) {
  props.config.omr_config.model = {
    yolo_conf: 0.35,
    cnn_conf: 0.75,
    enable_cnn_fallback: true,
  }
}

const detection = computed(() => props.config.detection)
const omrModel = computed(() => props.config.omr_config.model)
</script>
