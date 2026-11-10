<template>
  <div class="detection-settings">
    <!-- Top Sub-Tabs: AI Engine vs Academic Scoring Policies -->
    <v-tabs v-model="activeSubTab" density="compact" color="primary" class="mb-4 border-b rounded-lg bg-surface" grow>
      <v-tab value="ai_engine" class="font-weight-bold text-caption">
        <v-icon start size="16">mdi-brain</v-icon>
        الرؤية والذكاء الاصطناعي
      </v-tab>
      <v-tab value="scoring_policy" class="font-weight-bold text-caption">
        <v-icon start size="16">mdi-scale-balance</v-icon>
        سياسات احتساب الدرجات
      </v-tab>
    </v-tabs>

    <div v-show="activeSubTab === 'ai_engine'">
      <!-- Engine Selector Box -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <div class="d-flex align-center justify-space-between mb-3">
          <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-cog-sync-outline</v-icon>
            محرك التحليل والتعرف البصري
          </label>
          <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">مربوط بالخادم</v-chip>
        </div>

        <v-radio-group
          v-model="detection.engine"
          hide-details
          class="mt-1"
        >
          <v-radio value="opencv_omr" color="primary" class="mb-2">
            <template #label>
              <div>
                <strong class="text-body-2 font-weight-bold">OpenCV + الذكاء الاصطناعي (موصى به)</strong>
                <p class="text-caption text-medium-emphasis mb-0">
                  أعلى دقة قراءة بمحاذاة المربعات الأربعة واستخدام YOLOv8 و CNN للتحقق من الشخبطة والتظليل الملتبس.
                </p>
              </div>
            </template>
          </v-radio>
          <v-radio value="legacy_vector" color="primary">
            <template #label>
              <div>
                <strong class="text-body-2 font-weight-bold">المحرك الكلاسيكي البسيط (Vector Engine)</strong>
                <p class="text-caption text-medium-emphasis mb-0">
                  حساب كثافة البكسلات المباشرة بدون شبكة عصبية.
                </p>
              </div>
            </template>
          </v-radio>
        </v-radio-group>
      </div>

      <!-- Bubble Shading Thresholds Box -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2 mb-3">
          <v-icon color="indigo" size="20">mdi-contrast-box</v-icon>
          عتبات التعرف على التظليل وكثافة الحبر
        </label>

        <!-- Filled Min Threshold -->
        <div class="mb-4">
          <div class="d-flex justify-space-between align-center mb-1">
            <span class="text-caption font-weight-bold">الحد الأدنى لاعتبار الفقاعة مظللة:</span>
            <v-chip size="x-small" color="primary" class="font-weight-black">
              {{ detection.thresholds.filled_min }}%
            </v-chip>
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
          <span class="text-caption text-medium-emphasis d-block mt-1">
            أي فقاعة تتجاوز كثافة الحبر فيها هذه النسبة تُعتبر اختياراً مؤكداً للطالب.
          </span>
        </div>

        <!-- Empty Max Threshold -->
        <div class="mb-2">
          <div class="d-flex justify-space-between align-center mb-1">
            <span class="text-caption font-weight-bold">الحد الأقصى للفقاعة الفارغة:</span>
            <v-chip size="x-small" color="secondary" class="font-weight-black">
              {{ detection.thresholds.empty_max }}%
            </v-chip>
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
          <span class="text-caption text-medium-emphasis d-block mt-1">
            أقل من هذه النسبة يعتبر فراغاً أو إطار الدائرة المطبوعة فقط.
          </span>
        </div>
      </div>

      <!-- AI Neural Verification Switch & Model Confidence -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <div class="d-flex align-center justify-space-between mb-3">
          <div>
            <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
              <v-icon color="success" size="20">mdi-brain</v-icon>
              التحقق بالذكاء الاصطناعي (AI Verification)
            </label>
            <span class="text-caption text-medium-emphasis d-block mt-0.5">
              تمرير الفقاعات الملتبسة أو المشطوبة لشبكة تصنيف عصبية لتمييز المسح والمخالفات
            </span>
          </div>
          <v-switch
            v-model="detection.ai_verification"
            color="success"
            hide-details
            density="compact"
          />
        </div>

        <div v-if="detection.ai_verification" class="pt-2 border-t mt-2">
          <div class="d-flex justify-space-between align-center mb-1">
            <span class="text-caption font-weight-bold">عتبة ثقة نموذج YOLOv8:</span>
            <v-chip size="x-small" color="success" class="font-weight-black">
              {{ Math.round((omrModel.yolo_conf || 0.35) * 100) }}%
            </v-chip>
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
        </div>
      </div>

      <!-- Alignment Tolerance -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <div class="d-flex justify-space-between align-center mb-2">
          <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
            <v-icon color="warning" size="20">mdi-target</v-icon>
            نسبة التسامح مع انحراف الورقة بالملم
          </label>
          <v-chip size="x-small" color="warning" class="font-weight-black">
            {{ detection.tolerance_mm }} مم
          </v-chip>
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
        <span class="text-caption text-medium-emphasis d-block mt-1">
          أقصى إزاحة هندسية مسموحة لتصحيح المنظور قبل تحويل الورقة للمراجعة اليدوية.
        </span>
      </div>
    </div>

    <!-- Sub-Tab 2: Academic Scoring Policies -->
    <div v-show="activeSubTab === 'scoring_policy'">
      <ScoringPolicySettingsCard :config="config" />
    </div>

    <!-- System Confirmation Alert -->
    <v-alert
      type="success"
      variant="tonal"
      rounded="xl"
      density="compact"
      icon="mdi-check-circle-outline"
      class="text-caption font-weight-bold mt-3"
    >
      كافة الإعدادات والسياسات محفوظة ضمن القالب وتُطبق تلقائياً على محرك التصحيح في السيرفر عند مسح الأوراق.
    </v-alert>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ScoringPolicySettingsCard from './ScoringPolicySettingsCard.vue'

const props = defineProps<{
  config: any
}>()

const activeSubTab = ref<'ai_engine' | 'scoring_policy'>('ai_engine')

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

// Ensure omr_config model object exists
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
