<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="900px" scrollable>
    <v-card class="rounded-2xl main-card border elevation-4">
      <v-card-title class="pa-4 pa-md-5 border-b d-flex align-center justify-space-between bg-surface">
        <div class="d-flex align-center">
          <v-avatar color="secondary" variant="tonal" size="44" class="me-3 rounded-xl">
            <v-icon size="24">mdi-file-document-check</v-icon>
          </v-avatar>
          <div>
            <div class="text-h6 font-weight-black mb-0">تفاصيل الدفعة المطبوعة</div>
            <div class="text-caption text-medium-emphasis font-mono">
              {{ activeBatch?.batch_id }} - {{ activeBatch?.exam_title }}
            </div>
          </div>
        </div>
        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          density="comfortable"
          color="medium-emphasis"
          @click="$emit('update:modelValue', false)"
        />
      </v-card-title>
      
      <v-card-text class="pa-0 bg-grey-lighten-5">
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
      </v-card-text>
    </v-card>
  </v-dialog>
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
