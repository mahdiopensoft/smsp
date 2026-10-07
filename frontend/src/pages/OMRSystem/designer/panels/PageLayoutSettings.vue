<template>
  <div class="page-layout-settings">
    <!-- Preset Template Selector -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">النموذج القياسي المعتمد (Preset Pattern)</label>
        <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">موصى به</v-chip>
      </div>
      <v-select
        v-model="selectedPreset"
        :items="presets"
        item-title="title"
        item-value="id"
        variant="outlined"
        density="comfortable"
        rounded="lg"
        hide-details
        @update:model-value="onPresetChange"
      >
        <template v-slot:item="{ props, item }">
          <v-list-item v-bind="props" :subtitle="item.raw.subtitle" />
        </template>
      </v-select>
    </div>

    <!-- Document Output & Layout Mode (For Yemeni Ministry 50) -->
    <div v-if="isYemeniPreset" class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">نوع مخرج ونموذج الورقة المعيارية</label>
        <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">تنسيق مخصص</v-chip>
      </div>
      <v-btn-toggle
        v-model="config.display_mode"
        mandatory
        color="primary"
        variant="outlined"
        rounded="lg"
        grow
        class="w-100 mb-2 flex-column"
        style="height: auto;"
      >
        <v-btn value="audit_a4" class="font-weight-bold justify-start py-2">
          <v-icon start size="18" color="success">mdi-file-document-check-outline</v-icon>
          النموذج الرسمي الشامل المعتمد (A4 مع الترويسة والتدقيق والمطابقة)
        </v-btn>
        <v-btn value="compact_a5" class="font-weight-bold justify-start py-2">
          <v-icon start size="18" color="info">mdi-file-outline</v-icon>
          ورقة إجابة الطالب المطبوعة للاختبار (A5 المعيارية 210×148.5)
        </v-btn>
      </v-btn-toggle>
      <span class="text-caption text-medium-emphasis d-block mt-1">
        {{ config.display_mode === 'audit_a4' ? 'الوثيقة الرسمية الشاملة المعتمدة بكنترول الوزارة: ترويسة علوية + ورقة الإجابة + مصفوفة تدقيق الـ 80 درجة وتذييل النظام.' : 'المقاس الورقي المعياري المطبوع والموزع على الطلاب في قاعات الامتحانات (210×148.5 مم).' }}
      </span>
    </div>

    <!-- Paper Size & Dimensions -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <label class="text-subtitle-2 font-weight-bold mb-2 d-block">مقاس الورقة القياسي</label>
      <v-btn-toggle
        v-model="config.paper.size"
        mandatory
        color="primary"
        variant="outlined"
        rounded="lg"
        grow
        class="w-100 mb-3"
        @update:model-value="onPaperSizeChange"
      >
        <v-btn value="A4" class="font-weight-bold">A4 (210×297)</v-btn>
        <v-btn value="A5" class="font-weight-bold">A5 (210×148.5)</v-btn>
        <v-btn value="A3" class="font-weight-bold">A3</v-btn>
        <v-btn value="Letter" class="font-weight-bold">Letter</v-btn>
      </v-btn-toggle>

      <v-row dense>
        <v-col cols="6">
          <v-text-field
            v-model.number="config.paper.width_mm"
            label="العرض (مم)"
            type="number"
            variant="outlined"
            density="compact"
            rounded="lg"
            hide-details
            disabled
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model.number="config.paper.height_mm"
            label="الارتفاع (مم)"
            type="number"
            variant="outlined"
            density="compact"
            rounded="lg"
            hide-details
            disabled
          />
        </v-col>
      </v-row>
    </div>

    <!-- Target Print DPI & Colors -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">دقة المسح الضوئي والطباعة</label>
        <v-chip size="small" color="success" variant="tonal" class="font-weight-bold">
          {{ config.paper.dpi || 300 }} DPI معتمد
        </v-chip>
      </div>
      <p class="text-caption text-medium-emphasis mb-3">
        تضمن دقة 300 DPI قراءة واضحة للباركود ولعلامات الزوايا وتجنب أخطاء الميلان.
      </p>

      <label class="text-subtitle-2 font-weight-bold mb-2 d-block">اللون المعياري للطباعة</label>
      <div class="d-flex gap-2 align-center flex-wrap">
        <div
          v-for="color in themeColors"
          :key="color.hex"
          class="color-swatch rounded-lg cursor-pointer border"
          :style="{ backgroundColor: color.hex, width: '36px', height: '36px' }"
          :class="{ 'active-swatch': config.header.primary_color === color.hex }"
          :title="color.label"
          @click="config.header.primary_color = color.hex"
        />
      </div>
    </div>

    <!-- Direction -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5">
      <label class="text-subtitle-2 font-weight-bold mb-2 d-block">اتجاه القراءة وترتيب الأعمدة</label>
      <v-btn-toggle
        v-model="config.questions.layout.layout_direction"
        mandatory
        color="primary"
        variant="outlined"
        rounded="lg"
        grow
        class="w-100"
      >
        <v-btn value="rtl" class="font-weight-bold">من اليمين لليسار (RTL - عربي)</v-btn>
        <v-btn value="ltr" class="font-weight-bold">من اليسار لليمين (LTR)</v-btn>
      </v-btn-toggle>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps<{
  config: any
}>()

const emit = defineEmits<{
  (e: 'preset-selected', presetId: string): void
}>()

const selectedPreset = ref(props.config?.template_id || 'YEMEN_MINISTRY_50')

watch(() => props.config?.template_id, (newId) => {
  if (newId) selectedPreset.value = newId
})

const isYemeniPreset = computed(() => {
  const tId = props.config?.template_id || ''
  const name = props.config?.template_name || ''
  return tId === 'YEMEN_MINISTRY_50' || name.includes('وزارة التربية') || name.includes('الثانوية العامة') || props.config?.questions?.metadata?.num_questions === 50
})

const presets = [
  {
    id: 'YEMEN_MINISTRY_40',
    title: 'نموذج وزارة التربية والتعليم اليمنية (40 سؤال)',
    subtitle: '20 سؤال صح/خطأ + 20 سؤال اختيار متعدد (المعتمد في الشهادة الثانوية)',
  },
  {
    id: 'YEMEN_MINISTRY_50',
    title: 'نموذج وزارة التربية والتعليم اليمنية (50 سؤال هجين)',
    subtitle: '20 سؤال صح/خطأ + 30 سؤال اختيار متعدد + بطاقة بيانات الطالب والباركودات',
  },
  {
    id: 'YEMEN_MINISTRY_60',
    title: 'نموذج وزارة التربية والتعليم اليمنية (60 سؤال موسع)',
    subtitle: '20 سؤال صح/خطأ + 40 سؤال اختيار متعدد',
  },
  {
    id: 'YEMEN_UNIVERSITY_180',
    title: 'نموذج الجامعات اليمنية العام (180 سؤال - 4 أعمدة)',
    subtitle: 'اختبارات القبول والمقررات الشاملة في جامعة صنعاء والجامعات الحكومية',
  },
  {
    id: 'GENERAL_100',
    title: 'النموذج المعياري العام (100 سؤال)',
    subtitle: 'مناسب للمدارس والمعاهد والامتحانات النصفية والفصلية',
  },
]

const themeColors = [
  { hex: '#000000', label: 'أسود معتمد (وزارة التربية)' },
  { hex: '#e6007e', label: 'وردي أمني (جامعة صنعاء)' },
  { hex: '#1e40af', label: 'أزرق ملكي' },
  { hex: '#047857', label: 'أخضر معتمد' },
  { hex: '#b91c1c', label: 'أحمر داكن' },
]

function onPresetChange(presetId: string) {
  emit('preset-selected', presetId)
}

watch(() => props.config?.display_mode, (mode) => {
  if (!props.config?.paper) return
  if (mode === 'compact_a5') {
    props.config.paper.size = 'A5'
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 148.5
    props.config.paper.orientation = 'landscape'
  } else if (mode === 'audit_a4') {
    props.config.paper.size = 'A4'
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 297
    props.config.paper.orientation = 'portrait'
  }
})

function onPaperSizeChange(size: string) {
  if (size === 'A4') {
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 297
    props.config.display_mode = 'audit_a4'
  } else if (size === 'A5') {
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 148.5
    props.config.display_mode = 'compact_a5'
  } else if (size === 'A3') {
    props.config.paper.width_mm = 297
    props.config.paper.height_mm = 420
  } else if (size === 'Letter') {
    props.config.paper.width_mm = 216
    props.config.paper.height_mm = 279
  }
}
</script>

<style scoped>
.color-swatch {
  transition: transform 0.15s ease, border-color 0.15s ease;
}
.color-swatch:hover {
  transform: scale(1.1);
}
.active-swatch {
  border: 3px solid #3b82f6 !important;
  transform: scale(1.15);
}
</style>
