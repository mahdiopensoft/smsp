<template>
  <custom-data-table
    :model-value="selectedRows"
    @update:model-value="$emit('update:selectedRows', $event)"
    item-value="batch_id"
    :items="items"
    :getData="getData"
    :headers="headers"
    :customLoading="loading"
    :hasFilter="false"
    :log="false"
    :restore="false"
    :numbering="true"
    :showSelect="true"
    :actions="false"
    :search="false"
    class="bg-transparent"
  >
    <template v-slot:item-slot="{ item, key, index }">
      <template v-if="key === 'numbering'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
        </div>
      </template>

      <template v-else-if="key === 'batch_id'">
        <div class="d-flex justify-center align-center">
          <span class="font-mono font-weight-bold text-caption text-primary">
            {{ item.batch_id }}
          </span>
        </div>
      </template>

      <template v-else-if="key === 'exam_title'">
        <span class="text-body-2 font-weight-medium text-wrap">{{ item.exam_title }}</span>
      </template>

      <template v-else-if="key === 'total_sheets'">
        <div class="d-flex justify-center align-center">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
            {{ item.total_sheets }} ورقة
          </v-chip>
        </div>
      </template>

      <template v-else-if="key === 'printed_at'">
        <div class="d-flex justify-center align-center">
          <span class="text-caption text-medium-emphasis">{{ item.printed_at || '-' }}</span>
        </div>
      </template>

      <template v-else-if="key === 'printed_by_name'">
        <div class="d-flex justify-center align-center">
          <span class="text-body-2">{{ item.printed_by_name || '-' }}</span>
        </div>
      </template>

      <template v-else-if="key === 'actions'">
        <v-btn
          size="small"
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-eye-outline"
          @click="$emit('view-batch', item)"
        >
          تفاصيل الدفعة
        </v-btn>
      </template>
    </template>
  </custom-data-table>
</template>

<script setup lang="ts">
defineProps<{
  items: any
  getData: (params?: any) => Promise<any>
  headers: any[]
  loading?: boolean
  selectedRows: any[]
}>()

defineEmits<{
  (e: 'update:selectedRows', val: any[]): void
  (e: 'view-batch', item: any): void
}>()
</script>
