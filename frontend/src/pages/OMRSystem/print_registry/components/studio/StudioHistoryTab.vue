<template>
  <div class="studio-history-tab">
    <!-- Unified Custom Data Table for Batches with Built-in Search -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        v-bind="{
          items: batchesTableItems,
          getData: getBatchesData,
          headers,
          loading: loadingBatches,
        }"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :numbering="true"
        :search="true"
        class="bg-transparent"
      
        :actionList="(item) => ([ { label: 'استعراض تفاصيل الدفعة والطلاب', icon: 'eye-outline', color: 'primary', onClick: () => $emit('view-batch', item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
        <template v-slot:item-slot="{ item, key, index }">
          <template v-if="key === 'numbering'">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </template>
          <template v-else-if="key === 'batch_info'">
            <div class="py-1">
              <div class="font-weight-bold text-body-2 font-mono text-on-surface">{{ item.batch_id }}</div>
              <div class="text-caption text-medium-emphasis mt-0.5">
                {{ item.print_date }}
              </div>
            </div>
          </template>

          <template v-else-if="key === 'exam_info'">
            <div class="font-weight-bold text-body-2">{{ item.exam_title }}</div>
          </template>

          <template v-else-if="key === 'papers_count'">
            <span class="font-mono font-weight-bold text-body-2">{{ item.total_papers }} ورقة</span>
          </template>

          <template v-else-if="key === 'status'">
            <v-chip
              color="success"
              variant="tonal"
              size="small"
              class="font-weight-bold"
            >
              {{ item.status }}
            </v-chip>
          </template>

          <!-- Actions -->
          
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  batchesTableItems: any
  getBatchesData: any
  headers: any[]
  loadingBatches: boolean
}>()

defineEmits<{
  (e: 'view-batch', item: any): void
}>()
</script>
