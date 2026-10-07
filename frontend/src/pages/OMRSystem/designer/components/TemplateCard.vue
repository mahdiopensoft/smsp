<template>
  <v-card class="template-card rounded-xl border elevation-0 h-100 d-flex flex-column overflow-hidden">
    <!-- ── Card Top Thumbnail View ─────────────────────────────────── -->
    <div
      class="template-thumb-box position-relative overflow-hidden cursor-pointer"
      @click="emit('preview', template)"
    >
      <!-- Simulated Paper Sheet Container with Drop Shadow -->
      <div class="paper-preview-wrapper">
        <div class="thumb-scaler">
          <YemeniMinistrySheet
            v-if="isYemeniMinistryPreset"
            :exam-subject="template.template_data?.header?.exam_name || template.name"
            :exam-year="template.template_data?.metadata?.academic_year || '1444هـ — 2022-2023م'"
          />
          <OmrSheetMultigraphics
            v-else
            :total-questions="questionsCount"
            :questions-per-column="questionsPerColumn"
            :total-columns="columnsCount"
            :choices-per-question="choicesCount"
            :primary-color="primaryColor"
            :institution-name="template.template_data?.header?.institution_name || template.name || 'نموذج اختبار معياري'"
            :sub-title="template.template_data?.header?.sub_title || template.description || 'ورقة إجابة التصحيح الضوئي'"
            :exam-name="template.template_data?.header?.exam_name || template.name"
          />
        </div>
      </div>

      <!-- Hover Overlay (Frosted Glass & Quick Full Preview Button) -->
      <div class="thumb-overlay">
        <v-btn
          color="white"
          variant="flat"
          size="small"
          rounded="lg"
          prepend-icon="mdi-eye-outline"
          class="font-weight-bold text-primary elevation-2"
          @click.stop="emit('preview', template)"
        >
          معاينة كاملة
        </v-btn>
      </div>

      <!-- Top Badges (Unified 6px Border Radius) -->
      <div class="position-absolute top-0 end-0 pa-2 d-flex gap-1 z-index-2">
        <v-chip
          v-if="isYemeniMinistryPreset"
          size="x-small"
          color="primary"
          variant="flat"
          class="font-weight-bold unified-badge shadow-sm"
        >
          <v-icon start size="12">mdi-check-decagram</v-icon>
          رسمي — وزارة التربية
        </v-chip>
        <v-chip
          v-else-if="isUniversityPreset"
          size="x-small"
          color="indigo"
          variant="flat"
          class="font-weight-bold unified-badge shadow-sm"
        >
          <v-icon start size="12">mdi-domain</v-icon>
          نموذج جامعي
        </v-chip>
        <v-chip
          v-else
          size="x-small"
          color="blue-grey-darken-1"
          variant="flat"
          class="font-weight-bold unified-badge shadow-sm"
        >
          <v-icon start size="12">mdi-tune-variant</v-icon>
          قالب مخصص
        </v-chip>

        <v-chip
          size="x-small"
          color="surface"
          variant="flat"
          class="font-weight-bold unified-badge shadow-sm border text-medium-emphasis"
        >
          v{{ template.version || '1.0' }}
        </v-chip>
      </div>

      <!-- Paper Size Tag (Bottom Start of Thumbnail) -->
      <div class="position-absolute bottom-0 start-0 pa-2 z-index-2">
        <v-chip
          size="x-small"
          variant="flat"
          color="rgba(15, 23, 42, 0.72)"
          class="text-white font-weight-bold unified-badge"
        >
          <v-icon start size="11">mdi-file-document-outline</v-icon>
          {{ paperSize }}
        </v-chip>
      </div>
    </div>

    <!-- ── Card Details ────────────────────────────────────────────── -->
    <v-card-text class="pa-4 flex-grow-1 d-flex flex-column justify-space-between">
      <div>
        <!-- Title and ID -->
        <div class="d-flex align-start justify-space-between gap-2 mb-1">
          <h3 class="text-subtitle-1 font-weight-black text-on-surface line-clamp-1 mb-0" :title="template.name">
            {{ template.name }}
          </h3>
          <span class="text-caption text-disabled font-weight-mono">#{{ template.id }}</span>
        </div>

        <p class="text-caption text-medium-emphasis mb-3 line-clamp-2" style="min-height: 36px; line-height: 1.5;">
          {{ template.description || 'قالب اختبار معياري مخصص للتصحيح الآلي عالي الدقة 300 DPI' }}
        </p>

        <!-- Template Specs Grid (Unified 6px Border Radius Chips) -->
        <div class="specs-grid d-flex gap-2 flex-wrap mb-2">
          <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold unified-spec-chip">
            <v-icon start size="13">mdi-help-circle-outline</v-icon>
            {{ questionsCount }} سؤال
          </v-chip>
          <v-chip size="x-small" variant="tonal" color="info" class="font-weight-bold unified-spec-chip">
            <v-icon start size="13">mdi-view-column-outline</v-icon>
            {{ columnsCount }} أعمدة
          </v-chip>
          <v-chip size="x-small" variant="tonal" color="success" class="font-weight-bold unified-spec-chip">
            <v-icon start size="13">mdi-checkbox-marked-circle-outline</v-icon>
            {{ choicesCount }} خيارات
          </v-chip>
          <v-chip v-if="choicesCount === 2" size="x-small" variant="tonal" color="warning" class="font-weight-bold unified-spec-chip">
            <v-icon start size="13">mdi-check-all</v-icon>
            صح / خطأ
          </v-chip>
        </div>
      </div>

      <!-- Card Actions Footer -->
      <div class="pt-3 border-t d-flex align-center justify-space-between gap-2">
        <v-btn
          color="primary"
          variant="tonal"
          size="small"
          rounded="lg"
          class="font-weight-bold flex-grow-1"
          prepend-icon="mdi-pencil-outline"
          @click="emit('edit', template)"
        >
          تعديل
        </v-btn>
        <v-btn
          color="success"
          size="small"
          rounded="lg"
          class="font-weight-bold flex-grow-1 elevation-1"
          prepend-icon="mdi-scanner"
          @click="emit('scan', template.id)"
        >
          تصحيح
        </v-btn>
        <v-menu location="bottom end">
          <template v-slot:activator="{ props }">
            <v-btn icon size="small" variant="tonal" color="grey-darken-1" rounded="lg" v-bind="props">
              <v-icon size="18">mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list density="compact" rounded="lg" elevation="3" min-width="160">
            <v-list-item prepend-icon="mdi-eye-outline" title="معاينة الورقة" @click="emit('preview', template)" />
            <v-list-item prepend-icon="mdi-content-copy" title="نسخ كقالب جديد" @click="emit('duplicate', template)" />
            <v-list-item prepend-icon="mdi-printer-outline" title="طباعة فورية" @click="emit('print', template)" />
            <v-list-item prepend-icon="mdi-download-outline" title="تصدير ملف القالب" @click="downloadTemplateJson" />
            <v-divider class="my-1" />
            <v-list-item
              prepend-icon="mdi-delete-outline"
              title="حذف القالب"
              class="text-error"
              @click="emit('delete', template)"
            />
          </v-list>
        </v-menu>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'

const props = defineProps<{
  template: any
}>()

const emit = defineEmits<{
  (e: 'edit', t: any): void
  (e: 'scan', id: number | string): void
  (e: 'preview', t: any): void
  (e: 'duplicate', t: any): void
  (e: 'print', t: any): void
  (e: 'delete', t: any): void
}>()

const OmrSheetMultigraphics = defineAsyncComponent(() =>
  import('@/components/omr_templates/OmrSheetMultigraphics.vue')
)

const YemeniMinistrySheet = defineAsyncComponent(() =>
  import('@/components/omr_templates/YemeniMinistrySheet.vue')
)

const questionsCount = computed(() => {
  const t = props.template
  return (
    t?.total_mcq ||
    t?.template_data?.questions?.metadata?.num_questions ||
    t?.template_data?.metadata?.num_questions ||
    0
  )
})

const isYemeniMinistryPreset = computed(() => {
  const name = props.template?.name || ''
  const tId = props.template?.template_data?.template_id || ''
  const numQ = questionsCount.value
  return (
    name.includes('وزارة التربية') ||
    name.includes('الثانوية العامة') ||
    tId === 'YEMEN_MINISTRY_50' ||
    numQ === 50
  )
})

const isUniversityPreset = computed(() => {
  const name = props.template?.name || ''
  const numQ = questionsCount.value
  return numQ === 180 || name.includes('الجامعات') || name.includes('التعليم العالي')
})

const columnsCount = computed(() => {
  const t = props.template
  return (
    t?.template_data?.questions?.layout?.columns_count ||
    t?.template_data?.metadata?.columns_count ||
    t?.template_data?.layout?.columns_count ||
    4
  )
})

const questionsPerColumn = computed(() => {
  return Math.ceil(questionsCount.value / columnsCount.value)
})

const choicesCount = computed(() => {
  const t = props.template
  return (
    t?.template_data?.questions?.layout?.choices_count ||
    t?.template_data?.metadata?.choices_count ||
    t?.template_data?.layout?.choices_count ||
    4
  )
})

const primaryColor = computed(() => {
  return props.template?.template_data?.header?.primary_color || '#e6007e'
})

const paperSize = computed(() => {
  return (
    props.template?.template_data?.paper?.size ||
    props.template?.template_data?.metadata?.paper_size ||
    (questionsCount.value > 100 ? 'A3' : (questionsCount.value <= 40 ? 'A5' : 'A4'))
  )
})

function downloadTemplateJson() {
  const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(props.template, null, 2))
  const downloadAnchor = document.createElement('a')
  downloadAnchor.setAttribute('href', dataStr)
  downloadAnchor.setAttribute('download', `template_${props.template.id || 'omr'}_manifest.json`)
  document.body.appendChild(downloadAnchor)
  downloadAnchor.click()
  downloadAnchor.remove()
}
</script>

<style scoped>
.template-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease;
}
.template-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.08), 0 4px 12px -2px rgba(0, 0, 0, 0.04) !important;
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
}

.template-thumb-box {
  height: 200px;
  background-color: #f8fafc;
  background-image: radial-gradient(rgba(148, 163, 184, 0.35) 1px, transparent 1px);
  background-size: 14px 14px;
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 12px;
}

.paper-preview-wrapper {
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  display: flex;
  justify-content: center;
}

.thumb-scaler {
  transform: scale(0.22);
  transform-origin: top center;
  width: 210mm;
  margin: 0 auto;
  pointer-events: none;
}

.thumb-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(3px);
  opacity: 0;
  transition: opacity 0.25s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.template-thumb-box:hover .thumb-overlay {
  opacity: 1;
}

.unified-badge {
  border-radius: 6px !important;
}

.unified-spec-chip {
  border-radius: 6px !important;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.font-weight-mono {
  font-family: monospace;
}
</style>
