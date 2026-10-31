<template>
  <div class="section-layout-settings">
    <!-- Columns Count -->
    <div class="pa-4 rounded-xl border bg-surface mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">عدد الأعمدة الهندسية (Columns Count)</label>
        <v-chip size="small" color="info" variant="flat" class="font-weight-bold">
          {{ config.questions.layout.columns_count }} أعمدة
        </v-chip>
      </div>
      <v-btn-toggle
        v-model="config.questions.layout.columns_count"
        mandatory
        color="primary"
        variant="outlined"
        rounded="lg"
        grow
        class="w-100"
      >
        <v-btn :value="2" class="font-weight-bold">2 عمود</v-btn>
        <v-btn :value="3" class="font-weight-bold">3 أعمدة</v-btn>
        <v-btn :value="4" class="font-weight-bold">4 أعمدة (المعتمد)</v-btn>
        <v-btn :value="5" class="font-weight-bold">5 أعمدة</v-btn>
      </v-btn-toggle>
    </div>

    <!-- Row Spacing Slider -->
    <div class="pa-4 rounded-xl border bg-surface mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">التباعد الرأسي بين الأسئلة (Row Spacing)</label>
        <div class="d-flex align-center gap-2">
          <v-chip size="small" color="primary" variant="flat" class="font-weight-bold">
            {{ config.questions.layout.row_spacing_mm }} mm
          </v-chip>
          <v-btn size="x-small" variant="tonal" color="info" rounded="lg" class="font-weight-bold" @click="$emit('auto-fit-spacing')">
            ملاءمة تلقائية
          </v-btn>
        </div>
      </div>
      <v-slider
        v-model="config.questions.layout.row_spacing_mm"
        :min="3.6"
        :max="6.5"
        :step="0.1"
        color="primary"
        thumb-label
        hide-details
      />
    </div>

    <!-- Bubble Radius Slider -->
    <div class="pa-4 rounded-xl border bg-surface mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">نصف قطر الدائرة (Bubble Radius)</label>
        <v-chip size="small" color="primary" variant="flat" class="font-weight-bold">
          {{ config.questions.layout.bubble_radius_mm }} mm
        </v-chip>
      </div>
      <v-slider
        v-model="config.questions.layout.bubble_radius_mm"
        :min="1.4"
        :max="2.4"
        :step="0.1"
        color="primary"
        thumb-label
        hide-details
      />
    </div>

    <!-- MCQ Choice Labels Format -->
    <div class="pa-4 rounded-xl border bg-surface mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">نمط خيارات الاختيار من متعدد (MCQ)</label>
        <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
          {{ config.questions.layout.bubble_type === 'arabic_letters' ? 'عربي (أ، ب، ج، د)' : (config.questions.layout.bubble_type === 'letters' ? 'إنجليزي (A, B, C, D)' : 'أرقام (1, 2, 3, 4)') }}
        </v-chip>
      </div>
      <v-btn-toggle
        v-model="config.questions.layout.bubble_type"
        mandatory
        color="primary"
        variant="outlined"
        rounded="lg"
        grow
        class="w-100"
      >
        <v-btn value="numbers" class="font-weight-bold">أرقام (1, 2, 3, 4)</v-btn>
        <v-btn value="arabic_letters" class="font-weight-bold">عربي (أ، ب، ج، د)</v-btn>
        <v-btn value="letters" class="font-weight-bold">إنجليزي (A, B, C, D)</v-btn>
      </v-btn-toggle>
    </div>

    <!-- True / False Choice Scheme -->
    <div class="pa-4 rounded-xl border bg-surface mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">نمط خيارات الصواب والخطأ (True / False)</label>
        <v-chip size="small" color="success" variant="tonal" class="font-weight-bold">
          {{ config.questions.layout.tf_bubble_type === 'english' ? 'T / F' : (config.questions.layout.tf_bubble_type === 'symbols' ? '✓ / ✗' : (config.questions.layout.tf_bubble_type === 'arabic_words' ? 'صح / خطأ' : 'ص / خ')) }}
        </v-chip>
      </div>
      <v-btn-toggle
        v-model="config.questions.layout.tf_bubble_type"
        mandatory
        color="success"
        variant="outlined"
        rounded="lg"
        grow
        class="w-100"
      >
        <v-btn value="arabic" class="font-weight-bold">عربي (ص / خ)</v-btn>
        <v-btn value="arabic_words" class="font-weight-bold">كلمات (صح / خطأ)</v-btn>
        <v-btn value="english" class="font-weight-bold">إنجليزي (T / F)</v-btn>
        <v-btn value="symbols" class="font-weight-bold">رموز (✓ / ✗)</v-btn>
      </v-btn-toggle>
    </div>

    <!-- Choices Count per Question -->
    <div class="pa-4 rounded-xl border bg-surface">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">عدد خيارات أسئلة الاختيار من متعدد</label>
        <v-chip size="small" color="info" variant="flat" class="font-weight-bold">
          {{ config.questions.layout.choices_count || 4 }} خيارات
        </v-chip>
      </div>
      <v-btn-toggle
        v-model="config.questions.layout.choices_count"
        mandatory
        color="info"
        variant="outlined"
        rounded="lg"
        grow
        class="w-100"
      >
        <v-btn :value="4" class="font-weight-bold">4 خيارات (المعتمد)</v-btn>
        <v-btn :value="5" class="font-weight-bold">5 خيارات</v-btn>
        <v-btn :value="3" class="font-weight-bold">3 خيارات</v-btn>
      </v-btn-toggle>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  config: any
}>()

defineEmits<{
  (e: 'auto-fit-spacing'): void
}>()
</script>
