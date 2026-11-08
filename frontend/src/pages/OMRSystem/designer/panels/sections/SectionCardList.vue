<template>
  <div class="pa-4 rounded-xl border bg-surface mb-4">
    <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
      <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
        <v-icon color="info" size="20">mdi-view-headline</v-icon>
        أقسام الاختبار التفصيلية ({{ sectionsList.length }})
      </label>
      <div class="d-flex align-center gap-2">
        <v-btn
          v-if="sectionsList.length > 2 || hasDuplicateSectionTypes"
          size="small"
          variant="tonal"
          color="secondary"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-merge"
          @click="$emit('merge-sections')"
        >
          دمج إلى قسمين (صح/خطأ + متعدد)
        </v-btn>
        <v-btn
          size="small"
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-plus"
          @click="$emit('add-section')"
        >
          إضافة قسم جديد
        </v-btn>
      </div>
    </div>

    <!-- Sections Cards -->
    <div class="d-flex flex-column gap-3">
      <div
        v-for="(sec, idx) in sectionsList"
        :key="sec.id || idx"
        class="pa-3 rounded-lg border bg-surface elevation-0"
      >
        <!-- Section Card Header -->
        <div class="d-flex align-center justify-space-between mb-2">
          <div class="d-flex align-center gap-2">
            <v-chip
              size="x-small"
              :color="sec.type === 'true_false' ? 'info' : 'primary'"
              variant="flat"
              class="font-weight-bold rounded-s"
            >
              القسم {{ idx + 1 }}
            </v-chip>
            <span class="text-caption font-weight-bold">
              (سـ {{ sec.from_q }} إلى سـ {{ sec.to_q }})
            </span>
          </div>

          <div class="d-flex align-center gap-1">
            <v-btn
              icon="mdi-arrow-up"
              size="x-small"
              variant="text"
              :disabled="idx === 0"
              title="تحريك لأعلى"
              @click="$emit('move-section', idx, 'up')"
            />
            <v-btn
              icon="mdi-arrow-down"
              size="x-small"
              variant="text"
              :disabled="idx === sectionsList.length - 1"
              title="تحريك لأسفل"
              @click="$emit('move-section', idx, 'down')"
            />
            <v-btn
              icon="mdi-delete-outline"
              size="x-small"
              variant="text"
              color="error"
              :disabled="sectionsList.length <= 1"
              title="حذف هذا القسم"
              @click="$emit('remove-section', idx)"
            />
          </div>
        </div>

        <!-- Section Controls Row -->
        <v-row dense class="align-center">
          <custom-text-field
            v-model="sec.title"
            label="عنوان القسم"
            icon="format-title"
            cols="12"
            sm="5"
            md="5"
            :hideDetails="true"
            :clearable="false"
          />

          <auto-list
            v-model="sec.type"
            name="ScreenTypeChoices"
            :objects="questionTypeOptions"
            label="نوع الأسئلة"
            placeholder="النوع..."
            cols="6"
            sm="3"
            md="3"
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('change-type', idx, $event)"
          />

          <custom-text-field
            :model-value="getSectionCount(sec)"
            type="number"
            min="1"
            max="100"
            label="العدد"
            icon="numeric"
            cols="3"
            sm="2"
            md="2"
            :hideDetails="true"
            :clearable="false"
            @update:model-value="$emit('update-count', idx, Number($event))"
          />

          <custom-text-field
            v-model.number="sec.mark"
            type="number"
            step="0.5"
            min="0.5"
            label="الدرجة"
            icon="star-circle-outline"
            cols="3"
            sm="2"
            md="2"
            :hideDetails="true"
            :clearable="false"
          />
        </v-row>

        <!-- Section Footer / Summary -->
        <div class="d-flex justify-space-between align-center mt-2 pt-1 border-t text-caption text-medium-emphasis">
          <span>
            خيارات الإجابة:
            <strong class="text-high-emphasis">
              {{ sec.type === 'true_false' ? (config.questions.layout.tf_bubble_type === 'arabic' ? 'ص / خ' : 'صح / خطأ') : (config.questions.layout.bubble_type === 'arabic_letters' ? 'أ، ب، ج، د' : '1، 2، 3، 4') }}
            </strong>
          </span>
          <span>
            إجمالي درجات القسم:
            <strong class="text-primary font-weight-bold">
              {{ getSectionCount(sec) * (sec.mark || 1) }} درجة
            </strong>
          </span>
        </div>
      </div>
    </div>

    <!-- Add Section Button -->
    <v-btn
      color="primary"
      variant="tonal"
      rounded="lg"
      block
      class="font-weight-bold mt-3"
      prepend-icon="mdi-plus-circle-outline"
      @click="$emit('add-section')"
    >
      إضافة قسم جديد
    </v-btn>
  </div>
</template>

<script setup lang="ts">
const questionTypeOptions = [
  { id: 'true_false', value: 'true_false', name: 'صح وخطأ', title: 'صح وخطأ' },
  { id: 'mcq', value: 'mcq', name: 'اختيار من متعدد', title: 'اختيار من متعدد' },
]

defineProps<{
  config: any
  sectionsList: any[]
  hasDuplicateSectionTypes: boolean
  getSectionCount: (sec: any) => number
}>()

defineEmits<{
  (e: 'merge-sections'): void
  (e: 'add-section'): void
  (e: 'remove-section', idx: number): void
  (e: 'move-section', idx: number, direction: 'up' | 'down'): void
  (e: 'change-type', idx: number, type: string): void
  (e: 'update-count', idx: number, count: number): void
}>()
</script>
