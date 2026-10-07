<template>
  <div class="sections-manager">
    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. Question Architecture Overview & Live Summary               -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
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
          @click="applyMinistry40"
        >
          الوزاري: 20 صح/خطأ + 20 متعدد (40)
        </v-btn>
        <v-btn
          size="small"
          :variant="isYemeniPreset ? 'flat' : 'outlined'"
          :color="isYemeniPreset ? 'primary' : 'default'"
          rounded="lg"
          class="font-weight-bold"
          @click="applyYemeniMinistry50"
        >
          الوزاري: 20 صح/خطأ + 30 متعدد (50)
        </v-btn>
        <v-btn
          size="small"
          :variant="totalQuestionsCount === 60 ? 'flat' : 'outlined'"
          :color="totalQuestionsCount === 60 ? 'primary' : 'default'"
          rounded="lg"
          class="font-weight-bold"
          @click="applyMinistry60"
        >
          موسع: 20 صح/خطأ + 40 متعدد (60)
        </v-btn>
        <v-btn
          size="small"
          :variant="totalQuestionsCount === 100 ? 'flat' : 'outlined'"
          :color="totalQuestionsCount === 100 ? 'primary' : 'default'"
          rounded="lg"
          class="font-weight-bold"
          @click="applyGeneral100"
        >
          معياري: 100 متعدد
        </v-btn>
        <v-btn
          size="small"
          :variant="totalQuestionsCount === 180 ? 'flat' : 'outlined'"
          :color="totalQuestionsCount === 180 ? 'primary' : 'default'"
          rounded="lg"
          class="font-weight-bold"
          @click="applyUniversity180"
        >
          جامعات: 180 متعدد
        </v-btn>
      </div>

      <!-- Quick Steppers for Two Main Section Types (True/False + MCQ) -->
      <div class="pa-3 rounded-lg border bg-surface mb-3">
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
                @click="adjustTfCount(-5)"
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
                @update:model-value="setTfCount(Number($event))"
              />
              <v-btn
                icon="mdi-plus"
                size="x-small"
                variant="outlined"
                color="success"
                @click="adjustTfCount(5)"
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
                @click="adjustMcqCount(-5)"
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
                @update:model-value="setMcqCount(Number($event))"
              />
              <v-btn
                icon="mdi-plus"
                size="x-small"
                variant="outlined"
                color="primary"
                @click="adjustMcqCount(5)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 2. Detailed Sections List (Add / Edit / Delete / Reorder)       -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
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
            @click="mergeToStandardTwoSections"
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
            @click="addNewSection"
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
                :color="sec.type === 'true_false' ? 'success' : 'primary'"
                variant="flat"
                class="font-weight-bold"
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
                @click="moveSection(idx, 'up')"
              />
              <v-btn
                icon="mdi-arrow-down"
                size="x-small"
                variant="text"
                :disabled="idx === sectionsList.length - 1"
                title="تحريك لأسفل"
                @click="moveSection(idx, 'down')"
              />
              <v-btn
                icon="mdi-delete-outline"
                size="x-small"
                variant="text"
                color="error"
                :disabled="sectionsList.length <= 1"
                title="حذف هذا القسم"
                @click="removeSection(idx)"
              />
            </div>
          </div>

          <!-- Section Controls Row -->
          <v-row dense class="align-center">
            <!-- Title -->
            <v-col cols="12" sm="5">
              <v-text-field
                v-model="sec.title"
                label="عنوان القسم"
                density="compact"
                hide-details
                variant="outlined"
              />
            </v-col>

            <!-- Type -->
            <v-col cols="6" sm="3">
              <v-select
                v-model="sec.type"
                :items="[
                  { title: 'صح وخطأ', value: 'true_false' },
                  { title: 'اختيار من متعدد', value: 'mcq' }
                ]"
                label="نوع الأسئلة"
                density="compact"
                hide-details
                variant="outlined"
                @update:model-value="onSectionTypeChange(idx, $event)"
              />
            </v-col>

            <!-- Question Count in Section -->
            <v-col cols="6" sm="2">
              <v-text-field
                :model-value="getSectionCount(sec)"
                type="number"
                min="1"
                max="100"
                label="العدد"
                density="compact"
                hide-details
                variant="outlined"
                @update:model-value="updateSectionCount(idx, Number($event))"
              />
            </v-col>

            <!-- Mark per question -->
            <v-col cols="12" sm="2">
              <v-text-field
                v-model.number="sec.mark"
                type="number"
                step="0.5"
                min="0.5"
                label="الدرجة"
                density="compact"
                hide-details
                variant="outlined"
              />
            </v-col>
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
        @click="addNewSection"
      >
        إضافة قسم جديد
      </v-btn>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 3. Layout Columns & Sizing                                     -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
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
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">التباعد الرأسي بين الأسئلة (Row Spacing)</label>
        <div class="d-flex align-center gap-2">
          <v-chip size="small" color="primary" variant="flat" class="font-weight-bold">
            {{ config.questions.layout.row_spacing_mm }} mm
          </v-chip>
          <v-btn size="x-small" variant="tonal" color="info" rounded="lg" class="font-weight-bold" @click="autoFitRowSpacing">
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
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
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
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
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
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
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
    <div class="pa-4 rounded-xl border bg-grey-lighten-5">
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
import { computed } from 'vue'

const props = defineProps<{
  config: any
}>()

function ensureSections() {
  if (!props.config.questions.sections || !Array.isArray(props.config.questions.sections) || props.config.questions.sections.length === 0) {
    props.config.questions.sections = [
      { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 50, choices: ['1', '2', '3', '4'], mark: 2 },
    ]
  }
}

const sectionsList = computed(() => {
  ensureSections()
  return props.config.questions.sections
})

const totalQuestionsCount = computed(() => {
  ensureSections()
  const secs = props.config.questions.sections
  if (!secs || secs.length === 0) return 50
  const lastSec = secs[secs.length - 1]
  return lastSec.to_q || 50
})

const totalExamMarks = computed(() => {
  ensureSections()
  let sum = 0
  for (const sec of props.config.questions.sections) {
    const count = getSectionCount(sec)
    const mark = sec.mark || 1
    sum += count * mark
  }
  return sum
})

const isYemeniPreset = computed(() => {
  return totalQuestionsCount.value === 50 && tfCount.value === 20 && mcqCount.value === 30
})

function getSectionCount(sec: any): number {
  if (!sec) return 0
  const from = sec.from_q || 1
  const to = sec.to_q || from
  return Math.max(1, to - from + 1)
}

const tfCount = computed(() => {
  ensureSections()
  return props.config.questions.sections
    .filter((s: any) => s.type === 'true_false')
    .reduce((sum: number, s: any) => sum + getSectionCount(s), 0)
})

const mcqCount = computed(() => {
  ensureSections()
  return props.config.questions.sections
    .filter((s: any) => s.type === 'mcq')
    .reduce((sum: number, s: any) => sum + getSectionCount(s), 0)
})

const hasDuplicateSectionTypes = computed(() => {
  ensureSections()
  const types = props.config.questions.sections.map((s: any) => s.type)
  return new Set(types).size !== types.length
})

function mergeToStandardTwoSections() {
  ensureSections()
  const totalTf = tfCount.value
  const totalMcq = mcqCount.value
  const newSections: any[] = []

  if (totalTf > 0) {
    newSections.push({
      id: 'sec_tf',
      title: 'أسئلة الصواب والخطأ',
      type: 'true_false',
      from_q: 1,
      to_q: totalTf,
      choices: ['صح', 'خطأ'],
      mark: 1,
    })
  }

  if (totalMcq > 0) {
    const startMcq = totalTf + 1
    newSections.push({
      id: 'sec_mcq',
      title: 'أسئلة الاختيار من متعدد',
      type: 'mcq',
      from_q: startMcq,
      to_q: startMcq + totalMcq - 1,
      choices: ['1', '2', '3', '4'],
      mark: 2,
    })
  }

  props.config.questions.sections = newSections
  recalculateRanges()
}

function recalculateRanges() {
  ensureSections()
  let currentQ = 1
  for (const sec of props.config.questions.sections) {
    const count = getSectionCount(sec)
    sec.from_q = currentQ
    sec.to_q = currentQ + count - 1
    currentQ = sec.to_q + 1
  }
  props.config.questions.metadata.num_questions = currentQ - 1
}

function updateSectionCount(idx: number, newCount: number) {
  ensureSections()
  const sec = props.config.questions.sections[idx]
  if (!sec) return
  const count = Math.max(1, Math.min(200, isNaN(newCount) ? 1 : newCount))
  sec.to_q = (sec.from_q || 1) + count - 1
  recalculateRanges()
}

function onSectionTypeChange(idx: number, newType: string) {
  ensureSections()
  const sec = props.config.questions.sections[idx]
  if (!sec) return
  sec.type = newType
  if (newType === 'true_false') {
    sec.choices = ['صح', 'خطأ']
    sec.mark = sec.mark || 1
  } else {
    sec.choices = ['1', '2', '3', '4']
    sec.mark = sec.mark || 2
  }
}

function adjustTfCount(delta: number) {
  ensureSections()
  const newCount = Math.max(0, tfCount.value + delta)
  setTfCount(newCount)
}

function setTfCount(val: number) {
  ensureSections()
  const target = Math.max(0, Math.min(100, isNaN(val) ? 0 : val))
  const tfSecs = props.config.questions.sections.filter((s: any) => s.type === 'true_false')
  if (tfSecs.length === 0) {
    if (target > 0) {
      props.config.questions.sections.unshift({
        id: `sec_tf_${Date.now()}`,
        title: 'أسئلة الصواب والخطأ',
        type: 'true_false',
        from_q: 1,
        to_q: target,
        choices: ['صح', 'خطأ'],
        mark: 1,
      })
    }
  } else if (tfSecs.length === 1) {
    const idx = props.config.questions.sections.indexOf(tfSecs[0])
    if (target === 0 && props.config.questions.sections.length > 1) {
      removeSection(idx)
      return
    }
    updateSectionCount(idx, Math.max(1, target))
    return
  } else {
    tfSecs[0].to_q = (tfSecs[0].from_q || 1) + Math.max(1, target) - 1
    for (let i = 1; i < tfSecs.length; i++) {
      const idx = props.config.questions.sections.indexOf(tfSecs[i])
      props.config.questions.sections.splice(idx, 1)
    }
  }
  recalculateRanges()
}

function adjustMcqCount(delta: number) {
  ensureSections()
  const newCount = Math.max(0, mcqCount.value + delta)
  setMcqCount(newCount)
}

function setMcqCount(val: number) {
  ensureSections()
  const target = Math.max(0, Math.min(200, isNaN(val) ? 0 : val))
  const mcqSecs = props.config.questions.sections.filter((s: any) => s.type === 'mcq')
  if (mcqSecs.length === 0) {
    if (target > 0) {
      props.config.questions.sections.push({
        id: `sec_mcq_${Date.now()}`,
        title: 'أسئلة الاختيار من متعدد',
        type: 'mcq',
        from_q: 1,
        to_q: target,
        choices: ['1', '2', '3', '4'],
        mark: 2,
      })
    }
  } else if (mcqSecs.length === 1) {
    const idx = props.config.questions.sections.indexOf(mcqSecs[0])
    if (target === 0 && props.config.questions.sections.length > 1) {
      removeSection(idx)
      return
    }
    updateSectionCount(idx, Math.max(1, target))
    return
  } else {
    mcqSecs[0].to_q = (mcqSecs[0].from_q || 1) + Math.max(1, target) - 1
    for (let i = 1; i < mcqSecs.length; i++) {
      const idx = props.config.questions.sections.indexOf(mcqSecs[i])
      props.config.questions.sections.splice(idx, 1)
    }
  }
  recalculateRanges()
}

function addNewSection() {
  ensureSections()
  const lastSec = props.config.questions.sections[props.config.questions.sections.length - 1]
  const nextStart = lastSec ? ((lastSec.to_q || 1) + 1) : 1
  props.config.questions.sections.push({
    id: `sec_${Date.now()}`,
    title: `القسم ${props.config.questions.sections.length + 1}: أسئلة اختيار من متعدد`,
    type: 'mcq',
    from_q: nextStart,
    to_q: nextStart + 9, // 10 questions
    choices: ['1', '2', '3', '4'],
    mark: 1,
  })
  recalculateRanges()
}

function removeSection(idx: number) {
  ensureSections()
  if (props.config.questions.sections.length <= 1) return
  props.config.questions.sections.splice(idx, 1)
  recalculateRanges()
}

function moveSection(idx: number, direction: 'up' | 'down') {
  ensureSections()
  const targetIdx = direction === 'up' ? idx - 1 : idx + 1
  if (targetIdx < 0 || targetIdx >= props.config.questions.sections.length) return
  const item = props.config.questions.sections.splice(idx, 1)[0]
  props.config.questions.sections.splice(targetIdx, 0, item)
  recalculateRanges()
}

function applyMinistry40() {
  props.config.template_id = 'YEMEN_MINISTRY_40'
  props.config.template_name = 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (40 سؤال)'
  props.config.display_mode = 'compact_a5'
  if (!props.config.paper) props.config.paper = {}
  props.config.paper.size = 'A5'
  props.config.paper.width_mm = 210
  props.config.paper.height_mm = 148.5
  props.config.paper.orientation = 'landscape'
  props.config.questions.metadata.num_questions = 40
  props.config.questions.sections = [
    { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
    { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 40, choices: ['1', '2', '3', '4'], mark: 2 },
  ]
  props.config.questions.layout.columns_count = 4
  props.config.questions.layout.choices_count = 4
  props.config.questions.layout.bubble_type = 'numbers'
  props.config.questions.layout.tf_bubble_type = 'arabic'
  props.config.questions.layout.row_spacing_mm = 5.2
  props.config.questions.layout.bubble_radius_mm = 2.1
}

function applyYemeniMinistry50() {
  props.config.template_id = 'YEMEN_MINISTRY_50'
  props.config.template_name = 'نموذج اختبار الشهادة الثانوية العامة — وزارة التربية والتعليم (50 سؤال)'
  props.config.display_mode = 'compact_a5'
  if (!props.config.paper) props.config.paper = {}
  props.config.paper.size = 'A5'
  props.config.paper.width_mm = 210
  props.config.paper.height_mm = 148.5
  props.config.paper.orientation = 'landscape'
  props.config.questions.metadata.num_questions = 50
  props.config.questions.sections = [
    { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
    { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 50, choices: ['1', '2', '3', '4'], mark: 2 },
  ]
  props.config.questions.layout.columns_count = 4
  props.config.questions.layout.choices_count = 4
  props.config.questions.layout.bubble_type = 'numbers'
  props.config.questions.layout.tf_bubble_type = 'arabic'
  props.config.questions.layout.row_spacing_mm = 5.2
  props.config.questions.layout.bubble_radius_mm = 2.1
}

function applyMinistry60() {
  props.config.template_id = 'YEMEN_MINISTRY_60'
  props.config.template_name = 'نموذج اختبار (60 سؤال: 20 صح/خطأ + 40 متعدد)'
  props.config.questions.metadata.num_questions = 60
  props.config.questions.sections = [
    { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
    { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 60, choices: ['1', '2', '3', '4'], mark: 1.5 },
  ]
  props.config.questions.layout.columns_count = 4
  props.config.questions.layout.choices_count = 4
  props.config.questions.layout.bubble_type = 'numbers'
  props.config.questions.layout.tf_bubble_type = 'arabic'
  props.config.questions.layout.row_spacing_mm = 4.8
  props.config.questions.layout.bubble_radius_mm = 2.0
}

function applyUniversity180() {
  props.config.template_id = 'YEMEN_UNIVERSITY_180'
  props.config.template_name = 'نموذج الجامعات اليمنية العام (180 سؤال - 4 أعمدة)'
  props.config.questions.metadata.num_questions = 180
  props.config.questions.sections = [
    { id: 'sec1', title: 'أسئلة الاختبار الشامل', type: 'mcq', from_q: 1, to_q: 180, choices: ['1', '2', '3', '4'], mark: 1 },
  ]
  props.config.questions.layout.columns_count = 4
  props.config.questions.layout.choices_count = 4
  props.config.questions.layout.bubble_type = 'numbers'
  props.config.questions.layout.row_spacing_mm = 4.2
  props.config.questions.layout.bubble_radius_mm = 1.7
}

function applyGeneral100() {
  props.config.template_id = 'GENERAL_100'
  props.config.template_name = 'النموذج المعياري العام (100 سؤال)'
  props.config.questions.metadata.num_questions = 100
  props.config.questions.sections = [
    { id: 'sec1', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 1, to_q: 100, choices: ['1', '2', '3', '4'], mark: 1 },
  ]
  props.config.questions.layout.columns_count = 4
  props.config.questions.layout.choices_count = 4
  props.config.questions.layout.bubble_type = 'numbers'
  props.config.questions.layout.row_spacing_mm = 4.6
  props.config.questions.layout.bubble_radius_mm = 1.75
}

function autoFitRowSpacing() {
  const total = totalQuestionsCount.value
  const cols = props.config.questions.layout.columns_count || 4
  const rows = Math.ceil(total / cols)
  const availableH = 175 // mm
  const optimal = Math.max(3.8, Math.min(6.0, Math.floor((availableH / rows) * 10) / 10))
  props.config.questions.layout.row_spacing_mm = optimal
}
</script>
