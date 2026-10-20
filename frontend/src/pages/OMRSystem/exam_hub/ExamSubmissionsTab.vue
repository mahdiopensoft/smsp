<template>
  <div class="exam-submissions-tab">
    <div class="main-card rounded-2xl overflow-hidden mb-4">
      <custom-data-table
        v-bind="{
          items: submissionsTableItems,
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
import { ref, computed } from 'vue'

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

const submissionsTableItems = computed(() => {
  const subs = props.examDetails?.submissions || props.examDetails?.recent_submissions || []
  return {
    results: subs,
    pagination: {
      count: subs.length,
      current_page: 1,
      num_pages: 1,
      page_size: subs.length || 10,
      total: subs.length
    }
  }
})
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
