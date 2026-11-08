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
        <v-chip value="all" size="small" variant="tonal" filter style="border-radius: 6px !important;">
          الكل ({{ questions.length }})
        </v-chip>
        <v-chip value="ambiguous" size="small" color="warning" variant="tonal" filter style="border-radius: 6px !important;">
          ملتبسة ({{ ambiguousCount }})
        </v-chip>
        <v-chip value="wrong" size="small" color="error" variant="tonal" filter style="border-radius: 6px !important;">
          خاطئة ({{ wrongCount }})
        </v-chip>
        <v-chip value="correct" size="small" color="success" variant="tonal" filter style="border-radius: 6px !important;">
          صحيحة ({{ correctCount }})
        </v-chip>
        <v-chip value="empty" size="small" color="grey" variant="tonal" filter style="border-radius: 6px !important;">
          فارغة ({{ emptyCount }})
        </v-chip>
      </v-chip-group>

      <!-- حقل البحث السريع برقم السؤال عبر custom-text-field الموحد -->
      <div style="min-width: 170px; max-width: 210px;">
        <custom-text-field
          v-model="searchQuery"
          placeholder="ابحث برقم السؤال..."
          icon="magnify"
          cols="12"
          :hideDetails="true"
        />
      </div>
    </div>

    <!-- ── جدول تفاصيل الأسئلة الموحد (custom-data-table) ── -->
    <div class="main-card rounded-2xl overflow-hidden flex-grow-1 border">
      <custom-data-table
        :items="reviewTableItems"
        :getData="getReviewData"
        :headers="reviewHeaders"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :numbering="false"
        :showSelect="false"
        :actions="false"
        :search="false"
        :showTop="false"
        :rowClass="getRowClass"
        itemValue="question_number"
        class="bg-transparent"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- رقم السؤال -->
          <template v-if="key === 'question_number'">
            <div class="d-flex justify-center cursor-pointer py-1" @click="$emit('select-question', item)">
              <span class="font-weight-bold text-body-2 text-high-emphasis">
                {{ item.question_number }}
              </span>
            </div>
          </template>

          <!-- نوع السؤال (صح وخطأ vs اختيارات) -->
          <template v-else-if="key === 'question_type'">
            <div class="d-flex justify-center cursor-pointer py-1" @click="$emit('select-question', item)">
              <v-chip
                size="x-small"
                variant="tonal"
                :color="item.is_true_false ? 'teal' : 'indigo'"
                class="font-weight-bold px-2"
                style="border-radius: 6px !important;"
              >
                <v-icon start size="12">{{ item.is_true_false ? 'mdi-check-all' : 'mdi-format-list-bulleted' }}</v-icon>
                {{ item.is_true_false ? 'صح وخطأ' : 'اختيارات' }}
              </v-chip>
            </div>
          </template>

          <!-- الإجابة النموذجية -->
          <template v-else-if="key === 'correct_choice'">
            <div class="d-flex justify-center cursor-pointer py-1" @click="$emit('select-question', item)">
              <v-chip
                v-if="item.correct_choice_display && item.correct_choice_display !== 'لم تُحدد'"
                size="x-small"
                color="success"
                variant="tonal"
                class="font-weight-black px-2 border"
                style="border-radius: 6px !important;"
              >
                <v-icon start size="12" color="success">mdi-check-circle-outline</v-icon>
                {{ item.correct_choice_display }}
              </v-chip>
              <span v-else class="text-caption text-medium-emphasis">لم تُحدد</span>
            </div>
          </template>

          <!-- تظليل الطالب -->
          <template v-else-if="key === 'marked_choice'">
            <div class="d-flex justify-center cursor-pointer py-1" @click="$emit('select-question', item)">
              <v-chip
                v-if="item.marked_choice && item.marked_choice !== 'لم يُجب (فارغ)'"
                size="x-small"
                :color="item.is_correct ? 'success' : 'error'"
                variant="tonal"
                class="font-weight-black px-2"
                style="border-radius: 6px !important;"
              >
                <v-icon start size="12">{{ item.is_correct ? 'mdi-check' : 'mdi-close' }}</v-icon>
                {{ item.marked_choice_display || item.marked_choice }}
              </v-chip>
              <span v-else class="text-caption text-medium-emphasis">فارغ</span>
            </div>
          </template>

          <!-- أزرار التعديل السريع -->
          <template v-else-if="key === 'quick_override'">
            <div class="d-inline-flex align-center justify-center gap-1 py-1" @click.stop>
              <v-btn
                v-for="opt in item.options"
                :key="opt"
                size="x-small"
                density="compact"
                variant="flat"
                :color="getOptionBtnColor(item, opt)"
                :loading="overridingLoading === `${item.question_number}-${opt}`"
                class="font-weight-black px-2 min-width-0"
                style="min-width: 34px; height: 26px; border-radius: 6px !important;"
                @click="onOverrideClick(item, opt)"
              >
                {{ opt }}
              </v-btn>
            </div>
          </template>

          <!-- حالة السؤال -->
          <template v-else-if="key === 'status'">
            <div class="d-flex justify-center cursor-pointer py-1" @click="$emit('select-question', item)">
              <v-chip
                size="x-small"
                :color="getStatusChipColor(item)"
                variant="tonal"
                class="font-weight-medium px-1.5"
                style="border-radius: 6px !important;"
              >
                {{ item.status }}
              </v-chip>
            </div>
          </template>

          <!-- الدرجة المستحقة -->
          <template v-else-if="key === 'score'">
            <div class="d-flex justify-center font-weight-black text-caption py-1 cursor-pointer" @click="$emit('select-question', item)">
              <span :class="item.is_correct ? 'text-success' : 'text-medium-emphasis'">
                {{ item.score }}
              </span>
            </div>
          </template>
        </template>

        <!-- حالة عدم وجود بيانات أو نتائج مطابقة -->
        <template #no-data>
          <div class="text-center py-10">
            <div class="d-flex flex-column align-center justify-center gap-3">
              <div
                class="visual-circle rounded-xl d-flex align-center justify-center"
                :style="{
                  width: '64px',
                  height: '64px',
                  backgroundColor: `rgba(var(--v-theme-${emptyStateConfig.color}), 0.08)`,
                  border: `1px solid rgba(var(--v-theme-${emptyStateConfig.color}), 0.18)`
                }"
              >
                <v-icon size="32" :color="emptyStateConfig.color">{{ emptyStateConfig.icon }}</v-icon>
              </div>
              <div>
                <h4 class="text-subtitle-1 font-weight-bold mb-1" style="color: rgb(var(--v-theme-on-surface));">
                  {{ emptyStateConfig.title }}
                </h4>
                <p class="text-caption text-medium-emphasis mb-0" style="max-width: 320px; margin: 0 auto; line-height: 1.5;">
                  {{ emptyStateConfig.desc }}
                </p>
              </div>
              <v-btn
                v-if="searchQuery || activeFilter !== 'all'"
                size="small"
                variant="tonal"
                color="primary"
                rounded="lg"
                prepend-icon="mdi-filter-remove-outline"
                class="mt-1 font-weight-bold"
                @click="activeFilter = 'all'; searchQuery = ''"
              >
                إعادة ضبط الفلترة
              </v-btn>
            </div>
          </div>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
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

const reviewHeaders = [
  { title: "رقم السؤال", key: "question_number", sortable: true, align: "center", width: "95px" },
  { title: "نوع السؤال", key: "question_type", sortable: false, align: "center", width: "115px" },
  { title: "الإجابة النموذجية", key: "correct_choice", sortable: false, align: "center", width: "125px" },
  { title: "تظليل الطالب", key: "marked_choice", sortable: false, align: "center", width: "125px" },
  { title: "تعديل سريع للإجابة", key: "quick_override", sortable: false, align: "center", minWidth: "190px" },
  { title: "الحالة", key: "status", sortable: false, align: "center", width: "105px" },
  { title: "الدرجة", key: "score", sortable: true, align: "center", width: "85px" },
]

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

const reviewTableItems = ref({
  results: [] as any[],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getReviewData = (params: any = {}) => {
  const p = params?.params || params || {}
  const page = p.page || currentPage.value || 1
  const size = p.page_size || pageSize.value || 15
  currentPage.value = page
  pageSize.value = size
  const all = filteredQuestions.value || []
  const start = (page - 1) * size
  reviewTableItems.value = {
    results: all.slice(start, start + size),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / size) || 1,
      current_page: page,
    },
  }
  return reviewTableItems.value
}

watch([() => props.questions, filteredQuestions], () => {
  getReviewData({ params: { page: currentPage.value, page_size: pageSize.value } })
}, { immediate: true, deep: true })

watch([activeFilter, searchQuery], () => {
  currentPage.value = 1
  getReviewData({ params: { page: 1, page_size: pageSize.value } })
})

const getRowClass = (item: any) => {
  const isSelected = props.selectedQuestion?.question_number === item.question_number
  return isSelected ? 'selected-question-row cursor-pointer' : 'cursor-pointer'
}

const emptyStateConfig = computed(() => {
  if (!props.questions || props.questions.length === 0) {
    return {
      icon: 'mdi-database-off-outline',
      color: 'primary',
      title: 'لا توجد بيانات أسئلة مسجلة',
      desc: 'لم يتم العثور على أي بيانات تصحيح لورقة هذا الطالب حتى الآن.'
    }
  }
  if (searchQuery.value?.trim()) {
    return {
      icon: 'mdi-magnify-remove-outline',
      color: 'secondary',
      title: 'لا توجد نتائج مطابقة للبحث',
      desc: `لم يتم العثور على أي سؤال بالرقم "${searchQuery.value.trim()}".`
    }
  }
  if (activeFilter.value === 'ambiguous') {
    return {
      icon: 'mdi-shield-check-outline',
      color: 'success',
      title: 'ممتاز! لا توجد أسئلة ملتبسة',
      desc: 'جميع قراءات التظليل واضحة بنسبة ثقة عالية ومكتملة.'
    }
  }
  if (activeFilter.value === 'wrong') {
    return {
      icon: 'mdi-check-decagram-outline',
      color: 'success',
      title: 'رائع! لا توجد إجابات خاطئة',
      desc: 'كافة إجابات الطالب المسجلة صحيحة ومطابقة للنموذج.'
    }
  }
  if (activeFilter.value === 'correct') {
    return {
      icon: 'mdi-alert-circle-outline',
      color: 'warning',
      title: 'لا توجد أسئلة صحيحة في هذا النطاق',
      desc: 'لم يتم تسجيل درجات كاملة للأسئلة المحددة حالياً.'
    }
  }
  if (activeFilter.value === 'empty') {
    return {
      icon: 'mdi-pencil-check-outline',
      color: 'info',
      title: 'لا توجد أسئلة متروكة بدون تظليل',
      desc: 'قام الطالب بالإجابة على جميع الأسئلة بالكامل.'
    }
  }
  return {
    icon: 'mdi-database-off-outline',
    color: 'primary',
    title: 'لا توجد أسئلة',
    desc: 'لا توجد سجلات مطابقة للعرض حالياً.'
  }
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
:deep(.selected-question-row td) {
  background-color: rgba(var(--v-theme-primary), 0.12) !important;
}
:deep(tr.cursor-pointer:hover td) {
  background-color: rgba(var(--v-theme-primary), 0.05);
}
:deep(.custom-data-table-toolbar) {
  display: none !important;
}
</style>
