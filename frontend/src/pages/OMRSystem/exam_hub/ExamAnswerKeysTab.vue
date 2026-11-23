<template>
  <div class="exam-answer-keys-tab">
    <!-- Single Consolidated Model & Answer Key Card -->
    <div class="main-card rounded-2xl pa-4 mb-4">
      <!-- Row 1: Model Selection & Core Model Actions -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
        <!-- Model Selector AutoList (يدعم أي عدد من النماذج للجامعات والمعاهد دون انكسار الواجهة) -->
        <div style="min-width: 220px; max-width: 280px;">
          <auto-list
            :model-value="activeVersionTab"
            name="ExamHubModel"
            :objects="versionSelectOptions"
            cols="12"
            class="pa-0"
            label="النموذج المعروض"
            :add="false"
            :clearable="false"
            @update:model-value="(val) => $emit('update:activeVersionTab', val)"
          />
        </div>

        <!-- Actions for this Model (collapsed into one menu) -->
        <v-btn
          v-if="currentVersionObj"
          variant="tonal"
          color="primary"
          rounded="lg"
          size="small"
          class="font-weight-bold"
          prepend-icon="mdi-newspaper-variant-outline"
          @click="$emit('open-question-paper-modal')"
        >
          معاينة كراسة الأسئلة
        </v-btn>
      </div>

      <!-- Row 2: Answer Key Strip (Inline & Sleek) -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3" v-if="currentVersionObj">
        <div class="d-flex align-center gap-2">
          <v-icon color="success" size="18">mdi-key-variant</v-icon>
          <span class="text-caption font-weight-black text-on-surface">
            مفتاح الإجابة المعتمد (النموذج {{ currentVersionObj.versionCode }}):
          </span>
          <span class="text-caption text-medium-emphasis">({{ Object.keys(currentVersionObj.answerKey || currentVersionObj.answer_key || {}).length }} إجابة)</span>
        </div>

        <!-- Answer Key Pills -->
        <div class="d-flex align-center gap-1 flex-wrap">
          <div
            v-for="(ans, qNum) in (currentVersionObj.answerKey || currentVersionObj.answer_key || {})"
            :key="qNum"
            class="answer-key-pill d-inline-flex align-center px-2 py-0.5 rounded border"
          >
            <span class="font-mono text-caption text-medium-emphasis me-1">س{{ qNum }}:</span>
            <span class="font-weight-black font-mono text-caption text-primary">{{ ans }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="currentVersionObj">
      <!-- Unified Filter Fields for Questions -->
      <filter-fields label="خيارات تصفية والبحث في أسئلة النموذج" class="main-card border-0 pa-4 rounded-2xl mb-4">
        <template #fields>

          <!-- Bloom Level -->
          <auto-list
            v-model="filterBloomLevel"
            name="ExamHubBloomLevel"
            :objects="bloomLevelOptions"
            cols="3"
            :add="false"
          />

          <!-- Question Type -->
          <auto-list
            v-model="filterQuestionType"
            name="ExamHubQuestionType"
            :objects="questionTypeFilterOptions"
            cols="3"
            :add="false"
          />

          <!-- Actions -->
          <v-col cols="auto" class="d-flex align-center gap-2 mb-6">
            <custom-btn
              type="show"
              label="عرض"
              color="primary"
              class="font-weight-bold px-5"
              :click="applyQuestionFilters"
            />
            <custom-btn
              type="cancel_filter"
              :click="resetQuestionFilters"
              variant="tonal"
              color="error"
              label="إلغاء الفلترة"
              class="font-weight-bold"
            />
          </v-col>
        </template>
      </filter-fields>

      <!-- Unified Custom Data Table for Questions -->
      <div class="main-card rounded-2xl overflow-hidden mb-4">
        <custom-data-table
          v-bind="{
            items: qTableItems,
            getData: getQuestionsData,
            headers: questionsHeaders,
          }"
          :search="true"
          :hasFilter="false"
          :log="false"
          :restore="false"
        >
          <template v-slot:item-slot="{ item, key }">
            <!-- Question Number -->
            <template v-if="key === 'orderIndex'">
              <span class="font-weight-bold font-mono text-body-2">{{ item.orderIndex }}</span>
            </template>

            <!-- Question Content & Options -->
            <template v-else-if="key === 'question_content'">
              <div class="py-2 text-start">
                <div class="text-body-2 font-weight-bold mb-2 text-on-surface" v-html="$sanitizeHtml(item.content)"></div>
                <!-- Options Badges -->
                <div class="d-flex flex-wrap gap-2">
                  <div
                    v-for="opt in item.options"
                    :key="opt.id"
                    class="option-badge px-2 py-1 rounded-lg text-caption d-inline-flex align-center border"
                    :class="{ 'option-correct': opt.isTrue }"
                  >
                    <span class="font-weight-black font-mono me-1" :class="opt.isTrue ? 'text-success' : 'text-medium-emphasis'">
                      {{ opt.letter }} ({{ opt.arabic_letter }}):
                    </span>
                    <span :class="opt.isTrue ? 'font-weight-bold text-on-surface' : 'text-medium-emphasis'">
                      {{ opt.text }}
                    </span>
                    <v-icon v-if="opt.isTrue" size="14" color="success" class="ms-1">mdi-check-circle</v-icon>
                  </div>
                </div>
              </div>
            </template>

            <!-- Bloom Level -->
            <template v-else-if="key === 'bloom_level'">
              <span class="text-body-2 font-weight-medium">{{ item.bloomLevel || 'عام' }}</span>
            </template>

            <!-- Correct Answer -->
            <template v-else-if="key === 'correct_answer'">
              <v-chip size="small" color="success" variant="tonal" class="font-weight-black font-mono unified-table-chip px-3">
                <v-icon size="14" start>mdi-check-circle-outline</v-icon>
                {{ item.correctLetter }} ({{ item.correctArabic }})
              </v-chip>
            </template>

            <!-- Assigned Mark -->
            <template v-else-if="key === 'assigned_mark'">
              <span class="font-weight-black font-mono text-body-2 text-primary">
                {{ item.assignedMark }}
              </span>
            </template>
          </template>
        </custom-data-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  activeExam: { type: Object, default: () => ({}) },
  examDetails: { type: Object, default: () => ({}) },
  activeVersionTab: { type: Number, default: 0 },
})

defineEmits([
  'update:activeVersionTab',
  'open-question-paper-modal',
])

const questionSearchQuery = ref('')
const filterBloomLevel = ref(null)
const filterQuestionType = ref(null)

const currentVersionObj = computed(() => {
  if (!props.examDetails?.versions?.length) return null
  return props.examDetails.versions[props.activeVersionTab] || props.examDetails.versions[0]
})

const versionSelectOptions = computed(() => {
  if (!props.examDetails?.versions?.length) return []
  return props.examDetails.versions.map((v, idx) => ({
    title: `النموذج ${v.versionCode} (${v.questionsCount || v.questions?.length || 0} سؤال)`,
    value: idx
  }))
})

const bloomLevelOptions = computed(() => {
  const opts = [{ title: 'الكل (جميع المستويات)', value: null }]
  const qs = currentVersionObj.value?.questions || []
  const levels = new Set()
  qs.forEach(q => {
    if (q.bloomLevel) levels.add(q.bloomLevel)
  })
  levels.forEach(lvl => opts.push({ title: lvl, value: lvl }))
  return opts
})

const questionTypeFilterOptions = [
  { title: 'الكل (جميع الأنواع)', value: null },
  { title: 'صواب أو خطأ', value: 'true_false' },
  { title: 'اختيار من متعدد', value: 'mcq' },
]

const appliedQuestionSearch = ref('')
const appliedBloomLevel = ref(null)
const appliedQuestionType = ref(null)

const applyQuestionFilters = () => {
  appliedQuestionSearch.value = questionSearchQuery.value || ''
  appliedBloomLevel.value = filterBloomLevel.value
  appliedQuestionType.value = filterQuestionType.value
}

const filteredQuestions = computed(() => {
  let list = currentVersionObj.value?.questions || []
  if (appliedBloomLevel.value) {
    list = list.filter(q => q.bloomLevel === appliedBloomLevel.value)
  }
  if (appliedQuestionType.value) {
    list = list.filter(q => {
      const typeStr = (q.question_type || q.type || '').toLowerCase()
      if (appliedQuestionType.value === 'true_false') {
        return typeStr.includes('true') || typeStr.includes('tf') || typeStr.includes('صح')
      }
      return !typeStr.includes('true') && !typeStr.includes('tf') && !typeStr.includes('صح')
    })
  }
  if (appliedQuestionSearch.value && appliedQuestionSearch.value.trim()) {
    const s = appliedQuestionSearch.value.trim().toLowerCase()
    list = list.filter(q => {
      const contentMatch = (q.content || q.text || '').toLowerCase().includes(s)
      const optionsMatch = (q.options || []).some(o => (o.text || '').toLowerCase().includes(s))
      return contentMatch || optionsMatch
    })
  }
  return list
})

const questionsHeaders = ref([
  { title: '#', key: 'orderIndex', sortable: false, width: '70px' },
  { title: 'نص السؤال والخيارات', key: 'question_content', sortable: false },
  { title: 'المستوى المعرفي', key: 'bloom_level', sortable: false, width: '130px' },
  { title: 'الإجابة الصحيحة', key: 'correct_answer', sortable: false, width: '130px' },
  { title: 'الدرجة', key: 'assigned_mark', sortable: false, width: '80px' },
])

const qPage = ref(1)
const qPageSize = ref(10)
const qTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getQuestionsData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || qPage.value || 1
  const pageSize = Number(p.page_size) || qPageSize.value || 10
  qPage.value = page
  qPageSize.value = pageSize

  const all = filteredQuestions.value || []
  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  qTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return qTableItems.value
}

watch(filteredQuestions, () => {
  qPage.value = 1
  getQuestionsData({ page: 1, page_size: qPageSize.value })
}, { immediate: true })

const questionsTableItems = computed(() => qTableItems.value)

const resetQuestionFilters = () => {
  questionSearchQuery.value = ''
  filterBloomLevel.value = null
  filterQuestionType.value = null
  appliedQuestionSearch.value = ''
  appliedBloomLevel.value = null
  appliedQuestionType.value = null
}
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
.answer-key-pill {
  white-space: nowrap;
  min-width: 54px;
  justify-content: center;
  border-color: rgba(var(--v-border-color), 0.12) !important;
  background: rgba(var(--v-theme-surface-variant), 0.12) !important;
  transition: all 0.15s ease;
}
.answer-key-pill:hover {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
}
.option-badge {
  background: rgba(var(--v-theme-on-surface), 0.05);
  border: 1px solid rgba(var(--v-border-color), 0.1);
}
.option-correct {
  background: rgba(var(--v-theme-success), 0.12) !important;
  border-color: rgba(var(--v-theme-success), 0.3) !important;
  color: rgb(var(--v-theme-success)) !important;
  font-weight: bold;
}
.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
.font-mono {
  font-family: monospace, monospace;
}
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
</style>
