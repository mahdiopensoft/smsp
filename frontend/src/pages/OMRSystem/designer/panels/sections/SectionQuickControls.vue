<template>
  <div class="pa-4 rounded-xl border bg-surface mb-4">
    <div class="d-flex align-center justify-space-between mb-3">
      <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
        <v-icon color="primary" size="20">mdi-format-list-numbered-rtl</v-icon>
        هيكلية أقسام الأسئلة (Question Architecture)
      </label>
      <div class="d-flex align-center gap-1">
        <v-chip size="small" color="primary" variant="flat" class="font-weight-bold">
          إجمالي: {{ totalQuestionsCount }} سؤال
        </v-chip>
        <v-chip size="small" color="success" variant="flat" class="font-weight-bold">
          {{ totalExamMarks }} درجة
        </v-chip>
      </div>
    </div>

    <!-- Quick Presets -->
    <div class="d-flex gap-2 flex-wrap mb-3">
      <v-btn
        size="small"
        :variant="totalQuestionsCount === 40 ? 'flat' : 'outlined'"
        :color="totalQuestionsCount === 40 ? 'primary' : 'default'"
        rounded="lg"
        class="font-weight-bold"
        @click="$emit('apply-ministry-40')"
      >
        الوزاري: 20 صح/خطأ + 20 متعدد (40)
      </v-btn>
      <v-btn
        size="small"
        :variant="isYemeniPreset ? 'flat' : 'outlined'"
        :color="isYemeniPreset ? 'primary' : 'default'"
        rounded="lg"
        class="font-weight-bold"
        @click="$emit('apply-ministry-50')"
      >
        الوزاري: 20 صح/خطأ + 30 متعدد (50)
      </v-btn>
      <v-btn
        size="small"
        :variant="totalQuestionsCount === 60 ? 'flat' : 'outlined'"
        :color="totalQuestionsCount === 60 ? 'primary' : 'default'"
        rounded="lg"
        class="font-weight-bold"
        @click="$emit('apply-ministry-60')"
      >
        موسع: 20 صح/خطأ + 40 متعدد (60)
      </v-btn>
      <v-btn
        size="small"
        variant="outlined"
        color="teal"
        rounded="lg"
        class="font-weight-bold"
        @click="$emit('apply-institute-60')"
      >
        معاهد: 20 صح/خطأ + 40 متعدد (60)
      </v-btn>
      <v-btn
        size="small"
        :variant="totalQuestionsCount === 100 ? 'flat' : 'outlined'"
        :color="totalQuestionsCount === 100 ? 'primary' : 'default'"
        rounded="lg"
        class="font-weight-bold"
        @click="$emit('apply-general-100')"
      >
        معياري: 100 متعدد
      </v-btn>
      <v-btn
        size="small"
        :variant="totalQuestionsCount === 180 ? 'flat' : 'outlined'"
        :color="totalQuestionsCount === 180 ? 'primary' : 'default'"
        rounded="lg"
        class="font-weight-bold"
        @click="$emit('apply-university-180')"
      >
        جامعات: 180 متعدد
      </v-btn>
    </div>

    <!-- Quick Steppers for Two Main Section Types (True/False + MCQ) -->
    <div class="pa-3 rounded-lg border bg-surface mb-1">
      <div class="text-caption font-weight-bold text-medium-emphasis mb-2">
        تحكم فوري مباشر بعدد الأسئلة:
      </div>

      <div class="d-flex flex-column gap-3">
        <!-- True/False Quick Controls -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-2">
          <div class="d-flex align-center gap-2">
            <v-icon color="success" size="20">mdi-check-circle-outline</v-icon>
            <div>
              <div class="text-caption font-weight-bold">أسئلة الصواب والخطأ (صح / خطأ)</div>
              <div class="text-caption text-medium-emphasis">
                {{ tfCount }} سؤال ({{ tfCount * (tfSection?.mark || 1) }} درجة)
              </div>
            </div>
          </div>
          <div class="d-flex align-center gap-1">
            <v-btn
              icon="mdi-minus"
              size="x-small"
              variant="outlined"
              color="success"
              :disabled="tfCount <= 0"
              @click="$emit('adjust-tf', -5)"
            />
            <v-text-field
              :model-value="tfCount"
              type="number"
              min="0"
              max="100"
              density="compact"
              hide-details
              variant="outlined"
              class="text-center font-weight-bold"
              style="width: 70px;"
              @update:model-value="$emit('set-tf', Number($event))"
            />
            <v-btn
              icon="mdi-plus"
              size="x-small"
              variant="outlined"
              color="success"
              @click="$emit('adjust-tf', 5)"
            />
          </div>
        </div>

        <!-- MCQ Quick Controls -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-2 border-t pt-2">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-format-list-bulleted</v-icon>
            <div>
              <div class="text-caption font-weight-bold">أسئلة الاختيار من متعدد (MCQ)</div>
              <div class="text-caption text-medium-emphasis">
                {{ mcqCount }} سؤال ({{ mcqCount * (mcqSection?.mark || 2) }} درجة)
              </div>
            </div>
          </div>
          <div class="d-flex align-center gap-1">
            <v-btn
              icon="mdi-minus"
              size="x-small"
              variant="outlined"
              color="primary"
              :disabled="mcqCount <= 0"
              @click="$emit('adjust-mcq', -5)"
            />
            <v-text-field
              :model-value="mcqCount"
              type="number"
              min="0"
              max="200"
              density="compact"
              hide-details
              variant="outlined"
              class="text-center font-weight-bold"
              style="width: 70px;"
              @update:model-value="$emit('set-mcq', Number($event))"
            />
            <v-btn
              icon="mdi-plus"
              size="x-small"
              variant="outlined"
              color="primary"
              @click="$emit('adjust-mcq', 5)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  totalQuestionsCount: number
  totalExamMarks: number
  isYemeniPreset: boolean
  tfCount: number
  mcqCount: number
  tfSection: any
  mcqSection: any
}>()

defineEmits<{
  (e: 'apply-ministry-40'): void
  (e: 'apply-ministry-50'): void
  (e: 'apply-ministry-60'): void
  (e: 'apply-institute-60'): void
  (e: 'apply-general-100'): void
  (e: 'apply-university-180'): void
  (e: 'adjust-tf', delta: number): void
  (e: 'set-tf', val: number): void
  (e: 'adjust-mcq', delta: number): void
  (e: 'set-mcq', val: number): void
}>()
</script>
