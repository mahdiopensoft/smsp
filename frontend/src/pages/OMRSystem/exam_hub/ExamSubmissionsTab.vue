<template>
  <div class="exam-submissions-tab">
    <div class="main-card rounded-2xl overflow-hidden mb-4">
      <custom-data-table
        v-bind="{
          items: subTableItems,
          getData: getSubmissionsData,
          headers: submissionsHeaders,
        }"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <template v-if="key === 'submission_id'">
            <span class="font-mono text-caption text-medium-emphasis">#{{ item.id }}</span>
          </template>

          <template v-else-if="key === 'seat_number'">
            <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold font-mono unified-table-chip">
              {{ item.seat_number || '—' }}
            </v-chip>
          </template>

          <template v-else-if="key === 'student_name'">
            <span class="font-weight-bold text-body-2">{{ item.student_name || 'طالب' }}</span>
          </template>

          <template v-else-if="key === 'score'">
            <span class="font-weight-black text-body-1 text-primary">{{ item.score ?? '—' }}</span>
          </template>

          <template v-else-if="key === 'confidence'">
            <span v-if="item.confidence != null" class="font-mono font-weight-bold text-caption text-success">
              {{ Math.round(item.confidence * 100) }}%
            </span>
            <span v-else class="text-caption text-medium-emphasis">—</span>
          </template>

          <template v-else-if="key === 'status'">
            <v-chip size="small" color="success" variant="tonal" class="font-weight-bold unified-table-chip">
              {{ item.status }}
            </v-chip>
          </template>

          <template v-else-if="key === 'created_at'">
            <span class="text-caption text-medium-emphasis">{{ item.created_at }}</span>
          </template>

          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                type="show"
                is-icon
                label="عرض وتدقيق الورقة"
                :click="() => $emit('view-submissions', activeExam)"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  activeExam: { type: Object, default: () => ({}) },
  examDetails: { type: Object, default: () => ({}) },
})

defineEmits(['view-submissions'])

const submissionsHeaders = ref([
  { title: '#', key: 'submission_id', sortable: false, width: '80px' },
  { title: 'رقم الجلوس', key: 'seat_number', sortable: false, width: '120px' },
  { title: 'اسم الطالب', key: 'student_name', sortable: false },
  { title: 'الدرجة', key: 'score', sortable: false, width: '90px' },
  { title: 'نسبة الدقة', key: 'confidence', sortable: false, width: '100px' },
  { title: 'الحالة', key: 'status', sortable: false, width: '100px' },
  { title: 'تاريخ المعالجة', key: 'created_at', sortable: false, width: '140px' },
  { title: 'الإجراءات', key: 'actions', sortable: false, width: '90px' },
])

const subPage = ref(1)
const subPageSize = ref(10)
const subTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const rawSubmissions = computed(() => {
  return props.examDetails?.submissions || props.examDetails?.recent_submissions || []
})

const getSubmissionsData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || subPage.value || 1
  const pageSize = Number(p.page_size) || subPageSize.value || 10
  subPage.value = page
  subPageSize.value = pageSize

  const all = rawSubmissions.value || []
  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  subTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return subTableItems.value
}

watch(rawSubmissions, () => {
  subPage.value = 1
  getSubmissionsData({ page: 1, page_size: subPageSize.value })
}, { immediate: true })

const submissionsTableItems = computed(() => subTableItems.value)
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
.font-mono {
  font-family: monospace, monospace;
}
.gap-1 { gap: 4px; }
</style>
