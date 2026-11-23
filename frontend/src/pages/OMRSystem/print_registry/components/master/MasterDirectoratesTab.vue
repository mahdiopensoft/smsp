<template>
  <custom-data-table
    :key="'dirs-tbl-' + filteredCount + '-' + filterKey"
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
    :search="false"
    class="bg-transparent"
  
        :actionList="(item) => ([ { label: 'المراكز والمدارس', icon: 'school', color: 'teal', onClick: () => $emit('drill-down', item) }, { label: 'استوديو الطباعة', icon: 'printer-outline', color: 'primary', onClick: () => $emit('open-studio', item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
    <template v-slot:item-slot="{ item, key, index }">
      <template v-if="key === 'numbering'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
        </div>
      </template>

      <template v-else-if="key === 'name'">
        <div class="py-1 font-weight-bold text-subtitle-2 text-on-surface text-wrap" style="min-width: 240px;">
          {{ item.name }}
        </div>
      </template>

      <template v-else-if="key === 'office_name'">
        <div class="d-flex justify-center align-center">
          <span class="text-body-2 font-weight-medium">{{ item.office_name || '-' }}</span>
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
          <span class="font-weight-bold text-teal">{{ item.printed_count || 0 }} ورقة</span>
        </div>
      </template>

      <template v-else-if="key === 'printed_rate'">
        <div class="d-flex align-center justify-center gap-2 px-1">
          <v-progress-linear
            :model-value="item.printed_rate || 0"
            :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'teal')"
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
