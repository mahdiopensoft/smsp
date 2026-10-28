<template>
  <div class="review-questions-table-container d-flex flex-column h-100">
    <!-- ── شريط التصفية والبحث في الأسئلة ── -->
    <div class="filters-bar d-flex align-center justify-space-between flex-wrap gap-2 mb-2 px-2 py-1 bg-surface-variant-subtle rounded-xl border">
      <!-- أزرار فلترة الأسئلة -->
      <v-chip-group
        v-model="activeFilter"
        mandatory
        selected-class="text-primary font-weight-black elevation-1"
        density="compact"
      >
        <v-chip value="all" size="small" variant="tonal" filter>
          الكل ({{ questions.length }})
        </v-chip>
        <v-chip value="ambiguous" size="small" color="warning" variant="tonal" filter>
          ملتبسة ({{ ambiguousCount }})
        </v-chip>
        <v-chip value="wrong" size="small" color="error" variant="tonal" filter>
          خاطئة ({{ wrongCount }})
        </v-chip>
        <v-chip value="correct" size="small" color="success" variant="tonal" filter>
          صحيحة ({{ correctCount }})
        </v-chip>
        <v-chip value="empty" size="small" color="grey" variant="tonal" filter>
          فارغة ({{ emptyCount }})
        </v-chip>
      </v-chip-group>

      <!-- حقل البحث السريع برقم السؤال -->
      <v-text-field
        v-model="searchQuery"
        placeholder="ابحث برقم السؤال..."
        prepend-inner-icon="mdi-magnify"
        density="compact"
        variant="outlined"
        hide-details
        clearable
        rounded="lg"
        style="max-width: 180px;"
      />
    </div>

    <!-- ── جدول تفاصيل الأسئلة (Scrollable Body) ── -->
    <div class="table-wrapper border rounded-xl overflow-hidden flex-grow-1 bg-white position-relative">
      <v-table density="compact" fixed-header class="unified-review-table h-100">
        <thead>
          <tr class="bg-surface-variant-subtle text-caption font-weight-bold">
            <th class="text-center" style="width: 75px;">رقم السؤال</th>
            <th class="text-center" style="width: 105px;">نوع السؤال</th>
            <th class="text-center" style="width: 110px;">الإجابة النموذجية</th>
            <th class="text-center" style="width: 110px;">تظليل الطالب</th>
            <th class="text-center" style="min-width: 180px;">تعديل سريع للإجابة</th>
            <th class="text-center" style="width: 95px;">الحالة</th>
            <th class="text-center" style="width: 70px;">الدرجة</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in pagedQuestions"
            :key="item.question_number"
            class="question-row cursor-pointer"
            :class="{ 'selected-row': selectedQuestion?.question_number === item.question_number }"
            @click="$emit('select-question', item)"
          >
            <!-- رقم السؤال -->
            <td class="text-center py-1">
              <span
                class="font-weight-black text-caption px-2.5 py-0.5 rounded-pill border"
                :class="selectedQuestion?.question_number === item.question_number ? 'bg-primary text-white elevation-1' : 'text-primary bg-blue-lighten-5'"
              >
                #{{ item.question_number }}
              </span>
            </td>

            <!-- نوع السؤال (صح وخطأ vs اختيارات) -->
            <td class="text-center py-1">
              <v-chip
                size="x-small"
                variant="tonal"
                :color="item.is_true_false ? 'teal' : 'indigo'"
                class="font-weight-bold px-2"
              >
                <v-icon start size="12">{{ item.is_true_false ? 'mdi-check-all' : 'mdi-format-list-bulleted' }}</v-icon>
                {{ item.is_true_false ? 'صح وخطأ' : 'اختيارات' }}
              </v-chip>
            </td>

            <!-- الإجابة النموذجية -->
            <td class="text-center py-1">
              <v-chip
                v-if="item.correct_choice_display && item.correct_choice_display !== 'لم تُحدد'"
                size="x-small"
                color="success"
                variant="tonal"
                class="font-weight-black px-2 border"
              >
                <v-icon start size="12" color="success">mdi-check-circle-outline</v-icon>
                {{ item.correct_choice_display }}
              </v-chip>
              <span v-else class="text-caption text-medium-emphasis">لم تُحدد</span>
            </td>

            <!-- تظليل الطالب -->
            <td class="text-center py-1">
              <v-chip
                v-if="item.marked_choice && item.marked_choice !== 'لم يُجب (فارغ)'"
                size="x-small"
                :color="item.is_correct ? 'success' : 'error'"
                variant="tonal"
                class="font-weight-black px-2"
              >
                <v-icon start size="12">{{ item.is_correct ? 'mdi-check' : 'mdi-close' }}</v-icon>
                {{ item.marked_choice_display || item.marked_choice }}
              </v-chip>
              <span v-else class="text-caption text-medium-emphasis">فارغ</span>
            </td>

            <!-- أزرار التعديل السريع -->
            <td class="text-center py-1" @click.stop>
              <div class="d-inline-flex align-center gap-1">
                <v-btn
                  v-for="opt in item.options"
                  :key="opt"
                  size="x-small"
                  density="compact"
                  variant="flat"
                  :color="getOptionBtnColor(item, opt)"
                  :loading="overridingLoading === `${item.question_number}-${opt}`"
                  class="font-weight-black px-2 min-width-0"
                  style="min-width: 34px; height: 26px;"
                  @click="onOverrideClick(item, opt)"
                >
                  {{ opt }}
                </v-btn>
              </div>
            </td>

            <!-- حالة السؤال -->
            <td class="text-center py-1">
              <v-chip
                size="x-small"
                :color="getStatusChipColor(item)"
                variant="tonal"
                class="font-weight-medium px-1.5"
              >
                {{ item.status }}
              </v-chip>
            </td>

            <!-- الدرجة المستحقة -->
            <td class="text-center py-1 font-weight-black text-caption">
              <span :class="item.is_correct ? 'text-success' : 'text-medium-emphasis'">
                {{ item.score }}
              </span>
            </td>
          </tr>

          <tr v-if="pagedQuestions.length === 0">
            <td colspan="7" class="text-center py-8 text-medium-emphasis">
              لا توجد أسئلة تطابق معايير الفلترة الحالية
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- ── شريط التنقل في صفحات الجدول ── -->
    <div class="d-flex align-center justify-space-between px-3 py-1 bg-surface-variant-subtle rounded-xl border mt-2">
      <div class="text-caption text-medium-emphasis">
        عرض {{ pagedQuestions.length }} من إجمالي {{ filteredQuestions.length }} سؤال
      </div>
      <v-pagination
        v-if="pageCount > 1"
        v-model="currentPage"
        :length="pageCount"
        density="compact"
        total-visible="5"
        size="small"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { normalizeChoice, getStatusChip } from './reviewUtils'

const props = defineProps<{
  questions: any[]
  selectedQuestion: any
  overridingLoading?: string
}>()

const emit = defineEmits<{
  (e: 'select-question', question: any): void
  (e: 'override-choice', payload: { question: any; choice: string }): void
}>()

const activeFilter = ref<'all' | 'ambiguous' | 'wrong' | 'correct' | 'empty'>('all')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(15)

const ambiguousCount = computed(() => {
  return props.questions.filter(q => q.bubble_state === 'ambiguous' || (q.final_confidence && q.final_confidence < 0.7)).length
})

const wrongCount = computed(() => {
  return props.questions.filter(q => q.is_correct === false && q.marked_choice && q.marked_choice !== 'لم يُجب (فارغ)').length
})

const correctCount = computed(() => {
  return props.questions.filter(q => q.is_correct === true).length
})

const emptyCount = computed(() => {
  return props.questions.filter(q => !q.marked_choice || q.marked_choice === 'لم يُجب (فارغ)').length
})

const filteredQuestions = computed(() => {
  let list = props.questions || []

  // Apply Filter Tab
  if (activeFilter.value === 'ambiguous') {
    list = list.filter(q => q.bubble_state === 'ambiguous' || (q.final_confidence && q.final_confidence < 0.7))
  } else if (activeFilter.value === 'wrong') {
    list = list.filter(q => q.is_correct === false && q.marked_choice && q.marked_choice !== 'لم يُجب (فارغ)')
  } else if (activeFilter.value === 'correct') {
    list = list.filter(q => q.is_correct === true)
  } else if (activeFilter.value === 'empty') {
    list = list.filter(q => !q.marked_choice || q.marked_choice === 'لم يُجب (فارغ)')
  }

  // Apply Search
  const query = searchQuery.value?.trim()
  if (query) {
    list = list.filter(q => String(q.question_number).includes(query))
  }

  return list
})

const pageCount = computed(() => {
  return Math.ceil(filteredQuestions.value.length / pageSize.value) || 1
})

const pagedQuestions = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredQuestions.value.slice(start, start + pageSize.value)
})

function getOptionBtnColor(item: any, opt: string) {
  const isSelected = normalizeChoice(item.marked_choice) === normalizeChoice(opt) || String(item.marked_choice).trim() === String(opt).trim()
  if (isSelected) {
    if (item.is_correct === true) return 'success'
    if (item.is_correct === false && item.marked_choice && item.marked_choice !== 'لم يُجب (فارغ)') return 'error'
    return 'primary'
  }
  return 'grey-lighten-3'
}

function getStatusChipColor(item: any) {
  return getStatusChip(item).color
}

function onOverrideClick(item: any, opt: string) {
  emit('override-choice', { question: item, choice: opt })
}
</script>

<style scoped>
.unified-review-table {
  border-collapse: separate;
}
.question-row:hover {
  background-color: rgba(var(--v-theme-primary), 0.04);
}
.selected-row {
  background-color: rgba(var(--v-theme-primary), 0.08) !important;
}
</style>
