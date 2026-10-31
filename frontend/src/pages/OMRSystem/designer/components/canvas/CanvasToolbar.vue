<template>
  <div class="canvas-toolbar pa-3 px-4 rounded-xl border bg-surface mb-3 d-flex justify-space-between align-center flex-wrap gap-2 elevation-1">
    <div class="d-flex align-center gap-2 flex-wrap">
      <!-- View Mode -->
      <v-btn-toggle
        :model-value="zoomMode"
        mandatory
        density="compact"
        color="primary"
        variant="outlined"
        rounded="lg"
        class="me-1"
        @update:model-value="$emit('update:zoomMode', $event)"
      >
        <v-btn value="fit" size="small" class="font-weight-bold" prepend-icon="mdi-fit-to-screen-outline">
          ملاءمة الصفحة
        </v-btn>
        <v-btn value="actual" size="small" class="font-weight-bold" prepend-icon="mdi-image-size-select-actual">
          الحجم الفعلي 100%
        </v-btn>
      </v-btn-toggle>

      <!-- Proportional Zoom -->
      <div class="d-flex align-center rounded-lg px-1 border" style="background: rgba(var(--v-theme-surface-variant), 0.3);">
        <v-btn icon size="small" variant="text" :disabled="zoomLevel <= 0.4" @click="$emit('zoom-out')">
          <v-icon size="18">mdi-magnify-minus-outline</v-icon>
        </v-btn>
        <span class="text-caption font-weight-bold px-2 font-mono" style="min-width: 44px; text-align: center;">
          {{ Math.round(currentZoomDisplay * 100) }}%
        </span>
        <v-btn icon size="small" variant="text" :disabled="zoomLevel >= 3.0" @click="$emit('zoom-in')">
          <v-icon size="18">mdi-magnify-plus-outline</v-icon>
        </v-btn>
        <v-btn icon size="small" variant="text" title="إعادة ضبط" @click="$emit('reset-zoom')">
          <v-icon size="16">mdi-refresh</v-icon>
        </v-btn>
      </div>

      <!-- Shading Simulator Buttons -->
      <v-btn
        size="small"
        variant="tonal"
        color="info"
        rounded="lg"
        class="font-weight-bold"
        prepend-icon="mdi-dice-5-outline"
        @click="$emit('random-shade')"
      >
        تظليل تجريبي
      </v-btn>
      <v-btn
        v-if="hasSimulatedAnswers"
        size="small"
        variant="text"
        color="error"
        rounded="lg"
        class="font-weight-bold"
        prepend-icon="mdi-delete-sweep-outline"
        @click="$emit('clear-shade')"
      >
        مسح
      </v-btn>

      <!-- Presentation / Layout Mode Switcher -->
      <v-btn-toggle
        :model-value="presentationMode"
        mandatory
        density="compact"
        color="primary"
        variant="flat"
        rounded="lg"
        class="ms-2"
        @update:model-value="$emit('update:presentationMode', $event)"
      >
        <v-btn value="audit_a4" size="small" class="font-weight-bold" prepend-icon="mdi-file-document-check-outline">
          النموذج الرسمي الشامل (A4 المعتمد)
        </v-btn>
        <v-btn value="compact_a5" size="small" class="font-weight-bold" prepend-icon="mdi-file-outline">
          ورقة إجابة الطالب (A5 للاختبار)
        </v-btn>
        <v-btn value="university_180" size="small" class="font-weight-bold" prepend-icon="mdi-school-outline">
          نموذج الجامعات (180 سؤال)
        </v-btn>
      </v-btn-toggle>
    </div>

    <div class="d-flex align-center gap-2">
      <v-btn
        color="success"
        size="small"
        rounded="lg"
        class="font-weight-bold"
        prepend-icon="mdi-content-save"
        @click="$emit('save')"
      >
        حفظ القالب
      </v-btn>
      <v-btn
        variant="tonal"
        color="indigo"
        size="small"
        rounded="lg"
        class="font-weight-bold"
        prepend-icon="mdi-code-json"
        @click="$emit('export-json')"
      >
        تصدير JSON
      </v-btn>
      <v-btn
        variant="tonal"
        color="secondary"
        size="small"
        rounded="lg"
        class="font-weight-bold"
        prepend-icon="mdi-printer"
        @click="$emit('print')"
      >
        طباعة
      </v-btn>
      <v-btn
        color="primary"
        size="small"
        rounded="lg"
        class="font-weight-bold"
        prepend-icon="mdi-download"
        @click="$emit('export-png')"
      >
        تنزيل PNG عالية الدقة
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  zoomMode: 'fit' | 'actual' | 'custom'
  zoomLevel: number
  currentZoomDisplay: number
  presentationMode: 'audit_a4' | 'compact_a5' | 'university_180'
  hasSimulatedAnswers: boolean
}>()

defineEmits<{
  (e: 'update:zoomMode', val: 'fit' | 'actual' | 'custom'): void
  (e: 'update:presentationMode', val: 'audit_a4' | 'compact_a5' | 'university_180'): void
  (e: 'zoom-in'): void
  (e: 'zoom-out'): void
  (e: 'reset-zoom'): void
  (e: 'random-shade'): void
  (e: 'clear-shade'): void
  (e: 'save'): void
  (e: 'export-json'): void
  (e: 'print'): void
  (e: 'export-png'): void
}>()
</script>
