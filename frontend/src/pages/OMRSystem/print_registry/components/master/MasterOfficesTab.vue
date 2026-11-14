<template>
  <custom-data-table
    :key="'offices-tbl-' + filteredCount + '-' + filterKey"
    :model-value="selectedRows"
    @update:model-value="$emit('update:selectedRows', $event)"
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

      <template v-else-if="key === 'office_name'">
        <div class="d-flex align-center py-2" style="min-width: 280px;">
          <v-avatar color="primary" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
            <v-icon color="primary" size="20">mdi-office-building-outline</v-icon>
          </v-avatar>
          <div>
            <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.office_name }}</div>
            <div class="text-caption text-medium-emphasis">المحافظة: {{ item.governorate_name }}</div>
          </div>
        </div>
      </template>

      <template v-else-if="key === 'directorates_count'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-subtitle-2">{{ item.directorates_count ?? 0 }}</span>
        </div>
      </template>

      <template v-else-if="key === 'schools_count'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-subtitle-2">{{ item.schools_count ?? 0 }}</span>
        </div>
      </template>

      <template v-else-if="key === 'exams_count'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-subtitle-2">{{ item.exams_count ?? 0 }}</span>
        </div>
      </template>

      <template v-else-if="key === 'total_students'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-subtitle-2">{{ item.total_students ?? 0 }}</span>
        </div>
      </template>

      <template v-else-if="key === 'printed_count'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-primary">{{ item.printed_count || 0 }} ورقة</span>
        </div>
      </template>

      <template v-else-if="key === 'printed_rate'">
        <div class="d-flex align-center justify-center gap-2 px-1">
          <v-progress-linear
            :model-value="item.printed_rate || 0"
            :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'primary')"
            height="8"
            rounded
            style="min-width: 60px; max-width: 80px;"
          />
          <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
        </div>
      </template>

      <template v-else-if="key === 'print_status'">
        <div class="d-flex justify-center align-center">
          <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
            {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
          </v-chip>
        </div>
      </template>

      <template v-else-if="key === 'actions'">
        <div class="d-flex align-center justify-center gap-2">
          <v-btn
            size="small"
            color="primary"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-arrow-down-right"
            @click="$emit('drill-down', item)"
          >
            المديريات
          </v-btn>
          <v-btn
            size="small"
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer-outline"
            @click="$emit('open-studio', item)"
          >
            استوديو الطباعة
          </v-btn>
        </div>
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
  filteredCount: number
  filterKey: string
}>()

defineEmits<{
  (e: 'update:selectedRows', val: any[]): void
  (e: 'drill-down', item: any): void
  (e: 'open-studio', item: any): void
}>()
</script>
