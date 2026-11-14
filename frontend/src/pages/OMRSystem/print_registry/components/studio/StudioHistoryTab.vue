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
        :actions="false"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :numbering="true"
        :search="true"
        class="bg-transparent"
      >
        <template v-slot:item-slot="{ item, key, index }">
          <template v-if="key === 'numbering'">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </template>
          <template v-else-if="key === 'batch_info'">
            <div class="d-flex align-center py-2">
              <v-avatar color="secondary" variant="tonal" size="38" class="me-3 rounded-lg">
                <v-icon size="20">mdi-folder-printer</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-black text-body-2 font-mono text-on-surface">{{ item.batch_id }}</div>
                <div class="text-caption text-medium-emphasis mt-1">
                  {{ item.print_date }}
                </div>
              </div>
            </div>
          </template>

          <template v-else-if="key === 'exam_info'">
            <div class="font-weight-bold text-body-2">{{ item.exam_title }}</div>
          </template>

          <template v-else-if="key === 'papers_count'">
            <v-chip
              color="primary"
              variant="tonal"
              size="small"
              class="font-weight-bold unified-table-chip"
              prepend-icon="mdi-file-document-multiple"
            >
              {{ item.total_papers }} ورقة
            </v-chip>
          </template>

          <template v-else-if="key === 'status'">
            <v-chip
              color="success"
              variant="flat"
              size="small"
              class="font-weight-bold unified-table-chip"
              prepend-icon="mdi-check-all"
            >
              {{ item.status }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                is-icon
                icon="eye"
                color="primary"
                variant="tonal"
                label="استعراض تفاصيل الدفعة والطلاب"
                :click="() => $emit('view-batch', item)"
              />
            </div>
          </template>
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
