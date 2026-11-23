<template>
  <custom-dialog
    :model-value="modelValue"
    title="تفاصيل الدفعة المطبوعة"
    width="900"
    height="85vh"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div class="text-caption text-medium-emphasis font-mono mb-4 pb-3 border-b">
      {{ activeBatch?.batch_id }} - {{ activeBatch?.exam_title }}
    </div>

    <div v-if="loading" class="text-center py-12">
      <v-progress-circular indeterminate color="primary" size="44" class="mb-3" />
      <p class="text-body-2 font-weight-bold">جاري تحميل قائمة الطلاب...</p>
    </div>
    <div v-else>
      <custom-data-table
        v-bind="{
          items: tableItems,
          getData: getData,
          headers: headers,
        }"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :actions="false"
      >
        <template v-slot:item-slot="{ item, key, index }">
          <template v-if="key === 'numbering'">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </template>
          <template v-else-if="key === 'seat_number'">
            <span class="font-weight-bold font-mono">{{ item.seat_number }}</span>
          </template>
          <template v-else-if="key === 'model_code'">
            <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
              {{ item.model_code }}
            </v-chip>
          </template>
          <template v-else-if="key === 'printed_at'">
            <span class="text-caption text-medium-emphasis">{{ item.printed_at }}</span>
          </template>
        </template>
      </custom-data-table>
    </div>
  </custom-dialog>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  activeBatch?: any
  loading?: boolean
  tableItems?: any
  getData?: any
  headers?: any[]
}>()

defineEmits<{
  (e: 'update:modelValue', val: boolean): void
}>()
</script>
